import pytest


@pytest.mark.sphinx(testroot="codebeamer")
def test_codebeamer(app):
    app.build()
