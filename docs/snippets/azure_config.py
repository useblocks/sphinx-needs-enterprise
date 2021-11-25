import os

# Manipulates the content to add a link to the source item
azure_content = f"""
Item URL: `{{data.fields["System.TeamProject"]}}/{{data.id}} <https://dev.azure.com/useblocks/{{data.fields["System.TeamProject"]}}/_workitems/edit/{{data.id}}>`_

.. raw:: html

   {{data.fields["System.Description"]}}"""

needs_services = {
    'azure_config': {
        'url': "https://dev.azure.com/useblocks",
        'token': os.getenv('NEEDS_AZURE', ''),
        'id_prefix': "AZURE_",
        'query':  "[System.WorkItemType] = 'Issue'",
        'content': azure_content,
        'mappings': {
            "id": ["id"],
            "type": 'spec',
            "title": ["fields", "System.Title"],
            "status": ["fields", "System.State"],
        },
        'extra_data': {
            "Original Type": ["fields", 'System.WorkItemType'],
            "Original Assignee": ["fields", 'System.AssignedTo', 'displayName'],
        }
    }
}
