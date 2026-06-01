from langchain_core.tools import Tool
import httpx
from typing import Optional
from app.core.config import settings


def get_browser_search_tool() -> Tool:
    """
    Create a browser search tool for agents
    Uses DuckDuckGo or Google Search API
    """
    
    async def search_web(query: str, num_results: int = 5) -> str:
        """Search the web and return results"""
        try:
            # Using DuckDuckGo HTML API (free, no key needed)
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://html.duckduckgo.com/html/",
                    params={"q": query},
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                
                # Parse results (simplified - in production use proper HTML parser)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                for result in soup.select('.result')[:num_results]:
                    title_elem = result.select_one('.result__title')
                    snippet_elem = result.select_one('.result__snippet')
                    url_elem = result.select_one('.result__url')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True)
                        url = url_elem.get('href') if url_elem else "N/A"
                        
                        results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {url}")
                
                if results:
                    return "\n\n".join(results)
                else:
                    return "No results found."
                    
        except Exception as e:
            return f"Search error: {str(e)}"
    
    return Tool(
        name="browser_search",
        description="Search the web for current information. Use this when you need to find recent data, news, or verify facts.",
        func=lambda q: search_web(q),
        coroutine=search_web,
    )


def get_web_scraping_tool() -> Tool:
    """
    Create a web scraping tool for agents
    """
    
    async def scrape_url(url: str) -> str:
        """Scrape content from a URL"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=30.0
                )
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract main content (simplified)
                # Remove scripts and styles
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                text = soup.get_text(separator='\n', strip=True)
                
                # Limit length
                if len(text) > 5000:
                    text = text[:5000] + "\n... [content truncated]"
                
                return text
                
        except Exception as e:
            return f"Scraping error: {str(e)}"
    
    return Tool(
        name="web_scraper",
        description="Scrape content from a specific URL. Use this when you need to extract detailed information from a webpage.",
        func=lambda u: scrape_url(u),
        coroutine=scrape_url,
    )


# Future tools to implement:
# - YouTube API tool
# - Code execution tool
# - Email sending tool
# - File handling tool
