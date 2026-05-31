"""
🌐 CrewGraph Advanced Web UI
Complete web interface with connectors, workflows, and automation.
Features: Account connections, workflow builder, auto-execution, real-time monitoring.
"""
import gradio as gr
import json
from typing import Dict, Any
from config import OLLAMA_MODEL, CHROMA_PERSIST_DIR
from memory import get_memory_session
from crewai_node import run_crewai_task
from langgraph_setup import run_langgraph_workflow
from connectors import connector_manager, ConnectorManager
from workflow_engine import WorkflowEngine, list_workflow_templates, get_workflow_template

# Global state
active_workflows = {}
session_history = []

def connect_account(connector_type: str, name: str, **credentials) -> str:
    """Connect external account (GitHub, Notion, etc.)"""
    config = credentials
    
    # Add default configs
    if connector_type == "filesystem":
        config["base_path"] = "./workspace"
    elif connector_type == "websearch":
        pass  # No credentials needed
    
    success = connector_manager.add_connector(name, connector_type, config)
    
    if success:
        return f"✅ Successfully connected to {name} ({connector_type})"
    else:
        return f"❌ Failed to connect to {name}. Check credentials."

def list_connected_accounts() -> str:
    """List all connected accounts"""
    if not connector_manager.connectors:
        return "No accounts connected yet."
    
    result = "📌 Connected Accounts:\n"
    for name, conn in connector_manager.connectors.items():
        status = "🟢 Connected" if conn.connected else "🔴 Disconnected"
        result += f"- **{name}** ({conn.name}): {status}\n"
    
    return result

def execute_workflow(template_name: str, params_json: str) -> str:
    """Execute a pre-built or custom workflow"""
    try:
        params = json.loads(params_json) if params_json else {}
    except:
        return "❌ Invalid JSON in parameters"
    
    # Get workflow template
    workflow_def = get_workflow_template(template_name)
    if not workflow_def:
        # Try to load as custom JSON
        try:
            workflow_def = json.loads(template_name)
        except:
            return f"❌ Workflow template '{template_name}' not found"
    
    # Initialize engine
    engine = WorkflowEngine()
    engine.load_workflow(workflow_def)
    
    # Execute with context
    context = {"query": params.get("query", ""), "timestamp": str(json.dumps(params))}
    
    try:
        result = engine.execute(context, connector_manager)
        
        # Store in active workflows
        workflow_id = f"wf_{len(active_workflows)}"
        active_workflows[workflow_id] = result
        
        output = f"✅ Workflow completed successfully!\n\n"
        output += f"**Execution Log:**\n"
        for log in result.get("log", []):
            status_icon = "✅" if log["status"] == "completed" else "❌"
            output += f"- {status_icon} {log['node_type']} ({log['node_id']}): {log['status']}\n"
        
        output += f"\n**Final Context:**\n```json\n{json.dumps(result.get('context', {}), indent=2)}\n```"
        return output
    except Exception as e:
        return f"❌ Workflow execution failed: {str(e)}"

def run_automated_task(task_type: str, query: str, target_connector: str) -> str:
    """Run fully automated task with connectors"""
    if not query:
        return "❌ Please enter a task description"
    
    # Build automatic workflow based on task type
    workflow_steps = []
    
    if task_type == "Research & Save":
        # Search → Analyze → Save to File
        workflow_steps = [
            ("Web Search", f"Search for: {query}"),
            ("AI Analysis", f"Analyze and summarize: {query}"),
            ("Save to File", f"Save results to {target_connector}")
        ]
    elif task_type == "GitHub Automation":
        # Fetch Issues → Analyze → Create Response
        workflow_steps = [
            ("Fetch GitHub Issues", f"From repo: {target_connector}"),
            ("AI Analysis", f"Analyze issues related to: {query}"),
            ("Create Response", f"Post response to GitHub")
        ]
    elif task_type == "Notion Publishing":
        # Research → Write → Publish
        workflow_steps = [
            ("Web Research", f"Research topic: {query}"),
            ("Content Writing", f"Write article about: {query}"),
            ("Publish to Notion", f"Publish to database: {target_connector}")
        ]
    
    # Execute using CrewAI with connector tools
    tools = []
    if connector_manager.connectors:
        tools = connector_manager.get_tool_definitions()
    
    full_query = f"{task_type}: {query}\nTarget: {target_connector}\nSteps: {workflow_steps}"
    
    try:
        result = run_crewai_task(full_query, role="analyst", tools=tools)
        
        output = f"✅ Automated Task Completed!\n\n"
        output += f"**Task Type:** {task_type}\n"
        output += f"**Query:** {query}\n"
        output += f"**Target:** {target_connector}\n\n"
        output += f"**Execution Steps:**\n"
        for i, (step, desc) in enumerate(workflow_steps, 1):
            output += f"{i}. {step}: {desc}\n"
        output += f"\n**AI Result:**\n{result}"
        
        return output
    except Exception as e:
        return f"❌ Automation failed: {str(e)}"

