import pytest


@pytest.mark.sphinx(testroot="spreadsheet")
def test_spreadsheet(app):
    app.build()
    pass
