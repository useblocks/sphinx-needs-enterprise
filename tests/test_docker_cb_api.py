import json
import os
import pathlib
import time
from pathlib import Path

import pytest
import requests
from requests.auth import HTTPBasicAuth

from tests.data_providers.cb_data_provider import CbDataProvider

url = "http://127.0.0.1:8080/rest/v3"
url_v1 = "http://127.0.0.1:8080/rest"

# default user + pw
auth = HTTPBasicAuth("bond", "007")

create_project_json = {
    "name": "Implement car software",
    "storyPoints": 5,
    "description": "asdasd",
    "subjects": [
        {
            "id": 1007,
            "name": "As User, I want to have a software in my car, which is easy to use",
            "type": "TrackerItemReference",
        }
    ],
}

# TODO test sne import export features


def is_responsive(url):
    """
    waits until and url returns status code 200
    @param url: url
    @return: False if url not reachable
    """
    try:
        response = requests.get(url)
        print("docker response: " + str(response.status_code))
        if response.status_code == 200:
            return True
    except ConnectionError or ConnectionResetError:
        return False


@pytest.fixture(scope="session")
def docker_service(docker_ip, docker_services):
    """
    pytest-docker service
    @param docker_ip:
    @param docker_services:
    @return:
    """
    url = f"http://{docker_ip}:{8080}"

    time.sleep(30)
    docker_services.wait_until_responsive(timeout=180.0, pause=10, check=lambda: is_responsive(url))

    return url


@pytest.mark.cb_docker_needed
@pytest.mark.external_resource
@pytest.mark.ci_test
def test_codebeamer_api_in_ci():
    """
    testcase for GitHub CI. This requires a running cb docker container.
    assumes codebeamer docker instance is running on 127.0.0.1:8080
    @return:
    """
    # detect if we are in GitHub CI environment, fail test if we are not. This should only be executed on GH
    try:
        in_gh_ci = os.getenv("CI")

        if not in_gh_ci or in_gh_ci is None:
            raise NameError

    except NameError:
        pytest.fail(
            "Please add pytest marker filtering to your Configuration. " "For local testing use 'pytest -m local'"
        )

    data_provider = CbDataProvider("./cb_input.json", "http://127.0.0.1:8080")
    # get tracker id of new sys req tracker
    project_id = data_provider.create_cb_project("testproject", "project description")

    tracker_id = data_provider.create_cb_item(
        project_id, "System Requirement Specifications", "testname", "this is a sysreq description", 4321
    )

    status = 200

    auth = HTTPBasicAuth("bond", "007")

    if tracker_id:
        # access newly created requirement, check if API call successful
        response = requests.get("".join([url + "/trackers/", str(tracker_id), "/items"]), auth=auth)

        assert response.status_code == status

    else:
        pytest.fail(f"could not access codebeamer API with tracker_id: {tracker_id}")


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """
    specifies custom docker-compose file for pytest-docker
    @param pytestconfig:
    @return: path to file
    """
    return os.path.join(str(pytestconfig.rootdir), "tests/docker_files/cb_docker-compose.yml")


@pytest.mark.cb_docker_needed
@pytest.mark.external_resource
@pytest.mark.local
def test_codebeamer_api(docker_service):
    """
    testcase for local running, this spins up a docker container from a file specified in docker_compose_file
    if not previously run may take some time to download the containers.

    @param docker_service: pytest-docker fixture
    @return:
    """

    data_provider = CbDataProvider("./cb_input.json", "http://127.0.0.1:8080")
    # get tracker id of new sys req tracker
    project_id = data_provider.create_cb_project("testproject", "project description")

    tracker_id = data_provider.create_cb_item(
        project_id, "System Requirement Specifications", "testname", "this is a sysreq description", 4321
    )

    status = 200

    # cb API default user
    auth = HTTPBasicAuth("bond", "007")

    if tracker_id:
        # access newly created requirement, check if API call successful
        response = requests.get("".join([url + "/trackers/", str(tracker_id), "/items"]), auth=auth)

        assert response.status_code == status

    else:
        pytest.fail(f"could not access codebeamer API with tracker_id: {tracker_id}")


@pytest.mark.cb_docker_needed
@pytest.mark.external_resource
@pytest.mark.local
def test_cb_input(docker_service):
    data_provider = CbDataProvider("./cb_input.json", "http://127.0.0.1:8080")

    input_filepath = data_provider.generate_input()

    data_structure_from_input = data_provider.generate_data_from_input(input_filepath)

    with open(input_filepath, "r") as infile:

        # get wanted structure
        json_input = json.loads(infile.read())

        project_count = 0

        for x in json_input["projects"]:
            if len(x) > 0:
                project_count += 1

        assert len(data_structure_from_input) == project_count


@pytest.mark.cb_docker_needed
@pytest.mark.external_resource
@pytest.mark.local
@pytest.mark.sphinx(testroot="cb-directive")
def test_codebeamer_needservice(app, docker_service):

    file_abs_path = pathlib.Path(__file__).parent.absolute()

    data_provider = CbDataProvider(file_abs_path.joinpath("./data_providers/cb_input.json"), "http://127.0.0.1:8080")
    input_filepath = data_provider.generate_input()

    data_provider.generate_data_from_input(input_filepath)

    app.build()

    srcdir = Path(app.srcdir)
    out_dir = srcdir / "_build/html"

    # test if constraints_results / constraints_passed is properly set
    html = Path(out_dir, "index.html").read_text()

    assert "test_sysreq" in html
    assert "bug description test 1234" in html

    assert "cb_import" in html


@pytest.mark.cb_docker_needed
@pytest.mark.external_resource
@pytest.mark.ci_test
@pytest.mark.sphinx(testroot="cb-directive")
def test_ci_codebeamer_needservice(app):

    file_abs_path = pathlib.Path(__file__).parent.absolute()

    data_provider = CbDataProvider(file_abs_path.joinpath("./data_providers/cb_input.json"), "http://127.0.0.1:8080")
    input_filepath = data_provider.generate_input()

    data_provider.generate_data_from_input(input_filepath)

    app.build()

    srcdir = Path(app.srcdir)
    out_dir = srcdir / "_build/html"

    # test if constraints_results / constraints_passed is properly set
    html = Path(out_dir, "index.html").read_text()

    assert "test_sysreq" in html
    assert "bug description test 1234" in html

    assert "cb_import" in html


@pytest.mark.external_resource
@pytest.mark.ci_test
def test_empty():

    assert 1 == 1
