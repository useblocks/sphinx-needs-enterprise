import importlib.machinery
import os
import re
import types

import click
from sphinxcontrib.needs.utils import NeedsList

from sphinx_needs_enterprise.scripts.config import PROVIDERS


@click.group()
def cli():
    pass


@cli.command(name="import")
@click.argument("given_service")
@click.option("-c", "--conf", default="conf.py", type=click.Path(exists=True), help="Relative path to conf.py")
@click.option("-o", "--outdir", default=".", type=str, help="Relative path to folder for needs.json")
def import_cmd(given_service, conf, outdir):
    conf_path = os.path.abspath(conf)

    click.echo(f"Importing config from {conf_path}")
    # Import the conf.py file as config
    loader = importlib.machinery.SourceFileLoader("conf", conf_path)
    sphinx_config = types.ModuleType(loader.name)
    loader.exec_module(sphinx_config)

    if not hasattr(sphinx_config, "needs_services"):
        click.echo("Missing needs_services in configuration")
        return 1

    configured_services = sphinx_config.needs_services
    if given_service not in configured_services:
        click.echo(f'Unknown service: {given_service}. Available services are: {", ".join(configured_services)}')
        return 1
    config = configured_services[given_service]

    service = None
    for name, provider in PROVIDERS.items():
        if re.search(provider["regex"], given_service):
            service = provider["service"]
            click.echo(f'Using provider "{name}" for given service {given_service}')
            break

    if not service:
        click.echo(f"Could not find a matching service provider for {given_service}. Known providers are:")
        for name, provider in PROVIDERS.items():
            click.echo(f'  {name} with regex {provider["regex"]}')
        return 1

    app = get_app(sphinx_config)
    service_obj = service(app, given_service, config)
    params = service_obj._prepare_request({})

    # Getting data
    click.echo()
    click.echo(f'URL: {params["url"]}')
    click.echo(f'Query: {params["query"]}')
    click.echo("Sending request:  ", nl=False)
    data = service_obj.request()
    click.echo("Done")
    click.echo(f"Retrieved {len(data)} elements")

    # Storing data
    click.echo("\nStoring data to json file: ", nl=False)
    os.makedirs(outdir, exist_ok=True)
    needlist = NeedsList(sphinx_config, outdir, ".")
    for datum in data:
        needlist.add_need(needlist.current_version, datum)

    needlist.write_json()
    click.echo("Done")


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


if "main" in __name__:
    cli()
