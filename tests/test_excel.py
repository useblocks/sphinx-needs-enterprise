import json
from pathlib import Path

import pytest
from sphinxcontrib.needs.services.manager import ServiceManager


@pytest.mark.sphinx(testroot="excel")
def test_excel(app):
    app.build()
    assert isinstance(app.needs_services, ServiceManager)

    manager = app.needs_services
    service = manager.get("excel_config")
    assert hasattr(service, "content")

    assert service.content

    html = Path(app.outdir, "index.html").read_text()

    assert "Import from Excel 2" in html
    assert "EXCEL_TEST_IMPORT_1003" in html

    assert "is_open" in html
    assert "Debug data" in html
    assert "A need imported from a spreadsheet" in html
    assert "Marco Heinemann" not in html


@pytest.mark.sphinx(testroot="excel")
def test_excel_json(app):
    app.build()
    needs_text = Path(app.outdir, "needs.json").read_text()
    needs = json.loads(needs_text)
    assert "created" in needs
    need = needs["versions"]["0.1.5"]["needs"]["EXCEL_TEST_IMPORT_1003"]

    check_keys = [
        "id",
        "type",
        "description",
        "full_title",
        "is_need",
        "is_part",
        "links",
        "status",
        "tags",
        "title",
        "type_name",
    ]

    for key in check_keys:
        if key not in need.keys():
            raise AssertionError("%s not in exported need" % key)
