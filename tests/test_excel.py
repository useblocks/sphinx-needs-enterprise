import pytest


@pytest.mark.sphinx(testroot="excel")
def test_spreadsheet(app):
    app.build()
    pass
