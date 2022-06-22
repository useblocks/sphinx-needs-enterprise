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


@pytest.mark.sphinx(testroot="excel")
def test_excel_filter(app):
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
