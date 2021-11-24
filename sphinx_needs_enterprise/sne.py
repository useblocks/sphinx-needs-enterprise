import re

from sphinx_needs_enterprise.config import (
    SNE_DOCS_URL,
    SNE_LICENSE_URL,
    SNE_PRODUCT_ID,
    SNE_PRODUCT_NAME,
    SNE_PRODUCT_URL,
    get_providers,
)
from sphinx_needs_enterprise.license import License
from sphinx_needs_enterprise.version import VERSION


def setup(app):
    app.add_config_value("needs_enterprise_license", "", "html", types=[str])
    # Register sphinx-needs stuff after it has been initialised.
    app.connect("env-before-read-docs", prepare_env)
    app.connect("source-read", process_per_doc)
    app.connect("doctree-resolved", process_per_doc)
    app.connect("build-finished", process_finish)

    return {
        "version": VERSION,  # identifies the version of our extension
        "parallel_read_safe": True,  # support parallel modes
        "parallel_write_safe": True,
    }


def prepare_env(app, env, _docname):
    license_key = getattr(app.config, "needs_enterprise_license", "")
    if license_key.upper() == "PRIVATE":
        suppress_private_message = True
    else:
        suppress_private_message = False

    sne_license = License(
        SNE_PRODUCT_ID,
        SNE_PRODUCT_NAME,
        license_key,
        SNE_PRODUCT_URL,
        SNE_DOCS_URL,
        SNE_LICENSE_URL,
        suppress_private_message,
    )

    env.needs_sne_license = sne_license

    env.needs_sne_license.check()
    env.needs_sne_license.print_info()

    for service in getattr(app.config, "needs_services", {}).keys():
        for name, provider in get_providers().items():
            if re.search(provider["regex"], service):
                service_provider_class = provider["service"]
                app.needs_services.register(service, service_provider_class)
                break  # check next configured service


def process_per_doc(app, *kwargs):
    """
    Check the license everytime a new rst-file is read or get written.
    The license internal logic cares about not requesting information
    from license server too often.
    """
    sne_license = app.env.needs_sne_license
    sne_license.check()


def process_finish(app, exception):
    """
    Finally check/print again license after everything was done
    """
    # There are use cases, where needs_sne_license was not set up. (e.g. no files to build or prior error)
    if hasattr(app.env, "needs_sne_license"):
        app.env.needs_sne_license.print_info()
        app.env.needs_sne_license.free()  # Give back license
