jira_content = """
{{data.fields.description}}"""

needs_services = {
    'jira_config': {
        'url': "http://127.0.0.1:8081",
        'user': 'test',
        'password': 'test',
        'id_prefix': "JIRA_",
        'query': "project = PX",
        'content': jira_content,
        'mappings': {
            "id": ["key"],
            "type": 'spec',
            "title": ["fields", "summary"],
            "status": ["fields", "status", "name"],
        },
        'extra_data': {
            "Original Type": ["fields", "issuetype", "name"],
            "Original Assignee": ["fields", "assignee", "displayName"],
        }
    }
}
