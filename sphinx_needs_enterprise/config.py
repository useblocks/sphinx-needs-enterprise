def get_providers():
    from sphinx_needs_enterprise.services.codebeamer import CodebeamerService
    from sphinx_needs_enterprise.services.jira import JiraService
    from sphinx_needs_enterprise.services.azure import AzureService

    providers = {
        "jira": {"service": JiraService, "regex": "^jira"},
        "azure": {"service": AzureService, "regex": "^azure"},
        "codebeamer": {"service": CodebeamerService, "regex": "^codebeamer|^cb"},
    }
    return providers


# LICENSE
RSA_PUB_KEY = "<RSAKeyValue><Modulus>t5w/Rj4SijVJyQALRUzEJmV8Vin4P0SRCAqWSnttULrcIvkiEMhVS7OnUwUqWeRvrpDyvRy53hGHTgPIQG8pUrh0ZpX3KLRmEqBvtNEU6hOjALowi0Q/zEqYmahCh2fTb8k9FAfcMmO70TMIFfvYYGmogsmdrrCct+xEbGDM01Hhu+Go/61Jb8PpyRmZOgza5fbBC4v4rr9WF5wK6Jui7+P31bNSZDkDuxmx7dd5G+Gk2KImkRPxTZMBVQ6WmFiWFsac/KNvRskoKGlKQTaPUhpxsiPQgLnUVJPy4tzNL1qBzCXCMW3L2dgBM6W8j1kv6WbbouNbke6N+U3DIVehyQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
API_TOKEN = "WyI0MDg4MjQyIiwibmJ4Y2FWeEtmRjIrMG8xZ2szeis2NGlZU09meDk5RGFGdG1vNGJjNSJd"
PRIVATE_USAGE_FEATURE = "f1"
COMMERCIAL_USAGE_FEATURE = "f2"

