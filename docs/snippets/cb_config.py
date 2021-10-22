# Manipulates the content to add a link to the source issue
cb_content = """
`Codebeamer Link to Issue {{id}} <{{cb_server}}/issue/{{id}}>`_

{{description}}"""

needs_services = {
    'codebeamer_config': {
        'url': "http://127.0.0.1:8080",
        'user': 'bond',
        'password': '007',
        'prefix': "CB_IMPORT_",
        'content': cb_content,
        'query': "project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'",
        'mappings': {
            'type': "spec",
            'tags': 'cb_import, example',
            "id": ["id"],
            "status": ["status", "name"],
            "title": ["name"],
        },
        'extra_data': {
            'assignedBy': ['assignedTo', 0, 'name'],
            'createdAt': ['createdAt'],
            'updated': ['modifiedAt'],
            'type': ['typeName'],
        }
    }
}
