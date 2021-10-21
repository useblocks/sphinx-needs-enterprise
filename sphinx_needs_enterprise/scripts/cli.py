import importlib.machinery
import os
import re
import subprocess
import types
import webbrowser

import click
from sphinxcontrib.needs.utils import NeedsList

from sphinx_needs_enterprise.scripts.config import PROVIDERS


@click.group()
def cli():
    pass


@cli.command(name="import")
@click.argument("service")
@click.option("-c", "--conf", default="conf.py", type=click.Path(exists=True), help="Relative path to conf.py")
@click.option("-o", "--outdir", default=".", type=str, help="Relative path to folder for needs.json")
@click.option("-q", "--query", type=str, help="Query string")
@click.option(
    "-r", "--reuse", "old_needfile", type=click.Path(exists=True), help="Relative path to an existing needs.json file"
)
@click.option("-v", "--version", type=str, help="Version under which data shall be stored")
@click.option("-w", "--wipe", is_flag=True, default=False, help="Erases all data from reused file for used version.")
def import_cmd(service, conf, outdir, query, old_needfile, version, wipe):
    given_service = service
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
    options = {}
    if query:
        options["query"] = query
    params = service_obj._prepare_request(options)

    # Getting data
    click.echo()
    click.echo(f'URL: {params["url"]}')
    click.echo(f'Query: {params["query"]}')
    click.echo("Sending request:  ", nl=False)
    data = service_obj.request(options)
    click.echo("Done")
    click.echo(f"Retrieved {len(data)} elements")

    # Storing data
    os.makedirs(outdir, exist_ok=True)
    needlist = NeedsList(sphinx_config, outdir, ".")
    version = version or needlist.current_version
    click.echo(f"Version to use: {version}")

    if old_needfile:
        if not os.path.isabs(old_needfile):
            old_needfile = os.path.abspath(old_needfile)
        click.echo(f"Reusing needs.json: {old_needfile}")
        needlist.load_json(old_needfile)

    if wipe:
        click.echo(f"Erasing existing data for version {version}.")
        needlist.wipe_version(version)

    for datum in data:
        needlist.add_need(version, datum)

    click.echo("\nStoring data to json file: ", nl=False)
    needlist.write_json()
    click.echo("Done")


@cli.group()
def dev():
    pass


@dev.command(name="docker")
@click.argument("operation")
@click.option("-b", "--browser", is_flag=True, default=False, help="Opens a browser for each service")
def docker(operation, browser):
    """
    Starts all docker configurations delivered by Sphinx-Needs Enterprise for development.

    These are mainly containers for JIRA, CodeBeamer and more to test the different functions of
    Sphinx-Needs Enterprise.

    The OPERATION argument must be one of: start, up, stop, down.
    """
    if operation.lower() not in ["start", "up", "stop", "down"]:
        click.echo("operation must be one of: start, up, stop, down")
        return 1

    operation = operation.lower()

    click.echo("Starting all docker configurations")

    docker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "../", "docker/"))

    # Collect docker-compose files
    docker_files = []
    for element in os.listdir(docker_path):
        subelement = os.path.join(docker_path, element)
        if os.path.isdir(subelement):
            subfolder_file = os.path.join(subelement, "docker-compose.yml")
            if os.path.exists(subfolder_file):
                docker_files.append(subfolder_file)

    click.echo("Found following docker configurations:")

    args = ["docker-compose"]
    for docker_file in docker_files:
        args.append("-f")
        args.append(f"{docker_file}")
        click.echo(f" {docker_file}")
    args.append(operation)
    if operation in ["up", "start"]:
        args.append("-d")

    click.echo(f'\nExecuting {" ".join(args)}')
    os.chdir(docker_path)
    click.echo(f"CWD: {os.getcwd()}")

    subprocess.run(args)

    if browser:
        click.echo("Opening web browsers")
        for index, docker_file in enumerate(docker_files):
            url = f"127.0.0.1:{8080 + index}"
            click.echo(f"Opening {url} for {docker_file}")
            webbrowser.open(url)

    click.echo("All good, we are done! 🎉")


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
