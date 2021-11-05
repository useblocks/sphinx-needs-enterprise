import importlib
import os
import re
import sys
import types

import click

from sphinx_needs_enterprise.config import get_providers
from sphinx_needs_enterprise.scripts.utils import get_app


def service_loader(service, conf_path):
    """
    Loads the service form a given service_name in a given conf.py file.
    """
    given_service = service
    conf_path = os.path.abspath(conf_path)

    click.echo(f"Importing config from {conf_path}")
    # Import the conf.py file as config
    loader = importlib.machinery.SourceFileLoader("conf", conf_path)
    sphinx_config = types.ModuleType(loader.name)
    loader.exec_module(sphinx_config)

    if not hasattr(sphinx_config, "needs_services"):
        click.echo("Missing needs_services in configuration")
        sys.exit(1)

    configured_services = sphinx_config.needs_services
    if given_service not in configured_services:
        click.echo(f'Unknown service: {given_service}. Available services are: {", ".join(configured_services)}')
        sys.exit(1)

    config = configured_services[given_service]

    service = None
    for name, provider in get_providers().items():
        if re.search(provider["regex"], given_service):
            service = provider["service"]
            click.echo(f'Using provider "{name}" for given service {given_service}')
            break

    if not service:
        click.echo(f"Could not find a matching service provider for {given_service}. Known providers are:")
        for name, provider in get_providers().items():
            click.echo(f'  {name} with regex {provider["regex"]}')
        sys.exit(1)

    app = get_app(sphinx_config)
    service_obj = service(app, given_service, config)

    return service_obj, sphinx_config
