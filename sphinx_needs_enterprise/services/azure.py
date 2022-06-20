from azure.devops.connection import Connection
from azure.devops.v5_1.work_item_tracking.models import Wiql
from msrest.authentication import BasicAuthentication

from sphinx_needs_enterprise.extensions.extension import ServiceExtension
from sphinx_needs_enterprise.util import dict_undefined_set

DEFAULT_FIELDS = [
    "System.Id",
    "System.WorkItemType",
    "System.Title",
    "System.State",
    "System.AreaPath",
    "System.IterationPath",
    "System.Tags",
]

DEFAULT_ORDER = "[System.ChangedDate] desc"


class AzureService(ServiceExtension):
    options = ["query", "fields", "prefix"]

    def __init__(self, app, name, config, **kwargs):
        self.app = app
        self.name = name

        # Set default values, if nothing got configured
        dict_undefined_set(config, "url", "https://dev.azure.com/YOURORG")
        dict_undefined_set(config, "query", "[System.WorkItemType] = 'Issue'")
        dict_undefined_set(config, "fields", DEFAULT_FIELDS)
        dict_undefined_set(config, "order", DEFAULT_ORDER)
        dict_undefined_set(config, "id_prefix", "AZURE_")
        dict_undefined_set(config, "content", "{{data.fields.description}}")

        # If no mapping is given, we need to use a need-type, which really exists.
        # So we take the first one from config, instead of hard-coding a value or
        # getting it from the azure issue.
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

        # Prepare AZURE client
        credentials = BasicAuthentication("", self.token)
        connection = Connection(base_url=config["url"], creds=credentials)
        self.client = connection.clients.get_work_item_tracking_client()

    def request(self, options=None):
        """
        Request data from Azure devops.

        This is not calling the REST API on its own, instead we use the azure python client.
        See: https://github.com/microsoft/azure-devops-python-api
        """

        query = options.get("query", self.config["query"])
        fields = options.get("fields", self.config["fields"])
        order = options.get("order", self.config["order"])

        wiql = self._create_wiql(query, fields, order)

        wiql_results = self.client.query_by_wiql(wiql, top=200).work_items

        cleaned_data = []
        if wiql_results:
            # The wiql_result contain references only, so we need to get the data for each item step by step... *sigh*
            for res in wiql_results:
                datum = self.client.get_work_item(int(res.id))

                # The returned datum object returns functions and other stuff, we don't need.
                # See we store only elements, which we need (but try to keep the original structure)
                cleaned_datum = {
                    "id": datum.id,
                    "rev": datum.rev,
                    "url": datum.url,
                    "fields": datum.fields,
                    "relations": datum.relations,
                }
                cleaned_data.append(cleaned_datum)

        need_data = self._extract_data(cleaned_data, options)

        return need_data

    def debug(self, options):
        debug_data = {}  # tbd
        return debug_data

    def _create_wiql(self, query=None, fields=None, order=None):

        if fields is None:
            fields = self.config["fields"]

        if order is None:
            order = self.config["order"]

        field_str = ",".join(f"[{x}]" for x in fields)
        wiql = Wiql(
            query=f"""
            select {field_str}
            from WorkItems
            where {query}
            order by {order}"""
        )

        return wiql


class InvalidConfigException(BaseException):
    pass
