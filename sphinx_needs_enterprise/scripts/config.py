from sphinx_needs_enterprise.services.codebeamer import CodebeamerService
from sphinx_needs_enterprise.services.jira import JiraService

PROVIDERS = {
    "jira": {"service": JiraService, "regex": "^jira"},
    "codebeamer": {"service": CodebeamerService, "regex": "^codebeamer|^cb"},
}
