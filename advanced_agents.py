"""
Advanced AI Agents Module
Combines Vision, Voice, Code Execution, and Web Research capabilities.
"""

from vision_agent import VisionAnalyzer
from voice_agent import VoiceAgent
from code_runner_agent import CodeRunnerAgent
from web_search_agent import WebSearchAgent
from typing import Optional, Dict, Any

class AdvancedAgentsHub:
    """
    Central hub for all advanced AI agents.
    Provides unified interface for multi-modal interactions.
    """
    
    def __init__(self):
        self.vision = VisionAnalyzer()
        self.voice = VoiceAgent()
        self.coder = CodeRunnerAgent()
        self.researcher = WebSearchAgent()
        
    def process_multimodal_request(
        self,
        text: str,
        image_path: Optional[str] = None,
        execute_code: bool = False,
        search_web: bool = False
    ) -> Dict[str, Any]:
        """
        Handles complex requests involving multiple modalities.
        """
        results = {}
        
        # 1. Vision Analysis (if image provided)
        if image_path:
            results['vision'] = self.vision.analyze_image(image_path, text)
        
        # 2. Web Research (if requested)
        if search_web:
            results['research'] = self.researcher.research_topic(text)
        
        # 3. Code Execution (if requested)
        if execute_code:
            results['code'] = self.coder.write_and_run(text, "python")
        
        # 4. Voice Output (optional)
        # Can be triggered separately
        
        return results
    
    def autonomous_task(self, task_description: str) -> Dict[str, Any]:
        """
        Fully autonomous task execution.
        Example: "Research AI trends, create a summary chart, and save it"
        """
        steps = []
        
        # Step 1: Research
        research_data = self.researcher.research_topic(task_description)
        steps.append({"step": "Research", "status": "complete", "data": research_data})
        
        # Step 2: Generate analysis code
        analysis_code = f"""
print("Analysis of: {task_description}")
print(f"Sources analyzed: {len(research_data.get('search_results', []))}")
"""
        code_result = self.coder.write_and_run(analysis_code, "python")
        steps.append({"step": "Analysis", "status": "complete", "data": code_result})
        
        return {
            "task": task_description,
            "steps": steps,
            "complete": True
        }

# Example usage
if __name__ == "__main__":
    hub = AdvancedAgentsHub()
    
    # Test web search
    print("🔍 Testing Web Search...")
    results = hub.researcher.search("AI trends 2025", num_results=3)
    for r in results:
        print(f"- {r['title']}")
    
    # Test code execution
    print("\n💻 Testing Code Execution...")
    code = "print('Hello from CrewGraph-AI!')"
    result = hub.coder.write_and_run(code, "python")
    print(f"Output: {result.get('output', 'No output')}")
