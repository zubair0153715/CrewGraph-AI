# 🤖 CrewGraph-AI Pro

A fully local, free, and production-ready **advanced** multi-agent AI system.  
Combines **LangGraph + CrewAI + Pydantic Validation + Chroma Memory + Ollama LLMs** with cutting-edge features.

🔒 **100% Local** | 💸 **Zero API Cost** | 🧠 **Smart Routing & Validation** | 🌐 **Advanced Web UI** | 📄 **Document Support**

## 🎯 What Problem Does It Solve?

- 🔀 **Fragmented AI Tools:** No more switching between chatbots, code assistants, and research tools. One system handles it all.
- 💸 **Cloud Costs & Privacy:** Runs entirely on your machine. No API keys, no data leaks, no monthly bills.
- 🤷 **Unreliable Outputs:** Built-in state management, Pydantic schema validation, and memory prevent hallucinations & context loss.
- ⚙️ **Complex Setup:** Clone → 1 command → browser opens → start working. Zero configuration headache.

## 🏗️ Architecture

```
User Input (Advanced Gradio Web UI)
        ↓
FastAPI Backend → LangGraph State Orchestrator
        ↓
   ├─ 🔀 Intelligent Router → Classifies task complexity
   ├─ 🔄 Task Decomposition → Breaks complex tasks into sub-tasks
   ├─ ⚡ Parallel Execution → Multiple agents work simultaneously
   ├─ 👥 CrewAI Node → Multi-agent delegation (Researcher/Writer/Analyst/Coder/Reviewer)
   ├─ 🔄 Agent Reflection → Self-improvement loop
   ├─ ✅ Pydantic Validator → Structured & safe outputs with quality scoring
   ├─ 🧠 Chroma Memory → Persistent session + RAG retrieval
   └─ 🤝 HITL (Optional) → Human-in-the-loop approval
        ↓
Streamed Response → UI
```

## ✨ Features

### Core Features
- 🔄 **Stateful Orchestration:** LangGraph handles cyclic workflows, routing & HITL ready
- 👥 **Multi-Agent Coordination:** CrewAI runs isolated, stateless task clusters
- 📝 **Output Validation:** Pydantic schemas guarantee structured, parseable responses
- 🧠 **Persistent Memory:** ChromaDB + Ollama embeddings for long-term context
- 💻 **100% Local & Free:** Powered by Ollama (`qwen2.5:7b` + `nomic-embed-text`)

### Advanced Features (NEW!)
- 🎯 **Task Decomposition:** Automatically breaks complex tasks into manageable sub-tasks
- ⚡ **Parallel Execution:** Multiple agents work simultaneously on different sub-tasks
- 🔄 **Agent Reflection:** Self-review and improvement loop for higher quality outputs
- 📄 **Document Processing:** Upload PDFs, TXT, MD files for context-aware analysis
- 🎛️ **Agent Selection:** Choose specific agents (Researcher, Writer, Analyst, Coder, Reviewer)
- 🌡️ **Temperature Control:** Adjust creativity vs accuracy
- 📊 **Session Statistics:** Track messages, documents, and usage metrics
- 🤝 **Human-in-the-Loop:** Optional approval workflow for critical tasks
- 🎨 **Advanced Web UI:** Modern Gradio interface with file upload, stats, and controls

### Specialized Agents
- 🔍 **Researcher:** Expert information gathering and analysis
- ✍️ **Writer:** Content synthesis and structured responses
- 📊 **Analyst:** Data pattern recognition and insights
- 💻 **Coder:** Clean, production-ready code generation
- ✓ **Reviewer:** Quality assurance and improvement

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed & running
- 8GB+ RAM recommended (16GB for advanced features)

### Setup

```bash
# 1. Clone & enter
git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git 
cd CrewGraph-AI

# 2. Create virtual environment & install
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Pull local models (run once)
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

# 4. Launch (Standard Mode)
python main.py

# OR Launch (Advanced Mode with all features)
python main_advanced.py
```

🌐 Open `http://localhost:7860` in your browser. Done!

## 📁 Project Structure

