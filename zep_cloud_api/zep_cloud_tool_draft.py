import os
from typing import Dict, List, Optional, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
import requests
import json
import asyncio
from zep_python.client import AsyncZep
from zep_python.types import Message


class ZepCloudBaseTool(BaseTool):
    """Base class for Zep Cloud tools with common functionality."""

    api_key: Optional[str] = Field(default=None, description="Zep Cloud API key")
    base_url: str = Field(
        default="https://api.getzep.com", description="Zep Cloud API base URL"
    )
    _client: Optional[AsyncZep] = PrivateAttr(default=None)
    _loop: Optional[asyncio.AbstractEventLoop] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        super().__init__(handle_tool_error=True, **kwargs)
        if not self.api_key:
            self.api_key = os.getenv("ZEP_CLOUD_API_KEY")
        self._client = AsyncZep(api_key=self.api_key, base_url=self.base_url)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def _arun(self, coroutine):
        """Helper method to run async code in sync context."""
        try:
            return self._loop.run_until_complete(coroutine)
        finally:
            self._loop.close()


# Input schemas for each tool
class AddDataToGraphInput(BaseModel):
    """Schema for adding data to graph."""

    data: Dict[str, Any] = Field(
        ...,
        description="Data to add to the graph",
        example={
            "type": "user_preference",
            "content": "Prefers dark mode",
            "metadata": {"confidence": 0.9},
        },
    )


class SearchGraphInput(BaseModel):
    """Schema for searching graph."""

    query: str = Field(
        ...,
        description="Search query for the graph",
        example="user preferences dark mode",
    )
    scope: Optional[str] = Field(
        None, description="Scope of the search", example="user_preferences"
    )
    limit: Optional[int] = Field(
        10, description="Maximum number of results to return", example=10
    )


class UserIdInput(BaseModel):
    """Schema for endpoints requiring user ID."""

    user_id: str = Field(..., description="ID of the user", example="user123")


class UUIDInput(BaseModel):
    """Schema for endpoints requiring UUID."""

    uuid: str = Field(
        ...,
        description="UUID of the resource",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class AddDataToGraphTool(ZepCloudBaseTool):
    """Tool for adding data to the Zep Cloud graph."""

    name: str = "add_data_to_graph"
    description: str = (
        "Add new insights or preferences about the user to the graph for long-term storage"
    )
    args_schema: type[BaseModel] = AddDataToGraphInput

    def _run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph operations
        url = f"{self.base_url}/graph"
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}, json=data
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class SearchGraphTool(ZepCloudBaseTool):
    """Tool for searching the Zep Cloud graph."""

    name: str = "search_graph"
    description: str = (
        "Search the graph for relevant user data, preferences, and insights"
    )
    args_schema: type[BaseModel] = SearchGraphInput

    def _run(
        self, query: str, scope: Optional[str] = None, limit: Optional[int] = 10
    ) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph search
        url = f"{self.base_url}/graph/search"
        payload = {"query": query, "scope": scope, "limit": limit}
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}, json=payload
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class GetUserEdgesTool(ZepCloudBaseTool):
    """Tool for retrieving user edges from the Zep Cloud graph."""

    name: str = "get_user_edges"
    description: str = (
        "Retrieve relationships (edges) that link user data points together"
    )
    args_schema: type[BaseModel] = UserIdInput

    def _run(self, user_id: str) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph edges
        url = f"{self.base_url}/graph/edge/user/{user_id}"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class GetEdgeByUUIDTool(ZepCloudBaseTool):
    """Tool for retrieving a specific edge from the Zep Cloud graph."""

    name: str = "get_edge_by_uuid"
    description: str = (
        "Fetch detailed information about a specific relationship between user data points"
    )
    args_schema: type[BaseModel] = UUIDInput

    def _run(self, uuid: str) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph edges
        url = f"{self.base_url}/graph/edge/{uuid}"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class DeleteEdgeByUUIDTool(ZepCloudBaseTool):
    """Tool for deleting a specific edge from the Zep Cloud graph."""

    name: str = "delete_edge_by_uuid"
    description: str = (
        "Remove outdated or irrelevant relationships from the user's graph"
    )
    args_schema: type[BaseModel] = UUIDInput

    def _run(self, uuid: str) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph edges
        url = f"{self.base_url}/graph/edge/{uuid}"
        response = requests.delete(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class GetUserNodesTool(ZepCloudBaseTool):
    """Tool for retrieving user nodes from the Zep Cloud graph."""

    name: str = "get_user_nodes"
    description: str = "Retrieve all nodes (data points) associated with the user"
    args_schema: type[BaseModel] = UserIdInput

    def _run(self, user_id: str) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph nodes
        url = f"{self.base_url}/graph/node/user/{user_id}"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class GetNodeByUUIDTool(ZepCloudBaseTool):
    """Tool for retrieving a specific node from the Zep Cloud graph."""

    name: str = "get_node_by_uuid"
    description: str = "Fetch detailed information about a specific data point (node)"
    args_schema: type[BaseModel] = UUIDInput

    def _run(self, uuid: str) -> Dict[str, Any]:
        """Run the tool."""
        # TODO: Update when SDK supports graph nodes
        url = f"{self.base_url}/graph/node/{uuid}"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")
        return response.json()


class GetUserEpisodesTool(ZepCloudBaseTool):
    """Tool for retrieving user episodes from the Zep Cloud graph."""

    name: str = "get_user_episodes"
    description: str = (
        "Retrieve a history of episodes (interactions or events) associated with the user"
    )
    args_schema: type[BaseModel] = UserIdInput

    def _run(self, user_id: str) -> Dict[str, Any]:
        """Run the tool."""
        return self._arun(
            self._client.memory.search_sessions(user_id=user_id, search_scope="facts")
        )


class GetEpisodeByUUIDTool(ZepCloudBaseTool):
    """Tool for retrieving a specific episode from the Zep Cloud graph."""

    name: str = "get_episode_by_uuid"
    description: str = (
        "Retrieve detailed information about a specific interaction or event"
    )
    args_schema: type[BaseModel] = UUIDInput

    def _run(self, uuid: str) -> Dict[str, Any]:
        """Run the tool."""
        return self._arun(self._client.memory.get(session_id=uuid))



# Export all tools
__all__ = [
    "AddDataToGraphTool",
    "SearchGraphTool",
    "GetUserEdgesTool",
    "GetEdgeByUUIDTool",
    "DeleteEdgeByUUIDTool",
    "GetUserNodesTool",
    "GetNodeByUUIDTool",
    "GetUserEpisodesTool",
    "GetEpisodeByUUIDTool",
]
