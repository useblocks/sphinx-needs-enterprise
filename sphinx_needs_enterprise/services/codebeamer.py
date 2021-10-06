from sphinx_needs_enterprise.extensions.extension import ServiceExtension
from sphinx_needs_enterprise.util import dict_undefined_set

from sphinx_needs_enterprise.config import CODEBEAMER_PRODUCT_ID, CODEBEAMER_PRODUCT_NAME, \
    CODEBEAMER_PRIVATE_USAGE_KEY, CODEBEAMER_PRODUCT_URL, CODEBEAMER_DOCS_URL


class CodebeamerService(ServiceExtension):
    options = ['query', 'prefix']

    def __init__(self, app, name, config, **kwargs):
        self.app = app
        self.name = name

        # Set default values, if nothing got configured
        dict_undefined_set(config, "url", "http://127.0.0.1:8080")
        dict_undefined_set(config, "id_prefix", "CB_")
        dict_undefined_set(config, "url_postfix", "/rest/v3/items/query")
        dict_undefined_set(config, "content", "{{description}}")

        mappings_default = {
            'id': ['id'],
            'type': ['typeName'],
            'status': ['status', 'name'],
            'title': ['name'],
        }
        dict_undefined_set(config, "mappings", mappings_default)

        mappings_replaces_default = {
            r'^Task$': 'task',
            r'^Requirement$': 'req',
            r'^Specification$': 'spec',
            r'\\\\\\\\\\r\\n': '\n\n'
        }
        dict_undefined_set(config, "mappings_replaces", mappings_replaces_default)

        super().__init__(config, **kwargs)

        key = config.get('license_key', CODEBEAMER_PRIVATE_USAGE_KEY)
        suppress_private_message = getattr(app.config, 'needs_is_private_project', False)
        self.set_license(CODEBEAMER_PRODUCT_ID, CODEBEAMER_PRODUCT_NAME, CODEBEAMER_PRODUCT_URL, CODEBEAMER_DOCS_URL,
                         license_key=key, suppress_private_message=suppress_private_message)
        self.check_license()

    def request(self, options=None):
        params = self._prepare_request(options)

        request_params = {
            "method": 'GET',
            "url": params['url'],
            "auth": params['auth'],
            "params": {'queryString': params["query"]},
        }

        answer = self._send_request(request_params)
        data = answer.json()['items']
        need_data = self._extract_data(data, options)

        return need_data


class InvalidConfigException(BaseException):
    pass
