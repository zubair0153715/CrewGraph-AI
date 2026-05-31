import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import quote_plus

class WebSearchAgent:
    """
    Deep Web Research Agent.
    Performs real-time internet searches and extracts information.
    Uses DuckDuckGo HTML search (no API key needed).
    """
    
    def __init__(self):
        self.search_url = "https://html.duckduckgo.com/html/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Searches the web and returns top results.
        """
        try:
            payload = {"q": query}
            response = requests.post(
                self.search_url, 
                data=payload, 
                headers=self.headers,
                timeout=10
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.select('.result', limit=num_results):
                title_elem = result.select_one('.result__title')
                snippet_elem = result.select_one('.result__snippet')
                url_elem = result.select_one('.result__url')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True)
                    url = url_elem['href'] if url_elem else ""
                    
                    # Clean URL if it's a DuckDuckGo redirect
                    if url.startswith('//'):
                        url = 'https:' + url
                    
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": url
                    })
            
            return results
        except Exception as e:
            return [{"title": "Search failed", "snippet": str(e), "url": ""}]
    
    def extract_page_content(self, url: str) -> str:
        """
        Fetches and extracts main content from a webpage.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            text = soup.get_text(separator='\n', strip=True)
            return text[:3000]  # Limit to 3000 chars
        except Exception as e:
            return f"Failed to fetch page: {str(e)}"
    
    def research_topic(self, topic: str, depth: int = 2) -> Dict:
        """
        Performs deep research on a topic with multiple searches.
        Returns comprehensive findings.
        """
        search_queries = [
            f"{topic} overview",
            f"{topic} latest trends 2025",
            f"{topic} benefits challenges"
        ]
        
        all_results = []
        for query in search_queries[:depth]:
            results = self.search(query, num_results=3)
            all_results.extend(results)
        
        # Fetch full content from top 2 URLs
        detailed_content = []
        for result in all_results[:2]:
            if result.get("url"):
                content = self.extract_page_content(result["url"])
                detailed_content.append({
                    "source": result["title"],
                    "content": content
                })
        
        return {
            "query": topic,
            "search_results": all_results,
            "detailed_content": detailed_content,
            "summary": f"Researched {len(all_results)} sources on '{topic}'"
        }
