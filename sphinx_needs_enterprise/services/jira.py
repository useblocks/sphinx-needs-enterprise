from jira2markdown import convert as jira_convert
from m2r2 import convert as md_convert

from sphinx_needs_enterprise.extensions.extension import ServiceExtension
from sphinx_needs_enterprise.util import dict_undefined_set


class JiraService(ServiceExtension):
    options = ["query", "prefix"]

    def __init__(self, app, name, config, **kwargs):
        self.app = app
        self.name = name

        # Set default values, if nothing got configured
        dict_undefined_set(config, "url", "http://127.0.0.1:8080")
        dict_undefined_set(config, "query", "")
        dict_undefined_set(config, "id_prefix", "JIRA_")
        dict_undefined_set(config, "url_postfix", "/rest/api/2/search")
        dict_undefined_set(config, "content", "{{data.fields.description}}")
        dict_undefined_set(config, "convert_content", True)

        # If no mapping is given, we need to use a need-type, which really exists.
        # So we take the first one from config, instead of hard-coding a value or
        # getting it from the jira issue.
        default_need_type = str(self.app.config["needs_types"][0]["directive"])

        mappings_default = {
            "id": ["key"],
            "type": default_need_type,
            "title": ["fields", "summary"],
            "status": ["fields", "status", "name"],
        }
        dict_undefined_set(config, "mappings", mappings_default)

        mappings_replaces_default = {}
        dict_undefined_set(config, "mappings_replaces", mappings_replaces_default)

        super().__init__(config, **kwargs)

    def request(self, options=None):
        params = self._prepare_request(options)

        request_params = {
            "method": "GET",
            "url": params["url"],
            "auth": params["auth"],
            "params": {"jql": params["query"]},
        }

        answer = self._send_request(request_params)
        data = answer.json()["issues"]

        if self.config["convert_content"]:
            # We need to transform the description text format to rst, before we proceed to extract
            # the final data
            for datum in data:
                if datum["fields"]["description"] is None:
                    datum["fields"]["description"] = ""
                    continue
                try:
                    # Convert from Jira format to markdown and from markdown to rst.
                    datum["fields"]["description"] = md_convert(jira_convert(datum["fields"]["description"]))
                except KeyError:
                    pass

        need_data = self._extract_data(data, options)

        return need_data

    def debug(self, options):
        debug_data = {}  # tbd
        return debug_data


class InvalidConfigException(BaseException):
    pass
