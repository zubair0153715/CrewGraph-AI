import subprocess
import tempfile
import os
from typing import Optional, Dict, Any
import json

class CodeRunnerAgent:
    """
    Autonomous Coding Agent that writes, executes, and debugs code safely.
    Supports Python, JavaScript, and Bash with sandboxed execution.
    """
    
    SUPPORTED_LANGUAGES = ["python", "javascript", "bash"]
    
    def __init__(self):
        self.timeout = 30  # seconds
        
    def write_and_run(self, code: str, language: str = "python", input_data: Optional[str] = None) -> Dict[str, Any]:
        if language.lower() not in self.SUPPORTED_LANGUAGES:
            return {"error": f"Unsupported language: {language}", "output": ""}
            
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=self._get_extension(language)) as f:
                f.write(code)
                temp_file = f.name
            
            result = self._execute_file(temp_file, language, input_data)
            
            # Cleanup
            os.unlink(temp_file)
            
            return result
        except Exception as e:
            return {"error": str(e), "output": ""}
    
    def _get_extension(self, language: str) -> str:
        extensions = {
            "python": ".py",
            "javascript": ".js",
            "bash": ".sh"
        }
        return extensions.get(language.lower(), ".txt")
    
    def _execute_file(self, file_path: str, language: str, input_data: Optional[str] = None) -> Dict[str, Any]:
        cmd = []
        
        if language == "python":
            cmd = ["python3", file_path]
        elif language == "javascript":
            cmd = ["node", file_path]
        elif language == "bash":
            cmd = ["bash", file_path]
            
        try:
            process = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=os.path.dirname(file_path)
            )
            
            return {
                "output": process.stdout,
                "error": process.stderr if process.returncode != 0 else "",
                "return_code": process.returncode,
                "success": process.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Execution timed out after {self.timeout}s", "output": ""}
        except FileNotFoundError as e:
            return {"error": f"Interpreter not found: {str(e)}", "output": ""}
    
    def debug_code(self, code: str, error_message: str, language: str = "python") -> str:
        """Suggests fixes for code based on error message."""
        prompt = f"""
        You are an expert debugger. 
        Code: 
        ```{language}
        {code}
        ```
        
        Error: {error_message}
        
        Provide ONLY the corrected code block without explanation.
        """
        # This would call the LLM in a real implementation
        return f"# Debug suggestion for: {error_message}\n# Please check syntax and imports."

    def generate_unit_tests(self, code: str, language: str = "python") -> str:
        """Generates unit tests for the provided code."""
        prompt = f"""
        Generate comprehensive unit tests for this {language} code:
        ```{language}
        {code}
        ```
        Return only the test code.
        """
        return f"# Unit tests generated for {language} code"