def create_custom_workflow(nodes_json: str) -> str:
    """Create and validate a custom workflow from JSON"""
    try:
        workflow_def = json.loads(nodes_json)
        engine = WorkflowEngine()
        engine.load_workflow(workflow_def)
        
        output = "✅ Custom workflow created successfully!\n\n"
        output += f"**Workflow Stats:**\n"
        output += f"- Total Nodes: {len(engine.nodes)}\n"
        
        node_types = {}
        for node in engine.nodes.values():
            node_types[node.type.value] = node_types.get(node.type.value, 0) + 1
        
        output += "- Node Breakdown:\n"
        for ntype, count in node_types.items():
            output += f"  - {ntype}: {count}\n"
        
        output += "\n**Nodes:**\n"
        for node_id, node in engine.nodes.items():
            output += f"- `{node_id}` ({node.type.value}) → Next: {node.next_nodes}\n"
        
        return output
    except Exception as e:
        return f"❌ Invalid workflow definition: {str(e)}"

def view_workflow_status() -> str:
    """View status of executed workflows"""
    if not active_workflows:
        return "No workflows executed yet."
    
    output = "📊 Active Workflows:\n\n"
    for wf_id, result in active_workflows.items():
        output += f"**{wf_id}**\n"
        output += f"- Status: {result.get('status', 'unknown')}\n"
        output += f"- Log Entries: {len(result.get('log', []))}\n"
        output += f"- Completed: {'✅' if result.get('status') == 'completed' else '⏳'}\n\n"
    
    return output

