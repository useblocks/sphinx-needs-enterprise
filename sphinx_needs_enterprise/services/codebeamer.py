import json
import time

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
    options = ["query", "prefix", "raw", "wiki2html", "wiki2html_id", "cb_request_delay_ms"]

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
        dict_undefined_set(config, "wiki2html_id", 2)
        dict_undefined_set(config, "cb_request_delay_ms", 0)

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

        cb_request_delay_ms = options.get("cb_request_delay_ms", self.config["cb_request_delay_ms"])
        options["cb_request_delay_ms"] = cb_request_delay_ms

        wiki2html_id = options.get("wiki2html_id", self.config["wiki2html_id"])
        options["wiki2html_id"] = wiki2html_id

        params = self._prepare_request(options)

        delay = 1
        current_page = 1
        RETRY_LIMIT = 3

        request_params = {
            "method": "GET",
            "url": params["url"],
            "auth": params["auth"],
            "params": {
                "queryString": params["query"],
                "pageSize": 250,
                "page": current_page,
                "descriptionFormat": "HTML",
                "descFormat": "HTML",
            },
        }
        result = self._send_request(request_params, params["cert_abspath"])
        
        
        response_json = result.json()

        combined_objects = response_json["items"]
        print(len(combined_objects))

        retries = 0
        if result.status_code != 200:
            while retries < RETRY_LIMIT:
                print("retrying connection")
                result = self._send_request(request_params, params["cert_abspath"])
                retries += 1
                time.sleep(3)

        # check return code

        if result.status_code == 200:
            
            print("start pagination")



            total = response_json["total"]
            page_size = response_json["pageSize"]

            # there are more items than shown, request more pages
            if total > page_size:

                # minimum amount of pages needed for example if pageSize = 100 and 1000 objects
                min_pages = total // page_size

                # if page_size multiple of amount of objects, no additional query needed
                if total % page_size == 0:

                    total_page_count = min_pages

                else:
                    # one more pagination request needed to get remainder of data
                    total_page_count = min_pages + 1

                # request pages 2 - last page
                for i in range(total_page_count):
                    
                    time.sleep(delay)

                    current_page += 1
                    request_params["params"]["page"] = current_page

                    print(f"querying page {current_page}")

                    result = self._send_request(request_params, params["cert_abspath"])

                    status = result.status_code

                    retries = 0
                    
                    if status != 200:

                        while retries < RETRY_LIMIT:
                            print("retrying connection")
                            result = self._send_request(request_params, params["cert_abspath"])
                            retries += 1
                            time.sleep(3)

                        
                    response_json = result.json()

                    [combined_objects.append(item) for item in response_json["items"]]

                    print(len(combined_objects))

                    retries += 1

                    
        
        print("starting wiki2html requests")
        print(len(combined_objects))
        
        data = combined_objects
        
        """
        
        for datum in data:
            delay = cb_request_delay_ms / 1000
            if delay:
                time.sleep(delay*1.5)

            # Be sure "description" is set and valid
            if "description" not in datum or datum["description"] is None:
                datum["description"] = ""
            elif datum["descriptionFormat"] == "Wiki" and wiki2html == "True":
                # Transform the Codebeamer wiki syntax to HTML.
                # Must be done by an API request for each item.
                url = options.get("url", self.url)
                wiki2html_id = options.get("wiki2html_id", 2)

                url = url + f"/api/v3/projects/{wiki2html_id}/wiki2html"

                auth = (options.get("user", self.user), options.get("password", self.password))

                wiki2html_params = {
                    "method": "POST",
                    "url": url,
                    "auth": auth,
                    "headers": {"Content-Type": "application/json", "accept": "text/html"},
                    "data": json.dumps({"markup": datum["description"]}),
                }

                wiki2html_answer = self._send_request(wiki2html_params, params["cert_abspath"])
                datum["description"] = wiki2html_answer.text
        
        
        
        """
        

        need_data = self._extract_data(data, options)

        print(len(need_data))

        return need_data

    def debug(self, options):
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

        debug_data = {"request": request_params, "answer": answer.json()}

        return debug_data


class InvalidConfigException(BaseException):
    pass
