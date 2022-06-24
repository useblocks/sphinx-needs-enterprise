import os
import time

import pytest
import requests
from requests.auth import HTTPBasicAuth
from tests.data_providers import cb_data_provider

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


def create_cb_project(project_name):
    """

    :param project_name: name as string
    :return: id of created project
    """

    # this uses v1 API
    # more info here https://codebeamer.com/cb/wiki/117612

    create_project_json = {
        "name": project_name,
        "description": "A sample project to test and demonstrate the __REST API__",
        "category": "Test",
    }

    current_projects = requests.get(url + "/projects", auth=auth).json()

    current_id = -1

    for p in current_projects:
        if p["name"] == project_name:
            current_id = p["id"]

    if current_id != -1:
        # create a clean start by deleting old project
        delete_project = requests.delete("".join([url_v1, "/project/", str(current_id)]), auth=auth)

        # break if deletion did not work
        if delete_project.status_code != 200:
            return False

    # get project info
    response = requests.post(url_v1 + "/project", json=create_project_json, auth=auth)

    if response.status_code != 201:
        return False

    else:
        return response.json()["id"]


def create_cb_sys_req(name, description):
    """

    @param name: system requirement name
    @param description: req description
    @return: tracker id under which the sys req is saved
    """

    # create project
    project_id = create_cb_project("test_project")

    # this uses v3 API
    # more info: https://codebeamer.com/cb/wiki/11375767

    if not project_id:
        raise ConnectionError

    trackers = requests.get("".join([url, "/projects/", str(project_id), "/trackers"]), auth=auth).json()

    if trackers:

        tracker_id = -1

        for x in trackers:
            # find correct tracker
            if x["name"] == "System Requirement Specifications":
                tracker_id = x["id"]
                break

        create_trackeritem_json = {
            "name": name,
            "storyPoints": 5,
            "description": description,
            "subjects": [
                {
                    "id": 1007,
                    "name": "As User, I want to have a software in my car, which is easy to use",
                    "type": "TrackerItemReference",
                }
            ],
        }

        if tracker_id != -1:
            response = requests.post(
                "".join([url, "/trackers/", str(tracker_id), "/items"]), auth=auth, json=create_trackeritem_json
            )

            assert response.status_code == 200

        else:
            pytest.fail(f"could not access codebeamer API with tracker_id: {tracker_id}")

        return tracker_id

    else:
        raise ConnectionError


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

    data_provider = cb_data_provider.cb_data_provider("./cb_input.json", "http://127.0.0.1:8080")
    # get tracker id of new sys req tracker
    project_id = data_provider.create_cb_project("testproject", "project description")

    tracker_id = data_provider.create_cb_sys_req(project_id, "testname", "this is a sysreq description")

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

    data_provider = cb_data_provider.cb_data_provider("./cb_input.json", "http://127.0.0.1:8080")
    # get tracker id of new sys req tracker
    project_id = data_provider.create_cb_project("testproject", "project description")

    tracker_id = data_provider.create_cb_sys_req(project_id, "testname", "this is a sysreq description")

    status = 200

    # cb API default user
    auth = HTTPBasicAuth("bond", "007")

    if tracker_id:
        # access newly created requirement, check if API call successful
        response = requests.get("".join([url + "/trackers/", str(tracker_id), "/items"]), auth=auth)

        assert response.status_code == status

    else:
        pytest.fail(f"could not access codebeamer API with tracker_id: {tracker_id}")