# Gradio Interface
with gr.Blocks(title="CrewGraph AI Pro", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 CrewGraph AI Pro - Advanced Automation Platform")
    gr.Markdown("Connect accounts, build workflows, and automate everything!")
    
    with gr.Tabs():
        # Tab 1: Connect Accounts
        with gr.TabItem("🔌 Connect Accounts"):
            gr.Markdown("### Connect your external accounts for automation")
            
            with gr.Row():
                with gr.Column():
                    conn_name = gr.Textbox(label="Connection Name", placeholder="my-github")
                    conn_type = gr.Dropdown(
                        ["github", "notion", "filesystem", "websearch"],
                        label="Service Type"
                    )
                    
                    github_token = gr.Textbox(label="GitHub Token (optional)", type="password", visible=False)
                    github_user = gr.Textbox(label="GitHub Username (optional)", visible=False)
                    notion_token = gr.Textbox(label="Notion Token (optional)", type="password", visible=False)
                    notion_db = gr.Textbox(label="Notion Database ID (optional)", visible=False)
                    
                    connect_btn = gr.Button("Connect Account", variant="primary")
                    connect_output = gr.Textbox(label="Connection Status")
                
                with gr.Column():
                    list_btn = gr.Button("Refresh Connected Accounts")
                    accounts_output = gr.Textbox(label="Connected Accounts", lines=10)
            
            def toggle_credentials(service_type):
                return {
                    github_token: gr.update(visible=service_type == "github"),
                    github_user: gr.update(visible=service_type == "github"),
                    notion_token: gr.update(visible=service_type == "notion"),
                    notion_db: gr.update(visible=service_type == "notion")
                }
            
            conn_type.change(fn=toggle_credentials, inputs=[conn_type], outputs=[github_token, github_user, notion_token, notion_db])
            
            connect_btn.click(
                fn=lambda name, type_, gh_tok, gh_usr, nt, nd: connect_account(
                    type_, name,
                    token=gh_tok or nt,
                    username=gh_usr,
                    database_id=nd
                ),
                inputs=[conn_name, conn_type, github_token, github_user, notion_token, notion_db],
                outputs=[connect_output]
            )
            
            list_btn.click(fn=list_connected_accounts, outputs=[accounts_output])
        
        # Tab 2: Workflow Templates
        with gr.TabItem("🔄 Workflow Templates"):
            gr.Markdown("### Run pre-built automation workflows")
            
            templates = list_workflow_templates()
            template_names = [t["name"] for t in templates]
            
            with gr.Row():
                with gr.Column():
                    template_select = gr.Dropdown(template_names, label="Select Template")
                    template_desc = gr.Textbox(label="Description", interactive=False)
                    params_input = gr.JSON(
                        value={"query": "AI trends 2026", "repo": "my-repo", "notion_db": "db-id"},
                        label="Parameters (JSON)"
                    )
                    run_template_btn = gr.Button("Run Workflow", variant="primary")
                    template_output = gr.Textbox(label="Execution Result", lines=15)
                
                with gr.Column():
                    gr.Markdown("#### Available Templates:")
                    template_list = "\n".join([f"- **{t['name']}**: {t['description']}" for t in templates])
                    gr.Markdown(template_list)
            
            def update_template_desc(name):
                for t in templates:
                    if t["name"] == name:
                        return t["description"]
                return ""
            
            template_select.change(fn=update_template_desc, inputs=[template_select], outputs=[template_desc])
            run_template_btn.click(fn=execute_workflow, inputs=[template_select, params_input], outputs=[template_output])
        
        # Tab 3: Custom Workflow Builder
        with gr.TabItem("🛠️ Custom Workflow Builder"):
            gr.Markdown("### Build your own automation workflows (JSON)")
            
            default_workflow = json.dumps({
                "nodes": [
                    {"id": "start", "type": "trigger", "config": {"trigger_type": "manual"}, "next": ["step1"]},
                    {"id": "step1", "type": "agent", "config": {"agent_role": "researcher", "input_key": "query"}, "next": ["end"]},
                    {"id": "end", "type": "end", "config": {}}
                ]
            }, indent=2)
            
            with gr.Row():
                with gr.Column(scale=2):
                    workflow_json = gr.Code(
                        language="json",
                        value=default_workflow,
                        label="Workflow Definition (JSON)",
                        lines=20
                    )
                with gr.Column(scale=1):
                    create_btn = gr.Button("Create & Validate", variant="primary")
                    workflow_status = gr.Textbox(label="Validation Result", lines=10)
            
            create_btn.click(fn=create_custom_workflow, inputs=[workflow_json], outputs=[workflow_status])
        
        # Tab 4: Automated Tasks
        with gr.TabItem("⚡ Quick Automation"):
            gr.Markdown("### Run fully automated tasks with one click")
            
            with gr.Row():
                with gr.Column():
                    auto_task_type = gr.Dropdown(
                        ["Research & Save", "GitHub Automation", "Notion Publishing", "File Processing"],
                        label="Task Type"
                    )
                    auto_query = gr.Textbox(label="Task Description", placeholder="What should I do?", lines=3)
                    auto_target = gr.Textbox(label="Target (Repo/DB/Folder)", placeholder="my-repo or my-database")
                    run_auto_btn = gr.Button("Run Automated Task", variant="primary")
                    auto_output = gr.Textbox(label="Result", lines=15)
                
                with gr.Column():
                    gr.Markdown("#### How it works:")
                    gr.Markdown("""
                    1. **Select Task Type**: Choose what you want to automate
                    2. **Describe Task**: Tell the AI what to do in natural language
                    3. **Set Target**: Specify which account/folder/database to use
                    4. **Run**: AI will automatically orchestrate agents and connectors
                    
                    ✨ **Fully Automatic**: No manual steps needed!
                    """)
            
            run_auto_btn.click(
                fn=run_automated_task,
                inputs=[auto_task_type, auto_query, auto_target],
                outputs=[auto_output]
            )
        
        # Tab 5: Monitor & Logs
        with gr.TabItem("📊 Monitor"):
            gr.Markdown("### Monitor active workflows and execution logs")
            
            refresh_btn = gr.Button("Refresh Status")
            status_output = gr.Textbox(label="Workflow Status", lines=20)
            
            refresh_btn.click(fn=view_workflow_status, outputs=[status_output])
    
    gr.Markdown("---")
    gr.Markdown("Built with ❤️ using LangGraph + CrewAI + Local LLMs")

if __name__ == "__main__":
    print("🚀 Launching CrewGraph AI Pro Web Interface...")
    print("🌐 Open http://localhost:7860 in your browser")
    demo.launch(server_name="0.0.0.0", server_port=7860)
