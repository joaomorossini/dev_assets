import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
import requests
import json
import asyncio
from zep_python.client import AsyncZep
from zep_python.types import Message
from zep_cloud_base_tool import ZepCloudBaseTool
from zep_cloud.client import Zep


from pydantic import BaseModel
from typing import Optional, Union

from pydantic import BaseModel
from typing import Optional, Union


class AddDataToGraphSchema(BaseModel):
    data: Optional[Union[str, dict]] = Field(
        default=None,
        description="The data to be added, can be a string or JSON object.",
        examples=["{'key': 'value'}", "Sample text data"],
    )
    type: Optional[str] = Field(
        default=None,
        description="The type of data. Allowed values: 'text', 'json', 'message'.",
        examples=["text", "json", "message"],
    )
    user_id: Optional[str] = Field(
        default=None,
        description="The user ID to associate the data with.",
        examples=["user_456", "user_789"],
    )
    group_id: Optional[str] = Field(
        default=None,
        description="The group ID to associate the data with.",
        examples=["group_123", "team_alpha"],
    )


class AddDataToGraphTool(BaseTool):
    name: str = "add_data_to_graph_tool"
    description: str = """Add data to Zep Cloud's knowledge graph.
        This can be used to for user data, group data and for business documents, which can be used as a knowledge base for your application.   
    """
    args_schema: Type[BaseModel] = AddDataToGraphSchema

    def __init__(self, **kwargs):
        # Initialize the parent class
        super().__init__(handle_tool_error=True, **kwargs)

        # Load environment variables
        load_dotenv()

        # Define instance variables (not Pydantic fields)
        self.api_key = os.getenv("ZEP_CLOUD_API_KEY")
        self.base_url = "https://api.getzep.com"
        self.client = Zep(base_url=self.base_url, api_key=self.api_key)

    def _run(self, data, type, user_id, group_id):
        response = self.client.graph.add(
            data=data, type=type, user_id=user_id, group_id=group_id
        )
        print(response)
        return response
