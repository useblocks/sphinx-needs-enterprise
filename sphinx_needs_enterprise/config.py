def get_providers():
    from sphinx_needs_enterprise.services.azure import AzureService
    from sphinx_needs_enterprise.services.codebeamer import CodebeamerService
    from sphinx_needs_enterprise.services.elasticsearch import ElasticsearchService
    from sphinx_needs_enterprise.services.excel import ExcelService
    from sphinx_needs_enterprise.services.jira import JiraService

    providers = {
        "jira": {"service": JiraService, "regex": "^jira"},
        "azure": {"service": AzureService, "regex": "^azure"},
        "codebeamer": {"service": CodebeamerService, "regex": "^codebeamer|^cb"},
        "elasticsearch": {"service": ElasticsearchService, "regex": "^elastic|^es"},
        "excel": {"service": ExcelService, "regex": "^excel"}
    }
    return providers


# LICENSE
RSA_PUB_KEY = "<RSAKeyValue><Modulus>t5w/Rj4SijVJyQALRUzEJmV8Vin4P0SRCAqWSnttULrcIvkiEMhVS7OnUwUqWeRvrpDyvRy53hGHTgPIQ" \
              "G8pUrh0ZpX3KLRmEqBvtNEU6hOjALowi0Q/zEqYmahCh2fTb8k9FAfcMmO70TMIFfvYYGmogsmdrrCct+xEbGDM01Hhu+Go/61Jb8Pp" \
              "yRmZOgza5fbBC4v4rr9WF5wK6Jui7+P31bNSZDkDuxmx7dd5G+Gk2KImkRPxTZMBVQ6WmFiWFsac/KNvRskoKGlKQTaPUhpxsiPQgLn" \
              "UVJPy4tzNL1qBzCXCMW3L2dgBM6W8j1kv6WbbouNbke6N+U3DIVehyQ==" \
              "</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
API_TOKEN = "WyI0MDg4MjQyIiwibmJ4Y2FWeEtmRjIrMG8xZ2szeis2NGlZU09meDk5RGFGdG1vNGJjNSJd"

SNE_PRODUCT_ID = 13000
SNE_PRODUCT_NAME = "Sphinx-Needs Enterprise"
SNE_PRODUCT_URL = "https://sphinx-needs.com"
SNE_DOCS_URL = "https://useblocks.com/sphinx-needs-enterprise"
SNE_LICENSE_URL = "http://useblocks.com/sphinx-needs-enterprise/license.html"

LICENSE_RETRIES = 3
LICENSE_RETRY_SECS = 5
LICENSE_INTERVAL_SECS = 300

# TEXT MESSAGES
TEXT_PRIVATE_FULL = """
* Sphinx-Needs Enterprise License Information ************************************************
* No commercial license configured!
* This allows the free usage of {product_name} for private Sphinx projects
* of any size.
* If this is a academic or commercial project, please obtain a license under
* {product_url}.
* You can hide this message by setting "needs_enterprise_license = "PRIVATE"
* or by setting a valid commercial license.
* For technical support visit {docs_url}.
* For license information visit {license_url}.
***********************************************************************************************\n"""

TEXT_PRIVATE_SHORT = "Using {product_name} for private projects."

TEXT_INVALID = """
* Sphinx-Needs Enterprise License Information ************************************************
* Provided license '{license_key}' for extension {product_name} not valid.
* Reason: {message}
* Remove the license from configuration to activate the private usage.
* To obtain a valid license: {product_url}.
* For technical details please visit {docs_url}
***********************************************************************************************
"""
TEXT_INVALID_WARNING = """
Provided license "{license_key}" for extension {product_name} not valid.
Reason: {message}
"""

TEXT_VALID = "Commercial license for {product_name} by {customer} validated."
