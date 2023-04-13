import time

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

        current_page = 1
        retry_limit = 3

        params = self._prepare_request(options)

        # according to Jira docs password auth is deprecated
        # https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/

        request_params = {
            "method": "GET",
            "url": params["url"],
            "auth": params["auth"],
            "params": {
                "jql": params["query"],
                "maxResults": 400,
                "fields": "id,key,description,status,summary,issuetype,assignee",
            },
        }

        result = self._send_request(request_params)

        response_json = result.json()

        combined_objects = response_json["issues"]
        print(len(combined_objects))

        if result.status_code == 200:

            print("start pagination")

            total = response_json["total"]
            page_size = response_json["maxResults"]

            print(f"There are {total} elements")
            print(f"pagesize is {page_size}")

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

                print(f"requesting {total_page_count} pages")

                # request pages 2 - last page
                for i in range(total_page_count):

                    time.sleep(0.33)

                    current_page += 1
                    request_params["params"]["page"] = current_page

                    print(f"querying page {current_page}")

                    result = self._send_request(request_params)

                    status = result.status_code

                    retries = 0

                    if status != 200:

                        while retries < retry_limit:
                            print("retrying connection")
                            result = self._send_request(request_params)
                            retries += 1
                            time.sleep(3)

                    response_json = result.json()

                    [combined_objects.append(item) for item in response_json["issues"]]

                    print(len(combined_objects))

                    retries += 1

        data = combined_objects

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
