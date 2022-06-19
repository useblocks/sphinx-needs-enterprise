# Manipulates the content to add a link to the source issue
excel_content = """
{% if info in data %}
{{data.info}}
{% else %}
{{data.description}}
{% endif %}
"""

needs_services = {
    'excel_config': {
        'start_row': 5,
        'end_row': 15,
        'end_col': 7,
        "content": excel_content,
        'id_prefix': "EXCEL_",
        'mappings': {
            "id": ["id"],
            "type": 'spec',
            "title": ["title"],
            "status": ["status"],
        },
        'extra_data': {
            "AssignedTo": ["assignee"],
            "CreatedAt": ["created at"],
            "Updated": ["updated at"],
        }
    },
    'excel_config_2': {
        'end_col': 9,
        "content": excel_content,
        'id_prefix': "EXCEL_",
        'mappings': {
            "id": ["sid"],
            "type": 'impl',
            "title": ["topic"],
            "status": ["status"],
            "links": ["links"],
        }
    }
}
