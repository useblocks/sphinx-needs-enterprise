from sphinx_needs_enterprise.services.azure import AzureService
from sphinx_needs_enterprise.services.codebeamer import CodebeamerService
from sphinx_needs_enterprise.services.jira import JiraService


def setup(app):
    # Register sphinx-needs stuff after it has been initialised.
    app.connect("env-before-read-docs", prepare_env)


def prepare_env(app, env, _docname):
    app.needs_services.register("azure", AzureService)
    app.needs_services.register("codebeamer", CodebeamerService)
    app.needs_services.register("jira", JiraService)
