# CrewGraph-AI - Complete Setup Guide

## 🎯 Overview
CrewGraph-AI combines **LangGraph + CrewAI + Pydantic Validation + Chroma Memory + Ollama LLMs** into one seamless, 100% local multi-agent AI system.

## ✨ Key Features

### 1. **Smart Routing System**
- Automatically classifies queries as simple or complex
- Simple queries → Direct LLM response (fast)
- Complex queries → Multi-agent CrewAI workflow (thorough)

### 2. **Multi-Agent Coordination (CrewAI)**
- **Researcher Agent**: Finds and analyzes information
- **Writer Agent**: Synthesizes findings into clear responses
- Tasks are delegated based on query complexity

### 3. **Persistent Memory (ChromaDB)**
- All conversations stored locally
- RAG-powered context retrieval
- Session-based memory management
- Ollama embeddings for semantic search

### 4. **Output Validation (Pydantic)**
- Structured response schemas
- Confidence scoring
- Error prevention and formatting guarantees

### 5. **Web UI (Gradio)**
- Clean, responsive chat interface
- Example queries included
- Settings panel with system info
- One-click chat clearing

## 📁 File Structure

```
CrewGraph-AI/
├── main.py              # FastAPI + Gradio Web UI
├── langgraph_setup.py   # StateGraph, Routing, Validation nodes
├── crewai_node.py       # CrewAI multi-agent execution node
├── memory.py            # ChromaDB + Ollama embeddings
├── config.py            # Configuration & environment variables
├── requirements.txt     # Python dependencies
├── run.sh               # 1-click setup & launch script
├── README.md            # Project documentation
├── LICENSE              # MIT License
└── .gitignore           # Git ignore rules
```

## 🚀 Installation Methods

### Method 1: One-Click Setup (Recommended)

```bash
chmod +x run.sh
./run.sh
```

This script will:
1. Check Python 3.10+ installation
2. Verify Ollama is installed
3. Create virtual environment
4. Install all dependencies
5. Pull required models (qwen2.5:7b, nomic-embed-text)
6. Launch the web UI

### Method 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git
cd CrewGraph-AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install and start Ollama
# Visit https://ollama.com to download
# Then run: ollama serve

# 5. Pull models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

# 6. Launch application
python main.py
```

## 🌐 Usage

Once running, open your browser to: **http://localhost:7860**

### Example Queries

**Simple Queries** (Fast, direct response):
- "Hello! What can you do?"
- "What is Python?"
- "Explain gravity briefly"

**Complex Queries** (Triggers multi-agent research):
- "Research and analyze the impact of AI on healthcare"
- "Compare Python vs JavaScript for web development"
- "Analyze the pros and cons of remote work"

## ⚙️ Configuration

Edit `config.py` or set environment variables:

```python
# LLM Settings
LLM_MODEL = "qwen2.5:7b"          # Change to any Ollama model
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"

# Memory Settings
CHROMA_PERSIST_DIR = "./chroma_db"

# Server Settings
HOST = "0.0.0.0"
PORT = "7860"

# Feature Flags
ENABLE_ROUTER = True      # Enable smart routing
ENABLE_VALIDATION = True  # Enable Pydantic validation
ENABLE_MEMORY = True      # Enable ChromaDB memory
```

## 🔧 Customization

### Add New Agents

Edit `crewai_node.py`:

```python
def create_custom_agent():
    return Agent(
        role="Your Custom Role",
        goal="What this agent does",
        backstory="Agent's background",
        verbose=True,
        llm=f"ollama/{LLM_MODEL}"
    )
```

### Modify Routing Logic

Edit `langgraph_setup.py` → `router_node()`:

```python
def router_node(state: AgentState):
    query = state.get("query", "").lower()
    
    # Add your custom keywords
    complex_keywords = ["research", "analyze", "compare"]
    
    if any(kw in query for kw in complex_keywords):
        return "complex"
    return "simple"
```

### Change LLM Model

```bash
# Pull a different model
ollama pull llama3.2:3b
ollama pull mistral:7b

# Update config.py
LLM_MODEL = "llama3.2:3b"
```

## 🛠️ Troubleshooting

### Ollama Not Running
```bash
# Start Ollama service
ollama serve
```

### Models Not Found
```bash
# Re-pull models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### Port Already in Use
```python
# Edit config.py
PORT = "7861"  # Change to different port
```

### Memory Issues
```bash
# Clear ChromaDB
rm -rf chroma_db/

# Use smaller model
ollama pull qwen2.5:3b
```

### Dependency Conflicts
```bash
# Recreate virtual environment
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Architecture Flow

```
User Query (Gradio UI)
        ↓
Router Node → Classifies: Simple vs Complex
        ↓
Memory Retrieval → Fetches relevant context from ChromaDB
        ↓
   ┌─────────────┬─────────────┐
   ↓             ↓             ↓
Simple        Complex       Research
(LLM)        (CrewAI)      (Multi-Agent)
   ↓             ↓             ↓
   └─────────────┴─────────────┘
        ↓
Validation Node → Pydantic schema check
        ↓
Memory Storage → Save conversation
        ↓
Response to User
```

## 🔒 Privacy & Security

- ✅ 100% local execution
- ✅ No API keys required
- ✅ No data sent to cloud
- ✅ All memories stored locally
- ✅ Open source codebase

## 📈 Performance Tips

1. **Use SSD storage** for faster ChromaDB queries
2. **16GB+ RAM recommended** for smooth multi-agent workflows
3. **Close other applications** when running complex tasks
4. **Use smaller models** (e.g., `qwen2.5:3b`) on limited hardware
5. **Clear old memories** periodically: `rm -rf chroma_db/`

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open Pull Request

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** - Stateful orchestration
- **CrewAI** - Multi-agent framework
- **Ollama** - Local LLM runtime
- **ChromaDB** - Vector database
- **Gradio** - Web UI framework
- **Pydantic** - Data validation

---

**Made with ❤️ for the local AI community**

For issues and questions, please open a GitHub issue.
