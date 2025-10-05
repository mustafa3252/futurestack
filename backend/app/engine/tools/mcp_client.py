"""
MCP (Model Context Protocol) client for Docker MCP integration.
Connects to Docker MCP services for enhanced research capabilities.
"""

import os
import httpx
from typing import Optional, Dict, Any, List
from llama_index.core.tools import FunctionTool


class MCPClient:
    """Client for interacting with Docker MCP services."""

    def __init__(self, gateway_url: str = "http://localhost:8080"):
        self.gateway_url = gateway_url
        self.client = httpx.AsyncClient(timeout=60.0)

    async def search_web(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search the web using Brave Search MCP."""
        try:
            response = await self.client.post(
                f"{self.gateway_url}/brave-search",
                json={"query": query, "count": num_results}
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            print(f"Web search error: {e}")
            return []

    async def search_reddit(
        self,
        query: str,
        subreddit: Optional[str] = None,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Search Reddit for community insights."""
        try:
            params = {"query": query, "limit": limit}
            if subreddit:
                params["subreddit"] = subreddit

            response = await self.client.post(
                f"{self.gateway_url}/reddit",
                json=params
            )
            response.raise_for_status()
            return response.json().get("posts", [])
        except Exception as e:
            print(f"Reddit search error: {e}")
            return []

    async def search_github(
        self,
        query: str,
        type: str = "repositories",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search GitHub for technical research."""
        try:
            response = await self.client.post(
                f"{self.gateway_url}/github",
                json={"query": query, "type": type, "limit": limit}
            )
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"GitHub search error: {e}")
            return []

    async def save_to_notion(
        self,
        title: str,
        content: str,
        database_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save research report to Notion."""
        try:
            response = await self.client.post(
                f"{self.gateway_url}/notion",
                json={
                    "title": title,
                    "content": content,
                    "database_id": database_id or os.getenv("NOTION_DATABASE_ID")
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Notion save error: {e}")
            return {"error": str(e)}

    async def store_data(
        self,
        collection: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store data in MongoDB via MCP."""
        try:
            response = await self.client.post(
                f"{self.gateway_url}/mongodb",
                json={
                    "action": "insert",
                    "collection": collection,
                    "data": data
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"MongoDB store error: {e}")
            return {"error": str(e)}

    async def query_data(
        self,
        collection: str,
        query: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Query data from MongoDB via MCP."""
        try:
            response = await self.client.post(
                f"{self.gateway_url}/mongodb",
                json={
                    "action": "find",
                    "collection": collection,
                    "query": query
                }
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            print(f"MongoDB query error: {e}")
            return []

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


def create_mcp_tools(gateway_url: str = "http://localhost:8080") -> List[FunctionTool]:
    """Create LlamaIndex tools from MCP client."""
    client = MCPClient(gateway_url)

    async def web_search_tool(query: str) -> str:
        """Search the web for information about a topic."""
        results = await client.search_web(query)
        if not results:
            return "No results found"

        formatted = []
        for r in results[:5]:
            formatted.append(f"- {r.get('title', 'N/A')}: {r.get('description', 'N/A')} ({r.get('url', 'N/A')})")
        return "\n".join(formatted)

    async def reddit_search_tool(query: str, subreddit: Optional[str] = None) -> str:
        """Search Reddit for community discussions and insights."""
        results = await client.search_reddit(query, subreddit)
        if not results:
            return "No Reddit posts found"

        formatted = []
        for r in results[:5]:
            formatted.append(
                f"- r/{r.get('subreddit', 'unknown')}: {r.get('title', 'N/A')} "
                f"({r.get('score', 0)} upvotes, {r.get('num_comments', 0)} comments)"
            )
        return "\n".join(formatted)

    async def github_search_tool(query: str) -> str:
        """Search GitHub for repositories and code."""
        results = await client.search_github(query)
        if not results:
            return "No GitHub results found"

        formatted = []
        for r in results[:5]:
            formatted.append(
                f"- {r.get('full_name', 'N/A')}: {r.get('description', 'N/A')} "
                f"({r.get('stargazers_count', 0)} stars)"
            )
        return "\n".join(formatted)

    return [
        FunctionTool.from_defaults(
            fn=web_search_tool,
            name="web_search",
            description="Search the web for current information about any topic"
        ),
        FunctionTool.from_defaults(
            fn=reddit_search_tool,
            name="reddit_search",
            description="Search Reddit for community discussions, opinions, and insights"
        ),
        FunctionTool.from_defaults(
            fn=github_search_tool,
            name="github_search",
            description="Search GitHub for repositories, code, and technical information"
        ),
    ]
