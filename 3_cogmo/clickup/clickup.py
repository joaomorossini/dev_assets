from typing import Any, List, Type, Optional
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from app.services.clickup_utils import ClickupUtils


class CreateTaskSchema(BaseModel):
    lists_ids = ClickupUtils().get_lists_ids()

    list_id: str = Field(
        description=f"""List the available lists in an enumerated form (It is important that it is a numbered list, so it is easier for the user to decide.) and ask in which one the task should be created. 
DO NOT PROVIDE THE ID TO THE USER, ONLY THE NAMES.
"available_lists": {lists_ids}
When the user provides the name or a respective number for the list, do not use them; use the returned ID, which you did not provide to the user.""")
    name: str = Field(
        description="Name of the task to be created", example="Test task")
    description: str = Field(
        description="Description of the task", example="This is a description")
    assignees: Optional[List[str]] = Field(
        description="List of Member ID to be assigned to the task. Never use the member's name, only their ID", example=["48772077", "48882088"])


class CreateTaskTool(BaseTool):
    name: str = "create_task_tool"
    description: str = """
    This tool creates tasks with ClickUp based on an action, the task name and its description.
    - Create Task:
        Invoking: "create_task_tool" with parameters:
        - "list_id": "123456"
        - "name": "New Task"
        - "description": "This is a new task"
        - "assignees": ["48772077", "48882088"]
    """
    args_schema: Type[BaseModel] = CreateTaskSchema
    clickup: ClickupUtils = ClickupUtils()

    def __init__(self, **data):
        super().__init__(**data)
        self.clickup = ClickupUtils()

    def _run(self, name: str, description: str, assignees: Optional[list] = None, list_id: str = None) -> Any:
        """Runs a tool based on the action"""
        if assignees == None:
            members = ClickupUtils().get_list_members(list_id=list_id)
            warning = f"""Ask the user if any member should be tagged in the task.
List of members:
{members}
If no member is provided by the user, pass an empty list [] to the assignees parameter.
Fill this parameter with the ID, not the user's name
"""
            return warning

        try:
            return self.clickup.create_task(list_id=list_id, name=name, description=description, assignees=assignees)
        except Exception as e:
            return {"error": str(e)}
