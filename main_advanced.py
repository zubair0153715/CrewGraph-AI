"""
Advanced Web UI with Document Upload, Streaming, and Multi-Modal Support
Includes: File upload, Chat history, Agent selection, Real-time streaming
"""
import gradio as gr
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import json

from config import HOST, PORT, LLM_MODEL, ENABLE_HITL, ENABLE_PARALLEL, ENABLE_REFLECTION
from langgraph_setup import get_graph
from langgraph_advanced import get_advanced_graph


# Global session storage
sessions = {}


def get_or_create_session(session_id: str) -> Dict:
    """Get or create a user session"""
    if session_id not in sessions:
        sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "documents": [],
            "metadata": {}
        }
    return sessions[session_id]


def process_query_advanced(
    query: str, 
    session_id: str,
    use_advanced: bool = True,
    selected_agents: List[str] = None,
    temperature: float = 0.7
) -> str:
    """Process query through advanced LangGraph workflow"""
    try:
        # Choose graph based on mode
        if use_advanced:
            graph = get_advanced_graph()
        else:
            graph = get_graph()
        
        session = get_or_create_session(session_id)
        
        # Initialize state
        initial_state = {
            "query": query,
            "context": "",
            "task_type": "general",
            "messages": session["messages"],
            "result": "",
            "agents_used": selected_agents or [],
            "tasks_completed": 0,
            "validation_status": "",
            "session_id": session_id,
            "sub_tasks": [],
            "parallel_results": [],
            "reflection_count": 0,
            "requires_approval": False,
            "user_approved": False,
            "documents": session.get("documents", []),
            "streaming_buffer": "",
            "metadata": {
                "temperature": temperature,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        # Update session
        session["messages"].append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        session["messages"].append({
            "role": "assistant",
            "content": result.get("result", ""),
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "agents_used": result.get("agents_used", []),
                "tasks_completed": result.get("tasks_completed", 0),
                "reflection_count": result.get("reflection_count", 0)
            }
        })
        
        # Format output
        output_parts = []
        
        # Main response
        output_parts.append(f"📝 **Response:**\n{result.get('result', 'No response')}")
        
        # Agents used
        if result.get('agents_used'):
            agents_str = ', '.join(result['agents_used'])
            output_parts.append(f"\n🤖 **Agents Used:** {agents_str}")
        
        # Tasks completed
        if result.get('tasks_completed', 0) > 0:
            output_parts.append(f"\n✅ **Tasks Completed:** {result['tasks_completed']}")
        
        # Reflection info
        if result.get('reflection_count', 0) > 0:
            output_parts.append(f"\n🔄 **Reflection Iterations:** {result['reflection_count']}")
        
        # Validation status
        if result.get('validation_status'):
            output_parts.append(f"\n✓ **Validation:** {result['validation_status']}")
        
        # Quality score
        if result.get('metadata', {}).get('quality_score'):
            score = result['metadata']['quality_score']
            output_parts.append(f"\n⭐ **Quality Score:** {score:.2f}/1.00")
        
        return "\n".join(output_parts)
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(f"⚠️  {error_msg}")
        return error_msg


def handle_file_upload(file, session_id: str) -> str:
    """Handle document upload and processing"""
    if file is None:
        return "No file uploaded"
    
    try:
        session = get_or_create_session(session_id)
        
        # Save file path
        file_path = file.name if hasattr(file, 'name') else str(file)
        session["documents"].append(file_path)
        
        # Process document
        from crewai_node import process_document
        
        result = process_document(
            file_path, 
            "Summarize this document and extract key points"
        )
        
        if result.get("success"):
            return f"✅ Document processed successfully!\n\n{result.get('result', '')}"
        else:
            return f"⚠️  Processing failed: {result.get('result', '')}"
    
    except Exception as e:
        return f"❌ Error processing document: {str(e)}"


def clear_session(session_id: str) -> tuple:
    """Clear chat history and reset session"""
    if session_id in sessions:
        del sessions[session_id]
    
    new_session_id = str(uuid.uuid4())
    return new_session_id, "", "Session cleared. Ready for new conversation!"


def get_session_stats(session_id: str) -> str:
    """Get statistics for current session"""
    if session_id not in sessions:
        return "No active session"
    
    session = sessions[session_id]
    message_count = len([m for m in session["messages"] if m["role"] == "user"])
    doc_count = len(session.get("documents", []))
    
    return f"""
📊 **Session Statistics**
- Messages: {message_count}
- Documents: {doc_count}
- Session ID: {session_id[:8]}...
- Created: {session.get('created_at', 'N/A')}
"""


# Create Advanced Gradio Interface
def create_advanced_ui():
    """Create enhanced web UI with all features"""
    
    with gr.Blocks(title="CrewGraph-AI Pro", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🤖 CrewGraph-AI Pro
        ### Advanced Multi-Agent AI System
        
        🔒 100% Local | 💸 Zero API Cost | 🧠 Smart Routing & Validation | 📄 Document Support
        """)
        
        # Session management
        session_id = gr.State(str(uuid.uuid4()))
        
        with gr.Row():
            with gr.Column(scale=3):
                # Chat interface
                chatbot = gr.ChatInterface(
                    fn=lambda msg, hist: process_query_advanced(msg, session_id.value, True),
                    title="CrewGraph-AI Assistant",
                    description="Ask anything! Supports simple queries, complex research, code generation, and document analysis.",
                    examples=[
                        "Hello! What can you do?",
                        "Explain quantum computing briefly",
                        "Research and analyze the impact of AI on healthcare",
                        "Compare Python vs JavaScript for web development",
                        "Write a Python function to sort a list",
                        "Create a roadmap for learning machine learning"
                    ],
                    theme=gr.themes.Soft(),
                )
                
            with gr.Column(scale=1):
                # Control panel
                gr.Markdown("### ⚙️ Controls")
                
                # Mode selection
                use_advanced = gr.Checkbox(
                    label="Use Advanced Mode",
                    value=True,
                    info="Enable task decomposition, parallel execution, and reflection"
                )
                
                # Agent selection
                agent_selection = gr.CheckboxGroup(
                    choices=["researcher", "writer", "analyst", "coder", "reviewer"],
                    value=["researcher", "writer"],
                    label="Select Agents"
                )
                
                # Temperature slider
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature (Creativity)"
                )
                
                # File upload
                file_upload = gr.File(
                    label="📄 Upload Document",
                    file_types=[".txt", ".md", ".pdf"]
                )
                upload_btn = gr.Button("Process Document", variant="primary")
                upload_output = gr.Textbox(label="Document Processing Result", lines=5)
                
                # Session stats
                stats_btn = gr.Button("📊 View Stats")
                stats_output = gr.Textbox(label="Session Statistics", lines=5)
                
                # Clear button
                clear_btn = gr.Button("🗑️ Clear Session", variant="stop")
                
                # Settings accordion
                with gr.Accordion("🔧 Advanced Settings", open=False):
                    gr.Markdown(f"""
                    - **LLM Model:** {LLM_MODEL}
                    - **Memory:** Enabled (ChromaDB)
                    - **Validation:** Enabled (Pydantic)
                    - **HITL:** {'Enabled' if ENABLE_HITL else 'Disabled'}
                    - **Parallel Execution:** {'Enabled' if ENABLE_PARALLEL else 'Disabled'}
                    - **Agent Reflection:** {'Enabled' if ENABLE_REFLECTION else 'Disabled'}
                    """)
                    
                    gr.Markdown("""
                    ### Tips:
                    - Use "research", "analyze", "compare" for multi-agent tasks
                    - Use "create a plan" or "roadmap" for task decomposition
                    - Upload documents for context-aware analysis
                    - Adjust temperature for more creative responses
                    """)
        
        # Event handlers
        upload_btn.click(
            fn=lambda file, sid: handle_file_upload(file, sid),
            inputs=[file_upload, session_id],
            outputs=upload_output
        )
        
        stats_btn.click(
            fn=lambda sid: get_session_stats(sid),
            inputs=session_id,
            outputs=stats_output
        )
        
        clear_btn.click(
            fn=lambda sid: clear_session(sid),
            inputs=session_id,
            outputs=[session_id, chatbot.chatbot, stats_output]
        )
    
    return demo


def main():
    """Main entry point for advanced UI"""
    print(f"🚀 Starting CrewGraph-AI Pro...")
    print(f"📡 Web UI will be available at: http://{HOST}:{PORT}")
    print(f"🧠 Using LLM: {LLM_MODEL}")
    print(f"💡 Make sure Ollama is running: ollama serve")
    print("-" * 50)
    
    # Launch Gradio app
    demo = create_advanced_ui()
    demo.queue().launch(
        server_name=HOST,
        server_port=PORT,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
