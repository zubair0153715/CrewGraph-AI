"""
CrewGraph-AI Main Entry Point
FastAPI backend with Gradio web UI
"""
import gradio as gr
import uuid
from typing import Dict, Any
from config import HOST, PORT, LLM_MODEL
from langgraph_setup import get_graph


def process_query(query: str, session_id: str) -> str:
    """Process a query through the LangGraph workflow"""
    try:
        graph = get_graph()
        
        # Initialize state
        initial_state = {
            "query": query,
            "context": "",
            "task_type": "general",
            "messages": [],
            "result": "",
            "agents_used": [],
            "tasks_completed": 0,
            "validation_status": "",
            "session_id": session_id
        }
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        # Format output
        output_parts = []
        output_parts.append(f"📝 **Response:**\n{result.get('result', 'No response')}")
        
        if result.get('agents_used'):
            output_parts.append(f"\n🤖 **Agents Used:** {', '.join(result['agents_used'])}")
        
        if result.get('validation_status'):
            output_parts.append(f"\n✅ **Validation:** {result['validation_status']}")
        
        return "\n".join(output_parts)
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(f"⚠️  {error_msg}")
        return error_msg


def chat_interface(message: str, history: list) -> str:
    """Gradio chat interface handler"""
    if not message.strip():
        return "Please enter a query."
    
    # Generate or use existing session ID
    session_id = getattr(chat_interface, 'session_id', str(uuid.uuid4()))
    chat_interface.session_id = session_id
    
    return process_query(message, session_id)


def clear_chat():
    """Clear chat history and reset session"""
    chat_interface.session_id = str(uuid.uuid4())
    return ""


# Create Gradio Interface
with gr.Blocks(title="CrewGraph-AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 CrewGraph-AI
    ### Multi-Agent AI System with LangGraph + CrewAI
    
    🔒 100% Local | 💸 Zero API Cost | 🧠 Smart Routing & Validation
    """)
    
    chatbot = gr.ChatInterface(
        fn=chat_interface,
        title="CrewGraph-AI Assistant",
        description="Ask anything! Simple queries get quick answers. Complex tasks trigger multi-agent research.",
        examples=[
            "Hello! What can you do?",
            "Explain quantum computing briefly",
            "Research and analyze the impact of AI on healthcare",
            "Compare Python vs JavaScript for web development"
        ],
        theme=gr.themes.Soft(),
        clear_btn=gr.Button("🗑️ Clear Chat", variant="secondary")
    )
    
    # Additional controls
    with gr.Accordion("⚙️ Settings", open=False):
        gr.Markdown(f"""
        - **LLM Model:** {LLM_MODEL}
        - **Memory:** Enabled (ChromaDB)
        - **Validation:** Enabled (Pydantic)
        - **Routing:** Auto (Simple vs Complex)
        """)
        
        gr.Markdown("""
        ### Tips:
        - Use keywords like "research", "analyze", "compare" for complex multi-agent tasks
        - Simple questions get direct, fast responses
        - All conversations are stored locally in ChromaDB for context
        """)


def main():
    """Main entry point"""
    print(f"🚀 Starting CrewGraph-AI...")
    print(f"📡 Web UI will be available at: http://{HOST}:{PORT}")
    print(f"🧠 Using LLM: {LLM_MODEL}")
    print(f"💡 Make sure Ollama is running: ollama serve")
    print("-" * 50)
    
    # Launch Gradio app
    demo.queue().launch(
        server_name=HOST,
        server_port=PORT,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
