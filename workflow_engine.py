"""
🔄 CrewGraph Workflow Engine
Visual workflow builder and executor for complex multi-step automations.
Supports: Drag-and-drop style logic, conditional branching, loops, and parallel execution.
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime

class NodeType(Enum):
    TRIGGER = "trigger"
    ACTION = "action"
    CONDITION = "condition"
    AGENT = "agent"
    CONNECTOR = "connector"
    END = "end"

class WorkflowNode:
    def __init__(self, node_id: str, node_type: NodeType, config: Dict[str, Any]):
        self.id = node_id
        self.type = node_type
        self.config = config
        self.inputs = config.get("inputs", [])
        self.outputs = []
        self.next_nodes = []  # List of node IDs
        self.status = "pending"  # pending, running, completed, failed
    
    def execute(self, context: Dict[str, Any], connector_manager) -> Any:
        """Execute the node logic"""
        self.status = "running"
        try:
            if self.type == NodeType.TRIGGER:
                return self._execute_trigger(context)
            elif self.type == NodeType.ACTION:
                return self._execute_action(context)
            elif self.type == NodeType.CONDITION:
                return self._execute_condition(context)
            elif self.type == NodeType.AGENT:
                return self._execute_agent(context, connector_manager)
            elif self.type == NodeType.CONNECTOR:
                return self._execute_connector(context, connector_manager)
            elif self.type == NodeType.END:
                return self._execute_end(context)
        except Exception as e:
            self.status = "failed"
            raise e
        finally:
            if self.status != "failed":
                self.status = "completed"
    
    def _execute_trigger(self, context: Dict[str, Any]) -> Any:
        trigger_type = self.config.get("trigger_type", "manual")
        if trigger_type == "manual":
            return {"status": "triggered", "timestamp": datetime.now().isoformat()}
        elif trigger_type == "schedule":
            # Check if current time matches schedule (simplified)
            return {"status": "scheduled_check", "time": datetime.now().isoformat()}
        return {"status": "unknown_trigger"}
    
    def _execute_action(self, context: Dict[str, Any]) -> Any:
        action_type = self.config.get("action_type")
        if action_type == "transform":
            # Simple data transformation
            data = context.get(self.config.get("input_key", "data"))
            transform = self.config.get("transform", "upper")
            if transform == "upper":
                result = str(data).upper()
            elif transform == "lower":
                result = str(data).lower()
            elif transform == "json_parse":
                result = json.loads(str(data))
            else:
                result = data
            context[self.config.get("output_key", "result")] = result
            return result
        elif action_type == "delay":
            import time
            seconds = self.config.get("seconds", 1)
            time.sleep(seconds)
            return {"status": "delayed", "seconds": seconds}
        return {"status": "action_completed"}
    
    def _execute_condition(self, context: Dict[str, Any]) -> bool:
        condition = self.config.get("condition")
        # Simple condition evaluation (supports: equals, contains, greater_than)
        left = context.get(condition.get("left_key"))
        right = condition.get("right_value")
        operator = condition.get("operator", "equals")
        
        result = False
        if operator == "equals":
            result = str(left) == str(right)
        elif operator == "contains":
            result = str(right) in str(left)
        elif operator == "greater_than":
            result = float(left) > float(right)
        elif operator == "less_than":
            result = float(left) < float(right)
        
        context[f"condition_{self.id}"] = result
        return result
    
    def _execute_agent(self, context: Dict[str, Any], connector_manager) -> Any:
        from crewai_node import run_crewai_task
        query = context.get(self.config.get("input_key", "query"), "")
        agent_role = self.config.get("agent_role", "researcher")
        
        # Pass connectors as tools if available
        tools = []
        if connector_manager:
            tools = connector_manager.get_tool_definitions()
        
        result = run_crewai_task(query, role=agent_role, tools=tools)
        context[self.config.get("output_key", "agent_result")] = result
        return result
    
    def _execute_connector(self, context: Dict[str, Any], connector_manager) -> Any:
        if not connector_manager:
            raise Exception("Connector manager not available")
        
        connector_name = self.config.get("connector_name")
        operation = self.config.get("operation", "read")
        resource = context.get(self.config.get("resource_key", "resource"))
        
        connector = connector_manager.connectors.get(connector_name)
        if not connector:
            raise Exception(f"Connector {connector_name} not found")
        
        if operation == "read":
            result = connector.read(resource)
        elif operation == "write":
            data = context.get(self.config.get("data_key", "data"))
            result = connector.write(resource, data)
        else:
            raise Exception(f"Unknown operation: {operation}")
        
        context[self.config.get("output_key", "connector_result")] = result
        return result
    
    def _execute_end(self, context: Dict[str, Any]) -> Any:
        return {"status": "workflow_completed", "final_context": context}

class WorkflowEngine:
    """Executes workflows defined as JSON graphs"""
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.execution_log = []
    
    def load_workflow(self, workflow_def: Dict[str, Any]):
        """Load workflow from JSON definition"""
        self.nodes = {}
        for node_def in workflow_def.get("nodes", []):
            node = WorkflowNode(
                node_id=node_def["id"],
                node_type=NodeType(node_def["type"]),
                config=node_def.get("config", {})
            )
            node.next_nodes = node_def.get("next", [])
            self.nodes[node.id] = node
        
        # Validate workflow
        self._validate_workflow()
    
    def _validate_workflow(self):
        triggers = [n for n in self.nodes.values() if n.type == NodeType.TRIGGER]
        ends = [n for n in self.nodes.values() if n.type == NodeType.END]
        
        if len(triggers) == 0:
            raise ValueError("Workflow must have at least one trigger node")
        if len(ends) == 0:
            raise ValueError("Workflow must have at least one end node")
    
    def execute(self, initial_context: Dict[str, Any], connector_manager=None) -> Dict[str, Any]:
        """Execute the workflow starting from trigger nodes"""
        self.execution_log = []
        context = initial_context.copy()
        
        # Find all trigger nodes
        triggers = [n for n in self.nodes.values() if n.type == NodeType.TRIGGER]
        
        for trigger in triggers:
            self._execute_node_recursive(trigger, context, connector_manager)
        
        return {
            "status": "completed",
            "context": context,
            "log": self.execution_log
        }
    
    def _execute_node_recursive(self, node: WorkflowNode, context: Dict[str, Any], connector_manager):
        log_entry = {
            "node_id": node.id,
            "node_type": node.type.value,
            "start_time": datetime.now().isoformat(),
            "status": "started"
        }
        
        try:
            result = node.execute(context, connector_manager)
            log_entry["result"] = str(result)
            log_entry["status"] = "completed"
            
            # Handle conditional branching
            if node.type == NodeType.CONDITION:
                condition_result = context.get(f"condition_{node.id}", False)
                next_nodes = []
                
                # Check config for true/false paths
                true_next = node.config.get("true_next")
                false_next = node.config.get("false_next")
                
                if condition_result and true_next:
                    next_nodes = [true_next]
                elif not condition_result and false_next:
                    next_nodes = [false_next]
                else:
                    # Fallback to default next nodes
                    next_nodes = node.next_nodes
                
                for next_id in next_nodes:
                    if next_id in self.nodes:
                        self._execute_node_recursive(self.nodes[next_id], context, connector_manager)
            else:
                # Standard sequential execution
                for next_id in node.next_nodes:
                    if next_id in self.nodes:
                        self._execute_node_recursive(self.nodes[next_id], context, connector_manager)
        
        except Exception as e:
            log_entry["status"] = "failed"
            log_entry["error"] = str(e)
            raise e
        
        finally:
            log_entry["end_time"] = datetime.now().isoformat()
            self.execution_log.append(log_entry)

# Pre-built Workflow Templates
WORKFLOW_TEMPLATES = {
    "research_and_publish": {
        "name": "Research & Publish to Notion",
        "description": "Search web, analyze with AI, publish to Notion",
        "nodes": [
            {"id": "start", "type": "trigger", "config": {"trigger_type": "manual"}, "next": ["search"]},
            {"id": "search", "type": "connector", "config": {"connector_name": "websearch", "operation": "read", "resource_key": "query", "output_key": "search_results"}, "next": ["analyze"]},
            {"id": "analyze", "type": "agent", "config": {"agent_role": "analyst", "input_key": "search_results", "output_key": "analysis"}, "next": ["publish"]},
            {"id": "publish", "type": "connector", "config": {"connector_name": "notion", "operation": "write", "data_key": "analysis", "resource_key": "notion_db"}, "next": ["end"]},
            {"id": "end", "type": "end", "config": {}}
        ]
    },
    "github_issue_automation": {
        "name": "GitHub Issue Auto-Responder",
        "description": "Monitor issues, analyze with AI, create response",
        "nodes": [
            {"id": "start", "type": "trigger", "config": {"trigger_type": "manual"}, "next": ["fetch_issues"]},
            {"id": "fetch_issues", "type": "connector", "config": {"connector_name": "github", "operation": "read", "resource_key": "repo", "output_key": "issues"}, "next": ["filter_new"]},
            {"id": "filter_new", "type": "condition", "config": {"condition": {"left_key": "issues", "operator": "contains", "right_value": "new"}}, "true_next": "analyze_issue", "false_next": "end"},
            {"id": "analyze_issue", "type": "agent", "config": {"agent_role": "support", "input_key": "issues", "output_key": "response"}, "next": ["create_comment"]},
            {"id": "create_comment", "type": "connector", "config": {"connector_name": "github", "operation": "write", "data_key": "response"}, "next": ["end"]},
            {"id": "end", "type": "end", "config": {}}
        ]
    },
    "file_processor": {
        "name": "File Processor Pipeline",
        "description": "Read file, process with AI, save result",
        "nodes": [
            {"id": "start", "type": "trigger", "config": {"trigger_type": "manual"}, "next": ["read_file"]},
            {"id": "read_file", "type": "connector", "config": {"connector_name": "filesystem", "operation": "read", "resource_key": "filename", "output_key": "content"}, "next": ["process"]},
            {"id": "process", "type": "agent", "config": {"agent_role": "writer", "input_key": "content", "output_key": "processed"}, "next": ["save_file"]},
            {"id": "save_file", "type": "connector", "config": {"connector_name": "filesystem", "operation": "write", "data_key": "processed", "resource_key": "output_filename"}, "next": ["end"]},
            {"id": "end", "type": "end", "config": {}}
        ]
    }
}

def get_workflow_template(name: str) -> Optional[Dict[str, Any]]:
    return WORKFLOW_TEMPLATES.get(name)

def list_workflow_templates() -> List[Dict[str, str]]:
    return [{"name": k, "description": v["description"]} for k, v in WORKFLOW_TEMPLATES.items()]
