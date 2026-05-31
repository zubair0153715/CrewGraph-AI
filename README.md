# 🤖 CrewGraph-AI

A fully local, free, and production-ready multi-agent AI system.  
Combines **LangGraph + CrewAI + Pydantic Validation + Chroma Memory + Ollama LLMs** in one seamless workflow.

🔒 **100% Local** | 💸 **Zero API Cost** | 🧠 **Smart Routing & Validation** | 🌐 **Web UI Built-in**

## 🎯 What Problem Does It Solve?

- 🔀 **Fragmented AI Tools:** No more switching between chatbots, code assistants, and research tools. One system handles it all.
- 💸 **Cloud Costs & Privacy:** Runs entirely on your machine. No API keys, no data leaks, no monthly bills.
- 🤷 **Unreliable Outputs:** Built-in state management, Pydantic schema validation, and memory prevent hallucinations & context loss.
- ⚙️ **Complex Setup:** Clone → 1 command → browser opens → start working. Zero configuration headache.

## 🏗️ Architecture

```
User Input (Gradio Web UI)
        ↓
FastAPI Backend → LangGraph State Orchestrator
        ↓
   ├─ 🔀 Router → Classifies task complexity
   ├─ 👥 CrewAI Node → Multi-agent delegation (Research/Synthesis)
   ├─ ✅ Pydantic Validator → Structured & safe outputs
   └─ 🧠 Chroma Memory → Persistent session + RAG retrieval
        ↓
Streamed Response → UI
```

## ✨ Features

- 🔄 **Stateful Orchestration:** LangGraph handles cyclic workflows, routing & HITL ready
- 👥 **Multi-Agent Coordination:** CrewAI runs isolated, stateless task clusters
- 📝 **Output Validation:** Pydantic schemas guarantee structured, parseable responses
- 🧠 **Persistent Memory:** ChromaDB + Ollama embeddings for long-term context
- 💻 **100% Local & Free:** Powered by Ollama (`qwen2.5:7b` + `nomic-embed-text`)
- 🌐 **Zero-Config UI:** Gradio web interface, responsive & streaming-ready
- 🛡️ **Production Ready:** Docker-friendly, eval-ready, extensible node architecture

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed & running
- 8GB+ RAM recommended

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

# 4. Launch
python main.py
```

🌐 Open `http://localhost:7860` in your browser. Done.

## 📁 Project Structure

```
CrewGraph-AI/
├── main.py              # FastAPI + Gradio UI
├── langgraph_setup.py   # StateGraph + Routing + Validation
├── crewai_node.py       # Isolated CrewAI execution node
├── memory.py            # ChromaDB + Ollama embeddings
├── config.py            # Global settings & env vars
├── requirements.txt     # Python dependencies
├── run.sh               # 1-click setup & launch
├── README.md            # This file
└── .gitignore
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestrator | `LangGraph` |
| Multi-Agent | `CrewAI` (stateless node) |
| Validation | `PydanticAI` / `Pydantic` |
| Memory/RAG | `ChromaDB` + `Ollama Embeddings` |
| LLM Backend | `Ollama` (`qwen2.5:7b`) |
| UI | `Gradio` + `FastAPI` |
| Local Execution | `uvicorn`, `venv`, `docker` ready |

## 🤝 Contributing

PRs welcome! Please open an issue first for major changes. Follow standard Python PEP8 & add tests for new nodes.

## 📜 License

MIT License. See `LICENSE` for details.