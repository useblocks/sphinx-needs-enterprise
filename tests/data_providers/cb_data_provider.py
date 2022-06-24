import requests
from requests.auth import HTTPBasicAuth


class cb_data_provider():

    def __init__(self, input_path, cb_ip_address):

        self.file = input_path
        self.ip = cb_ip_address

        self.v1_api = "".join([self.ip, "/rest"])
        self.v3_api = "".join([self.ip, "/rest/v3"])

    @staticmethod
    def get_http_basic_auth():
        # default user + pw
        return HTTPBasicAuth("bond", "007")

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
        :return: id of created project
        """

        # this uses v1 API
        # more info here https://codebeamer.com/cb/wiki/117612

        create_project_json = {
            "name": project_name,
            "description": description,
            "category": "Test",
        }

        auth = self.get_http_basic_auth()

        current_projects = requests.get(self.v1_api + "/projects", auth=auth).json()

        current_id = -1

        for p in current_projects:
            if p["name"] == project_name:
                current_id = p["id"]

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

    def create_cb_sys_req(self, project_id, name, description):
        """

        @param project_id: project id to append to
        @param name: system requirement name
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

                if response.status_code == 200:
                    return tracker_id

            else:

                print(f"could not access codebeamer API with tracker_id: {tracker_id}")

                raise ConnectionError

        else:
            raise ConnectionError
