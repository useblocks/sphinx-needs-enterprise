import re

from sphinx_needs_enterprise.config import get_providers


def setup(app):
    # Register sphinx-needs stuff after it has been initialised.
    app.connect("env-before-read-docs", prepare_env)


def prepare_env(app, env, _docname):
    for service in getattr(app.config, "needs_services", {}).keys():
        for name, provider in get_providers().items():
            if re.search(provider["regex"], service):
                service_provider_class = provider["service"]
                app.needs_services.register(service, service_provider_class)
                break  # check next configured service

    # app.needs_services.register("azure", AzureService)
    # app.needs_services.register("codebeamer", CodebeamerService)
    # app.needs_services.register("jira", JiraService)
