# Manipulates the content of a need
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
            "id": ["ID"],
            "type": 'spec',
            "title": ["TITLE"],
            "status": ["STATUS"],
        },
        'extra_data': {
            "AssignedTo": ["ASSIGNEE"],
            "CreatedAt": ["CREATED AT"],
            "Updated": ["UPDATED AT"],
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
            "status": "is_{{status}}",
            "links": ["links"],
        }
    }
}
