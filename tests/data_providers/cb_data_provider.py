import json
import os.path
import time

import requests
from requests.auth import HTTPBasicAuth


class CbDataProvider:
    def __init__(self, input_path, cb_ip_address):

        self.file = input_path
        self.ip = cb_ip_address

        self.v1_api = "".join([self.ip, "/rest"])
        self.v3_api = "".join([self.ip, "/rest/v3"])

    @staticmethod
    def get_http_basic_auth():
        # default user + pw
        return HTTPBasicAuth("bond", "007")

    def generate_input(self):
        """

        generates cb_input.json

        Tracker names in codebeamer

        Contacts
        Releases
        User Stories
        Risks
        Teams
        Customer Requirement Specifications
        System Requirement Specifications
        Change Requests
        Bugs
        Tasks
        Test Cases
        Test Sets
        Test Configurations
        Test Runs
        Timekeeping

        @return: abs path where to find the json file
        """

        input_json = {
            "projects": {
                "testproject": {
                    "project_description": "project description test",
                    "Contacts": [],
                    "Releases": [],
                    "User": [],
                    "Stories": [],
                    "Risks": [],
                    "Teams": [],
                    "Customer Requirement Specifications": [],
                    "System Requirement Specifications": [{"name": "test_sysreq", "description": "sysreq test descr"}],
                    "Change": [],
                    "Requests": [],
                    "Bugs": [],
                    "Tasks": [],
                    "Test Cases": [],
                    "Test Sets": [],
                    "Test Configurations": [],
                    "Test Runs": [],
                    "Timekeeping": [],
                },
                "testproject_2": {
                    "project_description": "project description test",
                    "Contacts": [],
                    "Releases": [],
                    "User": [],
                    "Stories": [],
                    "Risks": [],
                    "Teams": [],
                    "Customer Requirement Specifications": [],
                    "System Requirement Specifications": [],
                    "Change": [],
                    "Requests": [],
                    "Bugs": [{"name": "test_bug", "description": "bug description test 1234"}],
                    "Tasks": [],
                    "Test Cases": [],
                    "Test Sets": [],
                    "Test Configurations": [],
                    "Test Runs": [],
                    "Timekeeping": [],
                },
            }
        }

        with open(self.file, "w+") as cb_input:
            cb_input.write(json.dumps(input_json, indent=2))

            return os.path.abspath(self.file)

    def delete_all_projects(self):

        # get projects
        # use v1 to delete projects

        # this uses v1 API
        # more info here https://codebeamer.com/cb/wiki/117612
        auth = self.get_http_basic_auth()

        current_projects = requests.get(self.v1_api + "/projects", auth=auth).json()

        for p in current_projects:

            # create a clean start by deleting old project
            delete_project = requests.delete("".join([self.v1_api, "/project/", str(p["id"])]), auth=auth)

            # break if deletion did not work
            if delete_project.status_code != 200:
                return False

        projects_after_del = requests.get(self.v1_api + "/projects", auth=auth).json()

        if len(projects_after_del) == 0:
            return True

        else:
            return False

    def create_cb_project(self, project_name, description):
        """

        :param project_name: name as string
        @param description: project description
        :return: id of created project or False if something has failed
        """

        # this uses v1 API
        # more info here https://codebeamer.com/cb/wiki/117612

        create_project_json = {
            "name": project_name,
            "description": description,
            "category": "Test",
        }

        auth = self.get_http_basic_auth()

        current_projects_response = requests.get(self.v1_api + "/projects", auth=auth)
        current_projects = current_projects_response.json()
        current_id = -1

        for p in current_projects:
            if p["name"] == project_name:
                current_id = p["uri"].split("/")[-1]
                break

        if current_id != -1:
            # create a clean start by deleting old project
            delete_project = requests.delete("".join([self.v1_api, "/project/", str(current_id)]), auth=auth)

            # break if deletion did not work
            if delete_project.status_code != 200:
                return False

        # get project info
        response = requests.post(self.v1_api + "/project", json=create_project_json, auth=auth)

        if response.status_code != 201:
            return False

        else:
            return response.json()["id"]

    def create_cb_item(self, project_id, tracker_name, item_name, item_description, item_id):
        """

        @param project_id: project id to append to
        @param tracker_name: tracker name
        @param description: req description
        @return: tracker id under which the sys req is saved
        """

        auth = self.get_http_basic_auth()

        url = self.v3_api
        # create project

        # this uses v3 API
        # more info: https://codebeamer.com/cb/wiki/11375767

        if not project_id:
            raise ConnectionError

        trackers = requests.get("".join([url, "/projects/", str(project_id), "/trackers"]), auth=auth).json()

        if trackers:

            tracker_id = -1

            for x in trackers:
                # find correct tracker
                if x["name"] == tracker_name:
                    tracker_id = x["id"]
                    break

            create_trackeritem_json = {
                "name": item_name,
                "storyPoints": 5,
                "description": item_description,
                "subjects": [
                    {
                        "id": item_id,
                        "name": "As User, I want to have a software in my car, which is easy to use",
                        "type": "TrackerItemReference",
                    }
                ],
            }

            # continue if correct tracker is present
            if tracker_id != -1:

                # create item in tracker
                response = requests.post(
                    "".join([url, "/trackers/", str(tracker_id), "/items"]), auth=auth, json=create_trackeritem_json
                )

                if response.status_code == 200:
                    return tracker_id

            else:

                print(f"could not access codebeamer API with tracker_id: {tracker_id}")

                raise ConnectionError

        else:
            raise ConnectionError

    def generate_data_from_input(self, input_filepath):
        """

        @param input_filepath: abs filepath to an inpu json file. see generate_input()
        @return: dict showing the data structure that was created
        """
        with open(input_filepath) as input_file:

            json_input = json.loads(input_file.read())

            data_structure = {}

            item_id = 1234

            for project in json_input["projects"].keys():

                data = json_input["projects"][project]

                data_structure[project] = {}
                data_structure[project]["id"] = None

                data_structure[project]["items"] = {}
                data_structure[project]["items"]["id"] = None

                # create each project
                project_id = self.create_cb_project(project, data["project_description"])

                if project_id:
                    data_structure[project]["id"] = project_id

                    # create items in correct tracker
                    for tracker_name, items in data.items():
                        if isinstance(items, str):
                            continue

                        for item in items:

                            response_tracker_id = self.create_cb_item(
                                project_id, tracker_name, item["name"], item["description"], item_id
                            )

                            if response_tracker_id:
                                item_id += 1
                                data_structure[project]["items"]["id"] = response_tracker_id

                            else:
                                data_structure["projects"][project]["items"]["id"] = False

                            time.sleep(1)

                # getting 429 Too many requests Error
                time.sleep(1)

        return data_structure
