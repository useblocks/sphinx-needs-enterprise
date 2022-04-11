import json
import os
import subprocess
import webbrowser
from datetime import datetime, timedelta

import click
import elasticsearch
import jinja2
from tqdm import tqdm

# API has changed with Sphinx-Needs version 0.7.3
try:
    from sphinxcontrib.needs.utils import NeedsList
except ImportError:
    from sphinxcontrib.needs.needsfile import NeedsList

from sphinx_needs_enterprise.scripts.loader import service_loader


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
    conf_path = os.path.abspath(conf)

    service_obj, sphinx_config = service_loader(service, conf_path)
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

    # Check needs options for new to be created needs from imported data
    needs_supported_options = [
        "tags",
        "links",
        "hide",
        "collapse",
        "layout",
        "style",
        "template",
        "pre_template",
        "post_template",
        "duration",
        "completion",
    ]  # needs options like id, status, type, title, will be created by default if not config
    if data:
        not_included_options = []
        for option in needs_supported_options:
            if option not in data[0]:
                not_included_options.append(option)
        if not_included_options:
            click.echo(
                f"Warning: new created needs from imported data will not have such needs options: {not_included_options}"
            )

    for datum in data:
        needlist.add_need(version, datum)

    click.echo("\nStoring data to json file: ", nl=False)
    needlist.write_json()
    click.echo("Done")


@cli.command(name="export")
@click.argument("service")
@click.option(
    "-j", "--json", "needs_file", default="needs.json", type=click.Path(), help="Relative path to a needs.json file"
)
@click.option("-c", "--conf", default="conf.py", type=click.Path(exists=True), help="Relative path to conf.py")
@click.option("-v", "--version", type=str, help="Version under which data shall be stored")
@click.option("-x", "--extra", multiple=True, type=click.Tuple([str, str]))
@click.option("-h", "--hours", type=int, default="0")
@click.option("-s", "--skip", type=int, default="0")
def export_cmd(service, needs_file, conf, version, extra, hours, skip):
    conf_path = os.path.abspath(conf)

    service_obj, sphinx_config = service_loader(service, conf_path)

    # Load needs.json data
    click.echo("\nReading json data: ", nl=False)
    with open(needs_file, "rb") as json_file:
        needs_data = json.load(json_file)
    click.echo("Done")

    if not version:
        version = needs_data["current_version"]
    needs = needs_data["versions"][version]["needs"]

    url = service_obj.url
    click.echo(f"Connectiong to Elasticsearch url: {url}")
    es = elasticsearch.Elasticsearch([url])

    es_index = service_obj.index
    if not es.indices.exists(index=es_index):
        click.echo(f"Creating index {es_index}")
        es.indices.create(es_index)
    else:
        click.echo(f"Using index {es_index}")

    elements = tqdm(needs.items(), bar_format="{bar:80} {percentage:3.0f}% | {desc}")
    counter = 0
    for element_index, element in enumerate(elements):
        if skip > 0:
            if element_index % skip == 0:
                continue
        key, need = element
        # click.echo(f'{key}')
        # need.pop("id", None)  # Remove id, as it is used by ElasticSearch internally
        for cus in extra:
            need[cus[0]] = cus[1]
        need["uploaded_at"] = datetime.now() + timedelta(hours=hours)
        elements.set_description(f"Uploading need {key}")
        es.index(index=es_index, document=need)
        counter += 1

    click.echo(f"Uploaded {counter} elements.")

    es.indices.refresh(index=es_index)


@cli.command()
@click.option(
    "-j", "--json", "needs_file", default="needs.json", type=click.Path(), help="Relative path to a needs.json file"
)
@click.option(
    "-t", "--template", "template_path", type=click.Path(exists=True), help="Relative path to a template file"
)
@click.option(
    "-o", "--output", "output_path", default="needs.rst", type=click.Path(), help="Relative path to output file"
)
def render(needs_file, template_path, output_path):
    if template_path is None:
        template_path = os.path.join(os.path.dirname(__file__), "../", "templates", "needs.rst.template")

    needs_file = os.path.abspath(needs_file)
    template_path = os.path.abspath(template_path)
    template_file = os.path.basename(template_path)
    template_dir = os.path.dirname(template_path)
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)

    click.echo(f"Needs file: {needs_file}")
    click.echo(f"Template file: {template_path}")
    click.echo(f"Output file: {output_path}\n")

    if not os.path.exists(needs_file):
        click.echo(f"Error: Needs file does not exist: {needs_file}")

    if not os.path.exists(template_path):
        click.echo(f"Error: Template file does not exist: {template_path}")

    # Load needs.json data
    click.echo("\nReading json data: ", nl=False)
    with open(needs_file, "rb") as json_file:
        need_data = json.load(json_file)
    click.echo("Done")

    # Render template
    click.echo("Rendering template: ", nl=False)
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(f"{template_file}".strip())

    output_data = template.render(data=need_data, now=datetime.now())

    click.echo("Done")

    # Storing data
    click.echo("Storing data: ", nl=False)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as output_fp:
        output_fp.write(output_data)

    click.echo("Done")

    click.echo("All good, we are done! 🎉")


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


if "main" in __name__:
    cli()