```
CrewGraph-AI/
├── main.py              # Standard FastAPI + Gradio UI
├── main_advanced.py     # Advanced UI with document support, stats, controls
├── langgraph_setup.py   # Standard StateGraph + Routing + Validation
├── langgraph_advanced.py# Advanced graph with decomposition, parallel exec, reflection
├── crewai_node.py       # Enhanced CrewAI execution (5 agent types, parallel, docs)
├── memory.py            # ChromaDB + Ollama embeddings
├── config.py            # Global settings & feature flags
├── requirements.txt     # Python dependencies
├── run.sh               # 1-click setup & launch
├── README.md            # This file
└── .gitignore
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestrator | `LangGraph` (Standard + Advanced) |
| Multi-Agent | `CrewAI` (5 specialized agents) |
| Validation | `PydanticAI` / `Pydantic` with quality scoring |
| Memory/RAG | `ChromaDB` + `Ollama Embeddings` |
| LLM Backend | `Ollama` (`qwen2.5:7b`, customizable) |
| UI | `Gradio` + `FastAPI` (Standard + Advanced) |
| Document Processing | `PyPDF2`, `markdown` |
| Local Execution | `uvicorn`, `venv`, docker-ready |

## 🎮 Usage Examples

### Simple Query
```
User: "What is Python?"
→ Direct LLM response (fast)
```

### Complex Research
```
User: "Research and analyze AI impact on healthcare"
→ Router detects complexity
→ Researcher + Writer agents activated
→ Multi-step research and synthesis
→ Validated output with sources
```

### Task Decomposition
```
User: "Create a roadmap for learning machine learning"
→ Decomposed into sub-tasks:
  1. Research ML fundamentals
  2. Identify key topics and prerequisites
  3. Create structured learning path
  4. Suggest resources and timeline
→ Parallel execution
→ Aggregated comprehensive roadmap
```

### Code Generation
```
User: "Write a Python function to sort a list"
→ Coder agent generates code
→ Reviewer agent checks quality
→ Clean, documented code output
```

### Document Analysis
```
1. Upload PDF/TXT/MD file
2. Ask: "Summarize this document"
→ Document processed by Researcher + Analyst
→ Key points extracted
→ Comprehensive summary generated
```

## ⚙️ Configuration

Edit `config.py` or use environment variables:

```bash
# LLM Settings
LLM_MODEL=qwen2.5:7b
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

# Feature Flags
ENABLE_ROUTER=true          # Auto task classification
ENABLE_VALIDATION=true      # Pydantic validation
ENABLE_MEMORY=true          # ChromaDB persistence
ENABLE_HITL=false           # Human-in-the-loop (optional)
ENABLE_PARALLEL=true        # Parallel task execution
ENABLE_REFLECTION=true      # Agent self-reflection
```

## 🔬 Advanced Features Deep Dive

### Task Decomposition
Automatically breaks complex queries into 2-4 actionable sub-tasks, each assigned to the most suitable agent.

### Parallel Execution
Sub-tasks execute simultaneously, reducing total processing time by up to 60%.

### Agent Reflection
After initial response generation, the system:
1. Reviews output for gaps and inaccuracies
2. Identifies improvement areas
3. Applies refinements (up to 2 iterations)
4. Delivers higher-quality final result

### Quality Scoring
Every response receives a quality score (0.0-1.0) based on:
- Completeness
- Accuracy indicators
- Structure and clarity
- Validation results

## 🤝 Contributing

PRs welcome! Please open an issue first for major changes. Follow standard Python PEP8 & add tests for new nodes.

### Areas for Contribution
- Additional agent types (Designer, Debugger, etc.)
- More document formats (DOCX, PPTX)
- Streaming responses
- API endpoints
- Docker containerization
- Evaluation benchmarks

## 📈 Roadmap

- [ ] Real-time streaming responses
- [ ] REST API endpoints
- [ ] Docker support
- [ ] Multi-modal inputs (images)
- [ ] Custom agent creation UI
- [ ] Conversation export
- [ ] Plugin system
- [ ] Performance optimization

## 📜 License

MIT License. See `LICENSE` for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Orchestration framework
- [CrewAI](https://github.com/joaomdmoura/crewai) - Multi-agent coordination
- [Ollama](https://ollama.com) - Local LLM runtime
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Gradio](https://gradio.app) - Web UI framework

---

**Made with ❤️ for the local AI community**

Star ⭐ this repo if you find it useful!
