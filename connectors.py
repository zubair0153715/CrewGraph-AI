"""
🔌 CrewGraph Connectors & Integrations
Handles authentication and API interactions for external services.
Supports: Google, GitHub, Notion, Slack, Local FS, Web Search.
"""
import os
import json
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class ConnectorBase:
    """Base class for all connectors"""
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.connected = False
    
    def connect(self) -> bool:
        raise NotImplementedError
    
    def read(self, resource: str, **kwargs) -> Any:
        raise NotImplementedError
    
    def write(self, resource: str, data: Any, **kwargs) -> bool:
        raise NotImplementedError
    
    def disconnect(self):
        self.connected = False

class FileSystemConnector(ConnectorBase):
    """Secure Local File System Access"""
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Local Files", config)
        self.base_path = Path(config.get("base_path", "./workspace"))
        self.allowed_extensions = config.get("allowed_extensions", [".txt", ".md", ".py", ".json", ".csv"])
        
    def connect(self) -> bool:
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
        self.connected = True
        return True
    
    def read(self, resource: str, **kwargs) -> str:
        file_path = self.base_path / resource
        if not str(file_path.resolve()).startswith(str(self.base_path.resolve())):
            raise SecurityError("Path traversal detected!")
        if not file_path.exists():
            return f"File {resource} not found."
        return file_path.read_text(encoding="utf-8")
    
    def write(self, resource: str, data: str, **kwargs) -> bool:
        file_path = self.base_path / resource
        if not str(file_path.resolve()).startswith(str(self.base_path.resolve())):
            raise SecurityError("Path traversal detected!")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(data, encoding="utf-8")
        return True
    
    def list_files(self, folder: str = "") -> List[str]:
        target = self.base_path / folder if folder else self.base_path
        return [str(f.relative_to(self.base_path)) for f in target.rglob("*") if f.is_file()]

class GitHubConnector(ConnectorBase):
    """GitHub API Integration"""
    def __init__(self, config: Dict[str, Any]):
        super().__init__("GitHub", config)
        self.token = config.get("token")
        self.username = config.get("username")
        self.headers = {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}
    
    def connect(self) -> bool:
        try:
            resp = requests.get("https://api.github.com/user", headers=self.headers)
            self.connected = resp.status_code == 200
            return self.connected
        except:
            return False
    
    def read(self, resource: str, **kwargs) -> Any:
        # resource format: "repo_name/issue_number" or "repo_name/readme"
        if "readme" in resource.lower():
            repo = resource.split("/")[0]
            url = f"https://api.github.com/repos/{self.username}/{repo}/readme"
        elif "issue" in resource.lower():
            parts = resource.split("/")
            repo, issue = parts[0], parts[-1]
            url = f"https://api.github.com/repos/{self.username}/{repo}/issues/{issue}"
        else:
            # Default: List repo contents
            url = f"https://api.github.com/repos/{self.username}/{resource}/contents"
        
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return {"error": resp.text}
        return resp.json()
    
    def write(self, resource: str, data: Any, **kwargs) -> bool:
        # Create Issue or Commit File
        if kwargs.get("type") == "issue":
            repo = resource.split("/")[0]
            url = f"https://api.github.com/repos/{self.username}/{repo}/issues"
            payload = {"title": data.get("title"), "body": data.get("body")}
            resp = requests.post(url, json=payload, headers=self.headers)
            return resp.status_code == 201
        return False

class NotionConnector(ConnectorBase):
    """Notion API Integration"""
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Notion", config)
        self.token = config.get("token")
        self.database_id = config.get("database_id")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def connect(self) -> bool:
        try:
            url = f"https://api.notion.com/v1/databases/{self.database_id}"
            resp = requests.get(url, headers=self.headers)
            self.connected = resp.status_code == 200
            return self.connected
        except:
            return False
    
    def read(self, resource: str, **kwargs) -> Any:
        # Query database
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        resp = requests.post(url, headers=self.headers, json={})
        if resp.status_code != 200:
            return {"error": resp.text}
        return resp.json()
    
    def write(self, resource: str, data: Any, **kwargs) -> bool:
        # Create Page
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": data.get("title", "Untitled")}}]}
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": data.get("content", "")}}]}
                }
            ]
        }
        resp = requests.post(url, json=payload, headers=self.headers)
        return resp.status_code == 200

class WebSearchConnector(ConnectorBase):
    """DuckDuckGo/Web Search (No API Key needed)"""
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Web Search", config)
        self.connected = True
    
    def connect(self) -> bool:
        return True
    
    def read(self, query: str, **kwargs) -> List[Dict]:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                return results
        except ImportError:
            return [{"error": "duckduckgo-search library not installed"}]
        except Exception as e:
            return [{"error": str(e)}]
    
    def write(self, *args, **kwargs):
        raise NotImplementedError("Web Search is read-only")

class SecurityError(Exception):
    pass

class ConnectorManager:
    """Manages all active connectors"""
    def __init__(self):
        self.connectors: Dict[str, ConnectorBase] = {}
    
    def add_connector(self, name: str, type_: str, config: Dict[str, Any]) -> bool:
        connector = None
        if type_ == "filesystem":
            connector = FileSystemConnector(config)
        elif type_ == "github":
            connector = GitHubConnector(config)
        elif type_ == "notion":
            connector = NotionConnector(config)
        elif type_ == "websearch":
            connector = WebSearchConnector(config)
        
        if connector and connector.connect():
            self.connectors[name] = connector
            return True
        return False
    
    def get_tool_definitions(self) -> List[Dict]:
        """Returns LangChain/CrewAI compatible tool definitions"""
        tools = []
        for name, conn in self.connectors.items():
            tools.append({
                "name": f"{name}_read",
                "description": f"Read data from {conn.name}",
                "func": conn.read
            })
            if hasattr(conn, 'write') and conn.write.__name__ != 'write': # Check if implemented
                 tools.append({
                    "name": f"{name}_write",
                    "description": f"Write data to {conn.name}",
                    "func": conn.write
                })
        return tools

# Singleton Instance
connector_manager = ConnectorManager()
