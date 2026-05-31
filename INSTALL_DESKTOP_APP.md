# 🖥️ CrewGraph-AI Desktop App - Installation Guide

## 📥 Download Ready-Made Installers (Recommended)

**No setup required!** Just download and install like any other app.

### Windows (.msi)
```bash
# Download from GitHub Releases
https://github.com/zubair0153715/CrewGraph-AI/releases/download/v3.0.0/CrewGraph-AI_3.0.0_x64_en-US.msi
```

### macOS (.dmg)
```bash
# Download from GitHub Releases
https://github.com/zubair0153715/CrewGraph-AI/releases/download/v3.0.0/CrewGraph-AI_3.0.0_aarch64.dmg
```

### Linux (.AppImage)
```bash
# Download from GitHub Releases
wget https://github.com/zubair0153715/CrewGraph-AI/releases/download/v3.0.0/CrewGraph-AI_3.0.0_amd64.AppImage
chmod +x CrewGraph-AI_3.0.0_amd64.AppImage
./CrewGraph-AI_3.0.0_amd64.AppImage
```

### Linux (.deb - Ubuntu/Debian)
```bash
wget https://github.com/zubair0153715/CrewGraph-AI/releases/download/v3.0.0/crewgraph-ai_3.0.0_amd64.deb
sudo dpkg -i crewgraph-ai_3.0.0_amd64.deb
```

### Linux (.rpm - Fedora/RHEL)
```bash
wget https://github.com/zubair0153715/CrewGraph-AI/releases/download/v3.0.0/crewgraph-ai-3.0.0-1.x86_64.rpm
sudo dnf install crewgraph-ai-3.0.0-1.x86_64.rpm
```

---

## 🛠️ Build From Source (Advanced Users)

If you want to build the desktop app yourself:

### Prerequisites

#### 1. Install Rust
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### 2. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y libwebkit2gtk-4.1-dev \
    build-essential \
    curl \
    wget \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libsoup2.4-dev \
    libjavascriptcoregtk-4.1-dev
```

**Fedora:**
```bash
sudo dnf install -y webkit2gtk4.1-devel \
    openssl-devel \
    gtk3-devel \
    libappindicator-gtk3-devel \
    librsvg2-devel \
    libsoup2.4-devel
```

**macOS:**
```bash
xcode-select --install
```

#### 3. Install Node.js & Tauri CLI
```bash
# Install Node.js (v18+)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Tauri CLI
npm install -D @tauri-apps/cli
npm install -g @tauri-apps/cli
```

#### 4. Install Python Dependencies
```bash
cd CrewGraph-AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 5. Pull Ollama Models
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
ollama pull llava
```

### Build Commands

#### Development Mode (Hot Reload)
```bash
cd src-tauri
npm run tauri dev
```

#### Production Build (Creates Installers)
```bash
cd src-tauri
npm run tauri build
```

After building, find your installers in:
- **Windows:** `src-tauri/target/release/bundle/msi/`
- **macOS:** `src-tauri/target/release/bundle/dmg/`
- **Linux:** `src-tauri/target/release/bundle/`

---

## 🚀 First Launch

1. **Install the app** using one of the methods above
2. **Open CrewGraph-AI** from your applications menu
3. **Wait for initialization** (first launch may take 1-2 minutes)
4. **Start creating agents!**

### Default Settings
- **Port:** 7860 (internal)
- **Models:** qwen2.5:7b, nomic-embed-text
- **Memory:** ChromaDB (local)
- **Storage:** ~/.crewgraph-ai/

---

## ⚙️ Configuration

Create a `.env` file in the app directory:

```bash
# Ollama Settings
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
EMBEDDING_MODEL=nomic-embed-text

# Optional: API Keys for Connectors
GITHUB_TOKEN=your_github_token
NOTION_TOKEN=your_notion_token
```

---

## 🐛 Troubleshooting

### App Won't Start
```bash
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve
```

### Port Already in Use
```bash
# Kill process on port 7860
lsof -ti:7860 | xargs kill -9
```

### Models Not Found
```bash
# Re-pull models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### Linux: Permission Denied
```bash
chmod +x CrewGraph-AI*.AppImage
```

---

## 📦 What's Included

✅ **Full AI Engine** - LangGraph + CrewAI  
✅ **Web UI** - Gradio-based interface  
✅ **Universal Agents** - 50+ pre-built roles  
✅ **Connectors** - GitHub, Notion, Web Search  
✅ **Vision & Voice** - Image analysis, Speech-to-Text  
✅ **Workflow Builder** - Visual automation designer  
✅ **Local Memory** - ChromaDB RAG system  
✅ **100% Offline** - No internet required (except web search)  

---

## 🎯 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10, macOS 11, Ubuntu 20.04 | Windows 11, macOS 13, Ubuntu 22.04 |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 10 GB | 20 GB SSD |
| **CPU** | 4 cores | 8 cores |
| **GPU** | Optional | NVIDIA RTX (for faster inference) |

---

## 📞 Support

- **GitHub Issues:** https://github.com/zubair0153715/CrewGraph-AI/issues
- **Discussions:** https://github.com/zubair0153715/CrewGraph-AI/discussions
- **Documentation:** https://github.com/zubair0153715/CrewGraph-AI/wiki

---

## 🔄 Updates

The app will check for updates automatically. You can also manually check:
- **Windows/macOS:** Help → Check for Updates
- **Linux:** Run the new AppImage or update the .deb/.rpm package

---

**Enjoy your fully autonomous AI desktop application!** 🎉
