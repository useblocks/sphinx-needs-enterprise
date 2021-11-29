import json

from sphinx_needs_enterprise.extensions.extension import ServiceExtension
from sphinx_needs_enterprise.util import dict_undefined_set

DEFAULT_CONTENT = """
{% set desc_list = data.description.split('\n') %}
{% if options.raw == "True"%}
.. code-block:: text
   {% for line in desc_list %}
   {{line}}
   {%- endfor %}
{% elif options.wiki2html == "True" %}
.. raw:: html
   {% for line in desc_list %}
   {{line}}
   {%- endfor %}

{% else %}
{{data.description}}
{% endif %}
"""


class CodebeamerService(ServiceExtension):
    options = ["query", "prefix", "raw", "wiki2html"]

    def __init__(self, app, name, config, **kwargs):
        self.app = app
        self.name = name

        # Set default values, if nothing got configured
        dict_undefined_set(config, "url", "http://127.0.0.1:8080")
        dict_undefined_set(config, "query", "")
        dict_undefined_set(config, "id_prefix", "CB_")
        dict_undefined_set(config, "url_postfix", "/rest/v3/items/query")
        dict_undefined_set(config, "content", DEFAULT_CONTENT)
        dict_undefined_set(config, "raw", "False")
        dict_undefined_set(config, "wiki2html", "True")

        mappings_default = {
            "id": ["id"],
            "type": ["typeName"],
            "status": ["status", "name"],
            "title": ["name"],
        }
        dict_undefined_set(config, "mappings", mappings_default)

        mappings_replaces_default = {
            r"^Task$": "task",
            r"^Requirement$": "req",
            r"^Specification$": "spec",
            r"\\\\\\\\\\r\\n": "\n\n",
        }
        dict_undefined_set(config, "mappings_replaces", mappings_replaces_default)

        super().__init__(config, **kwargs)

    def request(self, options=None):
        wiki2html = options.get("wiki2html", str(self.config["wiki2html"]))
        options["wiki2html"] = wiki2html  # Just to be sure that there is a value

        raw = options.get("raw", str(self.config["raw"]))
        options["raw"] = raw  # Just to be sure that there is a value

        params = self._prepare_request(options)

        request_params = {
            "method": "GET",
            "url": params["url"],
            "auth": params["auth"],
            "params": {
                "queryString": params["query"],
                "descriptionFormat": "HTML",
                "descFormat": "HTML",
            },
        }

        answer = self._send_request(request_params)
        data = answer.json()["items"]
        for datum in data:
            # Be sure "description" is set and valid
            if "description" not in datum or datum["description"] is None:
                datum["description"] = ""
            elif datum["descriptionFormat"] == "Wiki" and wiki2html == "True":
                # Transform the Codebeamer wiki syntax to HTML.
                # Must be done by an API request for each item.
                url = options.get("url", self.url)
                url = url + "/api/v3/projects/2/wiki2html"

                auth = (options.get("user", self.user), options.get("password", self.password))

                wiki2html_params = {
                    "method": "POST",
                    "url": url,
                    "auth": auth,
                    "headers": {"Content-Type": "application/json", "accept": "text/html"},
                    "data": json.dumps({"markup": datum["description"]}),
                }

                wiki2html_answer = self._send_request(wiki2html_params)
                datum["description"] = wiki2html_answer.text

        need_data = self._extract_data(data, options)

        return need_data


class InvalidConfigException(BaseException):
    pass
