from licensing.methods import Helpers, Key
from sphinx.util import logging

from sphinx_needs_enterprise.config import (
    API_TOKEN,
    COMMERCIAL_USAGE_FEATURE,
    PRIVATE_USAGE_FEATURE,
    RSA_PUB_KEY,
)


class License:
    def __init__(
        self,
        product_id,
        product_name,
        license_key,
        product_url=None,
        docs_url=None,
        suppress_private_message=False,
        private_feature=PRIVATE_USAGE_FEATURE,
        commercial_feature=COMMERCIAL_USAGE_FEATURE,
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
        self.license_key = license_key
        self.private_feature = private_feature
        self.commercial_feature = commercial_feature
        self.suppress_private_message = suppress_private_message

        self.valid = None
        self.activated = False
        self.is_private = None
        self.is_commercial = None
        self.customer = None
        self.server_reachable = None

    def check(self, own_output=False):
        """
        Checks and activates a given key.
        This function should be used as early as possible.

        Set "own_output" to True to let the extension print all the needed output to inform the user about the
        license status. Otherwise some common information will be printed, if license check fails.

        :param own_output: Flag, if True no output will be printed.
        :return: True, if license is valid and available, else false.
        """
        license, message = Key.activate(
            token=self.token,
            rsa_pub_key=self.rsa_pub_key,
            product_id=self.product_id,
            key=self.license_key,
            machine_code=Helpers.GetMachineCode(),
        )

        self.server_reachable = True
        if "Could not contact the server" in message:
            self.server_reachable = False

        if license is None:
            self.valid = False
            if not own_output:
                if not self.server_reachable:
                    self.log(f"License server not reachable to validate license for {self.product_name}.")
                else:
                    self.log.warning(
                        f'Provided license "{self.license_key}" for extension {self.product_name} not valid.'
                    )
                    self.log.info(
                        f"Remove the license from configuration to activate the private usage."
                        f"\nTo obtain a valid license: {self.product_url}."
                        f"\nFor technical details please visit {self.docs_url}"
                    )

                self.log.debug(message)
        else:
            self.valid = True
            self.activated = True
            self.is_private = getattr(license, self.private_feature, False)
            self.is_commercial = getattr(license, self.commercial_feature, False)

            self.customer = f"{license.customer['Name']} ({license.customer['CompanyName']})"

            if not own_output:
                if self.is_private:
                    self.log.info(f"Private license for {self.product_name} detected.")
                    if not self.suppress_private_message:
                        self.log.info(
                            f"*************************************************************************\n"
                            f"This allows the private usage of {self.product_name} for Sphinx projects "
                            f"of any size.\n"
                            f"If this is a academic or commercial project, please obtain a license under "
                            f"\n{self.product_url}."
                            f'\nYou can hide this message by setting "needs_is_private_project = True"'
                            f"sFor technical support visit f{self.docs_url}."
                            f"\n*************************************************************************\n"
                        )
                    self.log.debug(f"Provided license {self.license_key} is valid.")

                # The license is also a valid license, as long as it does not have the is_private flag configured.
                if self.is_commercial or not self.is_private:
                    self.log.info(f"Commercial license of {self.product_name} for {self.customer} detected.")

        return self.valid, self.server_reachable
