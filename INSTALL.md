# 🚀 CrewGraph AI - Complete Installation Guide

## Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Pull Ollama Models (One-time)
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### 3️⃣ Launch Web App
```bash
python web_app.py
```

🌐 Open **http://localhost:7860** in your browser!

---

## Detailed Installation

### Prerequisites

#### Python 3.10+
```bash
# Check Python version
python --version

# Install if needed
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.10 python3-pip

# macOS:
brew install python@3.10

# Windows: Download from python.org
```

#### Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Start Ollama service
ollama serve
```

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Install Requirements
```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### Pull Models
```bash
# Main LLM model
ollama pull qwen2.5:7b

# Embedding model for RAG/memory
ollama pull nomic-embed-text

# Optional: Larger model for better quality
ollama pull llama3:8b
```

---

## Running the Application

### Option 1: Advanced Web UI (Recommended)
```bash
python web_app.py
```
Features:
- 🔌 Connect external accounts (GitHub, Notion, etc.)
- 🔄 Pre-built workflow templates
- 🛠️ Custom workflow builder
- ⚡ One-click automation
- 📊 Real-time monitoring

### Option 2: Simple Chat Interface
```bash
python main.py
```

### Option 3: Docker
```bash
# Build and run
docker-compose up --build

# Access at http://localhost:7860
```

---

## Configuration

### Environment Variables (.env file)
Create a `.env` file in the root directory:

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
EMBEDDING_MODEL=nomic-embed-text

# Chroma DB
CHROMA_PERSIST_DIR=./chroma_db

# API Keys (Optional - for connectors)
GITHUB_TOKEN=ghp_your_token_here
NOTION_TOKEN=notion_secret_here
```

### Custom Settings (config.py)
Edit `config.py` to change:
- Default models
- Memory persistence directory
- Feature flags
- Agent configurations

---

## Connecting External Services

### GitHub
1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate token with `repo` scope
3. In Web UI: Connect Accounts → GitHub → Enter token & username

### Notion
1. Go to https://www.notion.so/my-integrations
2. Create new integration → Copy internal secret
3. Share database with your integration
4. In Web UI: Connect Accounts → Notion → Enter token & database ID

### Local File System
- Automatically enabled
- Files saved to `./workspace` folder
- Secure sandbox prevents path traversal

### Web Search
- Works out of the box (DuckDuckGo)
- No API key required

---

## Usage Examples

### 1. Simple Query
```
User: "What is machine learning?"
→ Direct answer from AI agent
```

### 2. Research Task
```
User: "Research latest AI trends in healthcare"
→ Web search → Analysis → Structured report
```

### 3. Automated Workflow
```
1. Connect GitHub account
2. Select "GitHub Issue Automation" template
3. Enter repo name
4. Run → AI monitors issues and suggests responses
```

### 4. Custom Workflow
```json
{
  "nodes": [
    {"id": "start", "type": "trigger", "next": ["search"]},
    {"id": "search", "type": "connector", "config": {"connector_name": "websearch"}},
    {"id": "analyze", "type": "agent", "config": {"agent_role": "analyst"}},
    {"id": "save", "type": "connector", "config": {"connector_name": "filesystem"}},
    {"id": "end", "type": "end"}
  ]
}
```

---

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve

# Update OLLAMA_HOST in .env if using custom port
```

### Module Not Found
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Change port in web_app.py
demo.launch(server_port=7861)  # Use different port
```

### Memory Issues
```bash
# Use smaller model
ollama pull qwen2.5:3b

# Clear Chroma DB
rm -rf chroma_db/*
```

---

## Performance Tips

### For Better Speed
- Use `qwen2.5:3b` instead of `7b`
- Enable GPU acceleration in Docker
- Reduce concurrent agents

### For Better Quality
- Use `llama3:8b` or larger models
- Increase temperature for creativity
- Add more context in queries

### For Production
- Use Docker with resource limits
- Enable HTTPS with reverse proxy
- Set up monitoring and logging
- Configure backup for Chroma DB

---

## Next Steps

1. ✅ **Explore Web UI**: Try all 5 tabs
2. ✅ **Connect Accounts**: Add GitHub/Notion for automation
3. ✅ **Run Templates**: Test pre-built workflows
4. ✅ **Build Custom**: Create your own automation
5. ✅ **Share Feedback**: Open issues on GitHub

🎉 **You're all set!** Start automating with CrewGraph AI!
