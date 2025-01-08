from typing import Any
import requests
import os
from dotenv import load_dotenv


class ClickupUtils:
    def __init__(self):
        load_dotenv()

        self.headers = {
            "Authorization": os.getenv("CLICKUP_ACCESS_TOKEN")}
        self.team_id = os.getenv("CLICKUP_TEAM_ID")

    def get_spaces(self) -> Any:
        url = f"https://api.clickup.com/api/v2/team/{self.team_id}/space"
        query = {"archived": "false"}
        response = requests.get(url, headers=self.headers, params=query)
        data = response.json()
        spaces_info = []

        for space in data["spaces"]:
            space_info = {
                "space_id": space["id"],
                "name": space["name"]
            }
            spaces_info.append(space_info)

        return spaces_info

    def get_folders(self, space_id: str) -> Any:
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        query = {"archived": "false"}
        response = requests.get(url, headers=self.headers, params=query)
        folders_data = response.json()
        return folders_data['folders']

    def get_lists(self, folder: dict) -> Any:
        lists_info = []

        for list in folder['lists']:
            list_info = {
                "id": list["id"],
                "name": list["name"]
            }
            lists_info.append(list_info)

        return lists_info

    def get_lists_ids(self) -> Any:
        all_lists = {}
        for space in self.get_spaces():
            for folder in self.get_folders(space['space_id']):
                for list_item in self.get_lists(folder):
                    all_lists[f'{space["name"]}/{folder["name"]}/{list_item["name"]}'] = list_item["id"]

        return all_lists

    def create_task(self, list_id: str, name: str, description: str, assignees: list = []) -> Any:
        """Creates a task receiving the task data dict containing name and description"""
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"

        query = {
            "custom_task_ids": "true",
            "team_id": self.team_id
        }

        payload = {
            "name": name,
            "description": description,
            "assignees": assignees,
            "archived": False,
            "group_assignees": []
        }

        response = requests.post(
            url, json=payload, headers=self.headers, params=query)
        return response.json()

    def get_tasks(self, list_id: str):

        url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

        query = {
        "archived": "false",
        "include_markdown_description": "true",
        "page": "0",
        "order_by": "string",
        "reverse": "true",
        "subtasks": "true",
        "statuses": [],
        "include_closed": "true",
        "assignees": [],
        "watchers": "string",
        "tags": "string",
        "due_date_gt": "0",
        "due_date_lt": "0",
        "date_created_gt": "0",
        "date_created_lt": "0",
        "date_updated_gt": "0",
        "date_updated_lt": "0",
        "date_done_gt": "0",
        "date_done_lt": "0",
        "custom_fields": "string",
        "custom_field": "string",
        "custom_items": "0"
        }

        response = requests.get(url, headers=self.headers, params=query)
        data = response.json()
        return data

    def get_list_members(self, list_id: str) -> Any:
        url = f"https://api.clickup.com/api/v2/list/{list_id}/member"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        members = [{"id": member["id"], "username": member["username"]}
                   for member in data.get("members", [])]
        return members
