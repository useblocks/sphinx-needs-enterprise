import os
import time
import pytest
import requests
from requests.auth import HTTPBasicAuth

url = "http://127.0.0.1:8080/rest/v3"
url_v1 = "http://127.0.0.1:8080/rest"

# default user + pw
auth = requests.auth.HTTPBasicAuth("bond", "007")

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
"""
# x = requests.post(url + "/project", json=myobj, auth=auth)
y = requests.get(url + "/projects", auth=auth)
time.sleep(1)
z = requests.get(url + "/projects/3/trackers", auth=auth)
time.sleep(1)
a = requests.get(url + "/trackers/3873/items", auth=auth)

# print(x.text)
print(y.json())
print(y.status_code)
print(z.json())
print(a.json())
# b = requests.post(url + "/trackers/3873/items", json=create_project_json, auth=auth)
# c = requests.get(url + "/trackers/3873/fields", auth=auth)
# print(b.json())

# delete_project = requests.delete("".join([url_v1, "/project/", str(5)]), auth=auth)
# print(delete_project.status_code)
# print(delete_project.text)
"""


# TODO fix url selection, replace with docker_ip?

# TODO assert x in api call

# TODO test sne import export features


def create_cb_project(project_name):
    """

    :param project_name: name as string
    :return: id of created project
    """
    # this uses v1 API
    create_project_json = {
        "name": project_name,
        "description": "A sample project to test and demonstrate the __REST API__",
        "category": "Test",
    }

    # current_projects = requests.get(url + "/projects", auth=auth).json()
    current_projects = requests.get(url + "/projects", auth=auth).json()

    current_id = -1

    for p in current_projects:
        if p["name"] == project_name:
            current_id = p["id"]

    if current_id != -1:
        # create a clean start
        delete_project = requests.delete("".join([url_v1, "/project/", str(current_id)]), auth=auth)

        if delete_project.status_code != 200:
            return False

    response = requests.post(url_v1 + "/project", json=create_project_json, auth=auth)

    if response.status_code != 201:
        return False

    else:
        return response.json()["id"]


def create_cb_sys_req(name, description):
    # System Requirement Specifications < API name fo tracker
    project_id = create_cb_project("test_project")

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

        return tracker_id

    else:
        raise ConnectionError


def is_responsive(url):
    try:
        response = requests.get(url)
        print("docker response: " + str(response.status_code))
        if response.status_code == 200:
            return True
    except ConnectionError or ConnectionResetError:
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "tests/docker_files/cb_docker-compose.yml")


@pytest.fixture(scope="session")
def docker_service(docker_ip, docker_services):

    url = f"http://{docker_ip}:{8080}"

    time.sleep(30)
    docker_services.wait_until_responsive(timeout=180.0, pause=10, check=lambda: is_responsive(url))

    return url


def test_codebeamer_api():
    tracker_id = create_cb_sys_req("testname", "this is a test description")

    status = 200

    auth = requests.auth.HTTPBasicAuth("bond", "007")

    if tracker_id:
        response = requests.get("".join([url + "/trackers/", str(tracker_id), "/items"]), auth=auth)

        assert response.status_code == status

    else:
        return False
