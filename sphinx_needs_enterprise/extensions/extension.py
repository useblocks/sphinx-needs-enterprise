import re

import requests
from jinja2 import Template
from sphinxcontrib.needs.services.base import BaseService

from sphinx_needs_enterprise.exceptions import (
    CommunicationException,
    InvalidConfigException,
    LicenseException,
)
from sphinx_needs_enterprise.license import License
from sphinx_needs_enterprise.util import dict_get


class ServiceExtension(BaseService):
    def __init__(
        self,
        config,
        url=None,
        url_postfix=None,
        query="",
        query_postfix="",
        user="",
        password="",
        token="",
        id_prefix="",
        content=None,
        mappings=None,
        mappings_replaces=None,
        extra_data=None,
        **kwargs,
    ):

        self.config = config

        self.url = url or config.get("url", "")
        self.url_postfix = url_postfix or config.get("url_postfix", "")

        self.query = query or config.get("query", "")
        self.query_postfix = query_postfix or config.get("query_postfix", "")

        self.user = user or config.get("user", "")
        self.password = password or config.get("password", "")
        self.token = token or config.get("token", "")

        self.id_prefix = id_prefix or config.get("id_prefix", "")

        self.content = content or config.get("content", "")

        self.mappings = mappings or config.get("mappings", {})
        self.mapping_replaces = mappings_replaces or config.get("mappings_replaces", {})
        self.extra_data = extra_data or config.get("extra_data", {})

        self.license_key = None
        self.product_id = None
        self.product_name = None
        self.license = None

        super().__init__(**kwargs)

    def set_license(
        self,
        product_id,
        product_name,
        product_url,
        docs_url,
        license_key=None,
        private_feature="f1",
        commercial_feature="f2",
        suppress_private_message=False,
    ):
        key = license_key or self.config.get("license_key", None)
        if key is None:
            raise LicenseException("No license key provided.")

        self.license_key = key
        self.product_id = product_id
        self.product_name = product_name
        self.product_url = product_url
        self.docs_url = docs_url
        self.suppress_private_message = suppress_private_message

        self.license = License(
            self.product_id,
            self.product_name,
            self.license_key,
            product_url=product_url,
            docs_url=docs_url,
            suppress_private_message=suppress_private_message,
        )

    def check_license(self):
        if self.license is None:
            raise LicenseException(
                'License not defined. User "set_license" to activate license ' "support for the Sphinx-Needs extension."
            )

        self.license.check()

    def _prepare_request(self, options):
        if options is None:
            options = {}
        url = options.get("url", self.url)
        url = url + self.url_postfix

        auth = (options.get("user", self.user), options.get("password", self.password))
        query = options.get("query", self.query)
        query = query + self.query_postfix

        request = {"url": url, "auth": auth, "query": query, "params": {}}
        return request

    def _send_request(self, request):
        """
        Sends the final request.

        ``request`` must be a dictionary, which contains data valid to the requests-lib.
        This request-data gets mostly defined by using ``prepare_request``.

        :param request: dict
        :return: request answer
        """

        # params = {
        #     'queryString': query
        # }

        result = requests.request(**request)
        if result.status_code >= 300:
            raise CommunicationException(f"Problems accessing {result.url}.\nReason: {result.text}")

        return result

    def _extract_data(self, data, options):
        """
        Extract data of a list/dictionary, which was retrieved via send_request.

        :param data: list or dict
        :param options: dict of set directive options
        :return: list of need-data
        """

        need_data = []
        if options is None:
            options = {}
        for item in data:
            extra_data = {}
            for name, selector in self.extra_data.items():
                if not (isinstance(selector, tuple) or isinstance(selector, list) or isinstance(selector, str)):
                    raise InvalidConfigException(
                        f"Given selector for {name} of extra_data must be a list or tuple. "
                        f'Got {type(selector)} with value "{selector}"'
                    )
                if isinstance(selector, str):
                    # Set the "hard-coded" string as value
                    extra_data[name] = selector
                else:
                    extra_data[name] = dict_get(item, selector)

            for regex, new_str in self.mapping_replaces.items():
                self.content = re.sub(regex, new_str, self.content)
            content_template = Template(self.content)
            context = {"data": item, "options": options}
            content = content_template.render(context)
            content += "\n\n| \n"  # Add enough space between content and extra_data

            # Add extra_data to content
            for key, value in extra_data.items():
                content += f"\n| **{key}**: {value}"
            content += "\n"

            prefix = options.get("prefix", self.id_prefix)

            need_values = {}
            for name, selector in self.mappings.items():
                if not (isinstance(selector, tuple) or isinstance(selector, list) or isinstance(selector, str)):
                    raise InvalidConfigException(
                        f"Given selector for {name} of mapping must be a list or tuple. "
                        f'Got {type(selector)} with value "{selector}"'
                    )
                if isinstance(selector, str):
                    # Set the "hard-coded" string as value
                    need_values[name] = selector
                else:
                    need_values[name] = str(dict_get(item, selector))

                for regex, new_str in self.mapping_replaces.items():
                    need_values[name] = re.sub(regex, new_str, need_values[name])

                if name == "id":
                    need_values[name] = prefix + need_values[name]

            finale_data = {"content": content}
            finale_data.update(need_values)

            need_data.append(finale_data)
        return need_data
