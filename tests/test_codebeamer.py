import pytest


@pytest.mark.sphinx(testroot="codebeamer")
@pytest.mark.cb_needed
def test_codebeamer(app):
    app.build()
    pass
