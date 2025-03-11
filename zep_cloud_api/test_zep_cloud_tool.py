import os
import unittest
import requests
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from zep_cloud_api.zep_cloud_tool_draft import *


class TestZepCloudTools(unittest.TestCase):
    """Test cases for Zep Cloud tools."""

    def setUp(self):
        """Set up test environment."""
        os.environ["ZEP_CLOUD_API_KEY"] = "test_api_key"
        self.mock_response = MagicMock()
        self.mock_response.json.return_value = {"status": "success"}
        self.mock_response.status_code = 200

        # Create event loop for tests
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up after tests."""
        try:
            self.loop.close()
        except:
            pass

    def test_add_data_to_graph(self):
        """Test AddDataToGraphTool."""
        with patch("requests.post", return_value=self.mock_response):
            tool = AddDataToGraphTool()
            result = tool.run(
                {
                    "data": {
                        "type": "user_preference",
                        "content": "Prefers dark mode",
                        "metadata": {"confidence": 0.9},
                    }
                }
            )
            self.assertEqual(result, {"status": "success"})

    def test_search_graph(self):
        """Test SearchGraphTool."""
        with patch("requests.post", return_value=self.mock_response):
            tool = SearchGraphTool()
            result = tool.run("user preferences dark mode")
            self.assertEqual(result, {"status": "success"})

    def test_get_user_edges(self):
        """Test GetUserEdgesTool."""
        with patch("requests.get", return_value=self.mock_response):
            tool = GetUserEdgesTool()
            result = tool.run("user123")
            self.assertEqual(result, {"status": "success"})

    def test_get_edge_by_uuid(self):
        """Test GetEdgeByUUIDTool."""
        with patch("requests.get", return_value=self.mock_response):
            tool = GetEdgeByUUIDTool()
            result = tool.run("550e8400-e29b-41d4-a716-446655440000")
            self.assertEqual(result, {"status": "success"})

    def test_delete_edge_by_uuid(self):
        """Test DeleteEdgeByUUIDTool."""
        with patch("requests.delete", return_value=self.mock_response):
            tool = DeleteEdgeByUUIDTool()
            result = tool.run("550e8400-e29b-41d4-a716-446655440000")
            self.assertEqual(result, {"status": "success"})

    def test_get_user_nodes(self):
        """Test GetUserNodesTool."""
        with patch("requests.get", return_value=self.mock_response):
            tool = GetUserNodesTool()
            result = tool.run("user123")
            self.assertEqual(result, {"status": "success"})

    def test_get_node_by_uuid(self):
        """Test GetNodeByUUIDTool."""
        with patch("requests.get", return_value=self.mock_response):
            tool = GetNodeByUUIDTool()
            result = tool.run("550e8400-e29b-41d4-a716-446655440000")
            self.assertEqual(result, {"status": "success"})

    @patch("zep_python.core.http_client.HttpxClientWrapper")
    @patch("zep_python.memory.client.AsyncMemoryClient")
    @patch("zep_python.client.AsyncZep")
    def test_get_user_episodes(
        self, mock_async_zep, mock_memory_client, mock_http_wrapper
    ):
        """Test GetUserEpisodesTool."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={"status": "success"})

        # Mock HTTP client wrapper
        mock_http_wrapper.return_value.request = AsyncMock(return_value=mock_response)

        # Mock the memory client
        mock_memory_client.return_value._client_wrapper = mock_http_wrapper.return_value
        mock_memory_client.return_value.search_sessions = AsyncMock(
            return_value={"status": "success"}
        )

        # Mock the Zep client
        mock_async_zep.return_value.memory = mock_memory_client.return_value

        tool = GetUserEpisodesTool()
        result = tool.run("user123")
        self.assertEqual(result, {"status": "success"})

    @patch("zep_python.core.http_client.HttpxClientWrapper")
    @patch("zep_python.memory.client.AsyncMemoryClient")
    @patch("zep_python.client.AsyncZep")
    def test_get_episode_by_uuid(
        self, mock_async_zep, mock_memory_client, mock_http_wrapper
    ):
        """Test GetEpisodeByUUIDTool."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={"status": "success"})

        # Mock HTTP client wrapper
        mock_http_wrapper.return_value.request = AsyncMock(return_value=mock_response)

        # Mock the memory client
        mock_memory_client.return_value._client_wrapper = mock_http_wrapper.return_value
        mock_memory_client.return_value.get = AsyncMock(
            return_value={"status": "success"}
        )

        # Mock the Zep client
        mock_async_zep.return_value.memory = mock_memory_client.return_value

        tool = GetEpisodeByUUIDTool()
        result = tool.run("550e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(result, {"status": "success"})

    def test_error_handling(self):
        """Test error handling in tools."""
        mock_error_response = MagicMock()
        mock_error_response.status_code = 500
        mock_error_response.text = "API Error"

        with patch("requests.get", return_value=mock_error_response):
            tool = GetUserNodesTool()
            with self.assertRaises(ValueError) as context:
                tool.run("user123")
            self.assertIn("API request failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
