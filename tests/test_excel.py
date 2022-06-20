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
