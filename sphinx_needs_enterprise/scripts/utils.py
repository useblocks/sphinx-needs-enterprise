def get_app(sphinx_config):
    """
    Create a dummy app object, which looks like a Sphinx app and contains all needed
    information for the Services classes.

    This helps us to reuse the code from services/jira and co.
    """

    class App:
        def __init__(self):
            self.config = {
                "needs_services": sphinx_config.needs_services,
                "needs_types": getattr(sphinx_config, "needs_types", [{"directive": "req"}]),
                "needs_is_private_project": getattr(sphinx_config, "needs_is_private_project", False),
            }

    return App()
