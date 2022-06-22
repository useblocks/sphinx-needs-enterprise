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

    assert "Import from Excel 19" in html
    assert "EXCEL_TEST_IMPORT_1019" in html

    assert "is_progress" in html
    assert "Debug data" in html
    assert "A need imported from a spreadsheet" in html
    assert "Haiyang Zhang" in html


@pytest.mark.sphinx(testroot="excel-incorrect")
def test_excel_incorrect_filter_statement(app):
    with pytest.raises(ReferenceError):
        app.build()
        assert isinstance(app.needs_services, ServiceManager)

        manager = app.needs_services
        service = manager.get("excel_config")
        assert hasattr(service, "content")
        assert service.content


@pytest.mark.sphinx(testroot="excel")
def test_excel_correct_filter_statement(app):
    app.build()
    assert isinstance(app.needs_services, ServiceManager)

    manager = app.needs_services
    service = manager.get("excel_config")
    assert hasattr(service, "content")
    assert service.content

    html = Path(app.outdir, "index.html").read_text()

    assert "Import from Excel 16" in html
    assert "EXCEL_TEST_IMPORT_1016" in html

    assert "A need imported from a spreadsheet" in html
    assert "is_progress" in html
    assert "Marco Heinemann" in html


@pytest.mark.sphinx(testroot="excel")
def test_excel_json(app):
    app.build()
    needs_text = Path(app.outdir, "needs.json").read_text()
    needs = json.loads(needs_text)
    assert "created" in needs
    need = needs["versions"]["0.1.5"]["needs"]["EXCEL_TEST_IMPORT_1019"]

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
