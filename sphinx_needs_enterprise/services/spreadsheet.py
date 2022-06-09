import re
import os

from sphinx_needs_enterprise.extensions.extension import ServiceExtension
from sphinx_needs_enterprise.util import dict_undefined_set, get_excel_data

DEFAULT_CONTENT = """
{% set desc_list = data.description.split('\n') %}
.. raw:: html
   {% for line in desc_list %}
   {{line}}
   {%- endfor %}
"""


def allowed_file(filename):
    pattern = r"^[\w\-\/\\]+?.(xlsx)$"
    check_file = re.search(pattern, filename)
    return '.' in filename and check_file is not None


class SpreadsheetService(ServiceExtension):
    options = ["file", "start_row", "end_row", "start_col", "end_col", "header_row"]

    def __init__(self, app, name, config, **kwargs):
        self.app = app
        self.name = name

        # Set default values, if nothing got configured
        dict_undefined_set(config, "file", "")
        dict_undefined_set(config, "start_row", 2)
        dict_undefined_set(config, "start_col", 1)
        dict_undefined_set(config, "id_prefix", "EXCEL_")
        dict_undefined_set(config, "content", DEFAULT_CONTENT)
        dict_undefined_set(config, "header_row", 1)

        mappings_default = {
            "id": ["id"],
            "type": "spec",
            "status": ["status"],
            "title": ["title"],
        }
        dict_undefined_set(config, "mappings", mappings_default)

        # mappings_replaces_default = {
        #     r"^Task$": "task",
        #     r"^Requirement$": "req",
        #     r"^Specification$": "spec",
        #     r"\\\\\\\\\\r\\n": "\n\n",
        # }
        # dict_undefined_set(config, "mappings_replaces", mappings_replaces_default)

        super().__init__(config, **kwargs)

    def request(self, options=None):
        file_path = options.get("file", str(self.config["file"]))
        options["file_path"] = file_path  # Just to be sure that there is a value

        start_row = options.get("start_row", int(self.config["start_row"]))
        end_row = options.get("end_row", int(self.config["end_row"]))
        start_col = options.get("start_col", int(self.config["start_col"]))
        end_col = options.get("end_col", int(self.config["end_col"]))
        header_row = options.get("header_row", int(self.config["header_row"]))
        # Absolute path starts with /, based on the conf.py directory. The leading forward slash (/) must be striped
        spreadsheet_file_path = os.path.join(self.app.confdir, file_path.lstrip("/"))

        if not allowed_file(file_path) or len(spreadsheet_file_path) == 0:
            raise InvalidConfigException(f"Invalid Spreadsheet file specified")

        data = get_excel_data(str(spreadsheet_file_path), end_row=int(end_row), end_col=int(end_col),
                              start_row=int(start_row), start_col=int(start_col), header_row=int(header_row))
        for datum in data:
            # Be sure "description" is set and valid
            if "description" not in datum or datum["description"] is None:
                datum["description"] = ""

        need_data = self._extract_data(data, options)

        return need_data

    def debug(self, options):
        # params = self._prepare_request(options)
        # request_params = {
        #     "method": "GET",
        #     "url": params["url"],
        #     "auth": params["auth"],
        #     "params": {
        #         "queryString": params["query"],
        #         "descriptionFormat": "HTML",
        #         "descFormat": "HTML",
        #     },
        # }
        # answer = self._send_request(request_params)
        #
        # debug_data = {"request": request_params, "answer": answer.json()}
        debug_data = {}

        return debug_data


class InvalidConfigException(BaseException):
    pass
