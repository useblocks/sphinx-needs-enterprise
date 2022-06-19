import pytest


@pytest.mark.sphinx(testroot="excel")
def test_excel(app):
    app.build()
    pass
