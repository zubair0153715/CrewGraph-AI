# 🌐 CrewGraph-AI Web App - Complete Installation Guide

## 🚀 Quick Start (Choose Your Method)

### Option 1: Docker (Recommended - Easiest!)
```bash
# One command to run everything!
./docker-run.sh

# Or manually:
docker-compose up -d
```
**Access:** http://localhost:7860

### Option 2: Local Python Installation
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git
cd CrewGraph-AI

# Run setup script
chmod +x run.sh
./run.sh
```
**Access:** http://localhost:7860

---

## 📋 Prerequisites

### For Docker Method:
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose (included with Docker Desktop)
- 4GB+ RAM available for container

### For Local Method:
- Python 3.10+
- 8GB+ RAM
- Ollama installed ([Download](https://ollama.com))

---

## 🔧 Detailed Installation

### Docker Installation (Cross-Platform)

#### Windows:
1. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Enable WSL2 backend in Docker settings
3. Open PowerShell or Git Bash:
   ```powershell
   git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git
   cd CrewGraph-AI
   .\docker-run.sh
   ```

#### macOS:
1. Install [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
2. Open Terminal:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git
   cd CrewGraph-AI
   chmod +x docker-run.sh
   ./docker-run.sh
   ```

#### Linux:
1. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   ```
2. Logout and login again, then:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CrewGraph-AI.git
   cd CrewGraph-AI
   chmod +x docker-run.sh
   ./docker-run.sh
   ```

### Local Python Installation

#### Step 1: Install Ollama
**Windows:** Download from [ollama.com](https://ollama.com)  
**macOS:** `brew install ollama`  
**Linux:** `curl -fsSL https://ollama.com/install.sh | sh`

#### Step 2: Pull Required Models
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

#### Step 3: Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Run the Application
```bash
# Standard mode
python main.py

# Advanced mode (all features)
python main_advanced.py
```

---

## 🎨 Web Interface Features

Once running, access http://localhost:7860 for:

### 💬 Chat Interface
- Real-time streaming responses
- Conversation history
- Copy/paste functionality
- Markdown rendering

### 🤖 Agent Selection
- **Auto** - Smart routing based on query complexity
- **Researcher** - Deep research & analysis
- **Writer** - Content creation & editing
- **Analyst** - Data analysis & insights
- **Coder** - Code generation & debugging
- **Reviewer** - Quality assurance

### 📁 Document Upload
- PDF, TXT, MD files supported
- Automatic text extraction
- Context-aware processing

### ⚙️ Advanced Settings
- Temperature control (creativity vs accuracy)
- Mode selection (Standard/Advanced)
- Session statistics tracking

---

## 🔍 Usage Examples

### Simple Queries (Auto-routed):
```
"Hello!"
"What is Python?"
"Explain quantum computing in simple terms"
```

### Complex Research Tasks:
```
"Research and analyze the impact of AI on healthcare in 2024"
"Compare microservices vs monolithic architecture with examples"
"Create a comprehensive guide to machine learning for beginners"
```

### Code Generation:
```
"Write a Python Flask API with authentication"
"Create a React component for a todo list with drag-and-drop"
"Debug this code: [paste your code]"
```

### Document Analysis:
1. Upload a PDF/TXT file
2. Ask questions about the content
3. Get summarized insights

---

## 🛠️ Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "7861:7860"  # Use 7861 instead
```

### Local Installation Issues

**Ollama connection error:**
```bash
# Restart Ollama service
# Windows: Restart Ollama app
# Mac: brew services restart ollama
# Linux: systemctl restart ollama
```

**Model not found:**
```bash
# Re-pull models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

**Memory errors:**
- Close other applications
- Use smaller model: `ollama pull qwen2.5:1.5b`
- Update config.py to reduce batch size

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| CPU | 4 cores | 8+ cores |
| Storage | 10GB | 20GB+ SSD |
| OS | Windows 10 / macOS 11 / Linux | Latest versions |

---

## 🔄 Updates

### Docker:
```bash
docker-compose pull
docker-compose up -d
```

### Local:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🆘 Support

- **Documentation:** See README.md
- **Issues:** Open on GitHub
- **Discussions:** GitHub Discussions tab

---

## 🎯 Next Steps

1. ✅ Install using Docker or local method
2. ✅ Open http://localhost:7860
3. ✅ Try example queries
4. ✅ Upload documents for analysis
5. ✅ Customize settings for your needs
6. ✅ Share with your team!

**Enjoy your local AI powerhouse!** 🚀
