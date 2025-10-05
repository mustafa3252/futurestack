"""
Simple MCP Server Implementation
Provides MCP-like functionality using existing APIs
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
import httpx
from llama_index.core.tools import FunctionTool


class SimpleMCPServer:
    """Simple MCP server using existing APIs instead of Docker services."""

    def __init__(self):
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def brave_search(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """Search web using Brave Search API."""
        if not self.brave_api_key:
            return []

        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.brave_api_key
            }
            response = await self.client.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": count},
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "url": item.get("url", "")
                })
            return results
        except Exception as e:
            print(f"Brave search error: {e}")
            return []

    async def reddit_search(self, query: str, subreddit: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Search Reddit using Reddit API."""
        if not self.reddit_client_id or not self.reddit_secret:
            return []

        try:
            # Get OAuth token
            auth_response = await self.client.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=(self.reddit_client_id, self.reddit_secret),
                data={"grant_type": "client_credentials"},
                headers={"User-Agent": "StartupScout/1.0"}
            )
            auth_response.raise_for_status()
            token = auth_response.json()["access_token"]

            # Search Reddit
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "StartupScout/1.0"
            }

            search_url = f"https://oauth.reddit.com/r/{subreddit}/search" if subreddit else "https://oauth.reddit.com/search"
            params = {"q": query, "limit": limit, "sort": "relevance"}

            response = await self.client.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for post in data.get("data", {}).get("children", []):
                post_data = post.get("data", {})
                results.append({
                    "title": post_data.get("title", ""),
                    "subreddit": post_data.get("subreddit", ""),
                    "score": post_data.get("score", 0),
                    "num_comments": post_data.get("num_comments", 0),
                    "url": f"https://reddit.com{post_data.get('permalink', '')}",
                    "selftext": post_data.get("selftext", "")[:200]  # First 200 chars
                })
            return results
        except Exception as e:
            print(f"Reddit search error: {e}")
            return []

    async def github_search(self, query: str, type: str = "repositories", limit: int = 10) -> List[Dict[str, Any]]:
        """Search GitHub using GitHub API."""
        if not self.github_token:
            return []

        try:
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            response = await self.client.get(
                f"https://api.github.com/search/{type}",
                params={"q": query, "per_page": limit},
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append({
                    "name": item.get("name", ""),
                    "full_name": item.get("full_name", ""),
                    "description": item.get("description", ""),
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", ""),
                    "url": item.get("html_url", "")
                })
            return results
        except Exception as e:
            print(f"GitHub search error: {e}")
            return []

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


def create_mcp_tools() -> List[FunctionTool]:
    """Create LlamaIndex tools from SimpleMCPServer."""
    server = SimpleMCPServer()

    async def web_search(query: str) -> str:
        """Search the web for current information. Returns top search results with titles, descriptions, and URLs."""
        results = await server.brave_search(query)
        if not results:
            return "No web results found. The Brave API key may not be configured."

        formatted = ["Web Search Results:"]
        for i, r in enumerate(results[:5], 1):
            formatted.append(f"\n{i}. **{r['title']}**")
            formatted.append(f"   {r['description']}")
            formatted.append(f"   URL: {r['url']}")
        return "\n".join(formatted)

    async def reddit_search(query: str, subreddit: str = None) -> str:
        """Search Reddit for community discussions and insights. Optionally specify a subreddit."""
        results = await server.reddit_search(query, subreddit)
        if not results:
            return "No Reddit posts found. The Reddit API credentials may not be configured."

        formatted = ["Reddit Search Results:"]
        for i, r in enumerate(results[:5], 1):
            formatted.append(f"\n{i}. r/{r['subreddit']}: **{r['title']}**")
            formatted.append(f"   Score: {r['score']} | Comments: {r['num_comments']}")
            formatted.append(f"   {r['selftext'][:150]}..." if r['selftext'] else "")
            formatted.append(f"   {r['url']}")
        return "\n".join(formatted)

    async def github_search(query: str) -> str:
        """Search GitHub for repositories, code, and projects. Returns repo info with stars and descriptions."""
        results = await server.github_search(query)
        if not results:
            return "No GitHub results found. The GitHub token may not be configured."

        formatted = ["GitHub Search Results:"]
        for i, r in enumerate(results[:5], 1):
            formatted.append(f"\n{i}. **{r['full_name']}** ({r['language']})")
            formatted.append(f"   ⭐ {r['stars']} stars")
            formatted.append(f"   {r['description']}")
            formatted.append(f"   {r['url']}")
        return "\n".join(formatted)

    return [
        FunctionTool.from_defaults(
            fn=web_search,
            name="web_search",
            description="Search the web for current information about startups, markets, trends, or any topic. Returns top search results with titles and descriptions."
        ),
        FunctionTool.from_defaults(
            fn=reddit_search,
            name="reddit_search",
            description="Search Reddit for community discussions, user opinions, and authentic insights about products, markets, or topics. Great for customer research."
        ),
        FunctionTool.from_defaults(
            fn=github_search,
            name="github_search",
            description="Search GitHub for repositories, open source projects, and code examples. Useful for technical research and competitor analysis."
        ),
    ]
