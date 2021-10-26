import time

from licensing.methods import Helpers, Key
from sphinx.util import logging

from sphinx_needs_enterprise.config import (
    API_TOKEN,
    LICENSE_INTERVAL_SECS,
    LICENSE_RETRIES,
    LICENSE_RETRY_SECS,
    RSA_PUB_KEY,
    TEXT_INVALID,
    TEXT_INVALID_WARNING,
    TEXT_PRIVATE_FULL,
    TEXT_PRIVATE_SHORT,
    TEXT_VALID,
)


class License:
    def __init__(
        self,
        product_id,
        product_name,
        license_key=None,
        product_url=None,
        docs_url=None,
        license_url=None,
        suppress_private_message=False,
        rsa_key=RSA_PUB_KEY,
        api_token=API_TOKEN,
    ):

        self.log = logging.getLogger(__name__)

        self.rsa_pub_key = rsa_key
        self.token = api_token
        self.product_id = product_id
        self.product_name = product_name
        self.product_url = product_url
        self.docs_url = docs_url
        self.license_url = license_url
        self.license_key = license_key
        self.suppress_private_message = suppress_private_message

        self.machine_code = Helpers.GetMachineCode()

        self.is_valid = None
        self.activated = False
        self.is_private = None
        self.is_commercial = None
        self.customer = None
        self.server_reachable = None
        self.license = None
        self.message = None
        self.limit_reached = None
        self.last_check = 0

    def check(self, own_output=False):
        """
        Checks and activates a given key.
        This function should be used as early as possible.

        Set "own_output" to True to let the extension print all the needed output to inform the user about the
        license status. Otherwise some common information will be printed, if license check fails.

        :param own_output: Flag, if True no output will be printed.
        :return: True, if license is valid and available, else false.
        """

        # check/recheck a license only, if the license-timeout as been reached.
        # Otherwise a check makes no sense and is too early.
        if not time.time() - self.last_check >= LICENSE_INTERVAL_SECS:
            return self.is_valid, self.server_reachable

        self.last_check = time.time()

        self.is_valid = False
        self.activated = False
        self.server_reachable = None

        if not self.license_key or self.license_key.upper() == "PRIVATE":
            self.is_valid = True
            self.is_private = True
            self.is_commercial = False
            self.server_reachable = True
            self.limit_reached = False

            return self.is_valid, self.server_reachable

        self.is_private = False
        self.is_commercial = True

        attempt = 1
        while (self.limit_reached is None or self.limit_reached is True) and attempt <= 3:
            if attempt > 1:
                time.sleep(LICENSE_RETRY_SECS)
            self.log.debug(f"License attempt: {attempt}")
            self.license, self.message = Key.activate(
                token=self.token,
                rsa_pub_key=self.rsa_pub_key,
                product_id=self.product_id,
                key=self.license_key,
                machine_code=self.machine_code,
                floating_time_interval=LICENSE_INTERVAL_SECS,
            )

            if "Could not contact the server" in self.message:
                self.server_reachable = False
                self.log.info(
                    f"License server not reachable "
                    f"Try again in {LICENSE_RETRY_SECS} secs. Attempt {attempt}/{LICENSE_RETRIES}"
                )
            else:
                self.server_reachable = True

            if "limit has been reached" in self.message:
                self.limit_reached = True
                self.log.info(
                    f"License limit has been reached. "
                    f"Try again in {LICENSE_RETRY_SECS} secs. Attempt {attempt}/{LICENSE_RETRIES}"
                )
            else:
                self.limit_reached = False

            attempt += 1

        if self.license is None:
            return self.is_valid, self.server_reachable

        self.is_valid = True
        self.activated = True

        self.customer = f"{self.license.customer['Name']} ({self.license.customer['CompanyName']})"

        return self.is_valid, self.server_reachable

    def free(self):
        """
        Gives back a a floating license.
        Should normally be called at the end of a build process
        """

        # Private licenses are not registered on server.
        # Also do not free a license, if it is invalid.
        if self.is_private or not self.is_valid:
            return

        success, message = Key.deactivate(
            token=self.token,
            product_id=self.product_id,
            key=self.license_key,
            machine_code=self.machine_code,
            floating=True,
        )
        if not success:
            self.log.info(f"Could not free license: {message}")

        return success

    def print_info(self):
        """
        Prints the current user information regarding the license status.

        As the status is checked several times during a single build,
        we can not print everytime information to the user.
        So this functions helps to bother the user only on specific points of the build process
        (e.g. start and end).
        """
        if not self.license_key or self.is_private:
            if not self.suppress_private_message:
                self.log.info(
                    TEXT_PRIVATE_FULL.format(
                        product_name=self.product_name,
                        product_url=self.product_url,
                        docs_url=self.docs_url,
                        license_url=self.license_url,
                    )
                )
            else:
                self.log.info(TEXT_PRIVATE_SHORT.format(product_name=self.product_name))
            return

        if self.license is None:
            if not self.server_reachable:
                self.log.info(f"License server not reachable to validate license for {self.product_name}.")
            else:

                self.log.warning(
                    TEXT_INVALID_WARNING.format(
                        license_key=self.license_key, product_name=self.product_name, message=self.message
                    )
                )
                self.log.info(
                    TEXT_INVALID.format(
                        license_key=self.license_key,
                        product_name=self.product_name,
                        message=self.message,
                        product_url=self.product_url,
                        docs_url=self.docs_url,
                    )
                )
        else:
            self.log.info(TEXT_VALID.format(product_name=self.product_name, customer=self.customer))
