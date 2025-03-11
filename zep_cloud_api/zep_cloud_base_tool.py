import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
import requests
import json
import asyncio
from zep_python.client import AsyncZep, Zep
from zep_python.types import Message


class ZepCloudBaseTool(BaseTool):
    """Base class for Zep Cloud tools with common functionality."""

    def __init__(self, **kwargs):
        load_dotenv()
        super().__init__(handle_tool_error=True, **kwargs)
        self.api_key = os.getenv("ZEP_CLOUD_API_KEY")
        self.base_url = "https://api.getzep.com"
        self.client = Zep(base_url=self.base_url, api_key=self.api_key)
