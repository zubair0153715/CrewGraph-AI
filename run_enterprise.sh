#!/usr/bin/env bash
set -e

echo "🚀 CrewGraph-AI Enterprise v2.0 - Setting up..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.10+ first."
    exit 1
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not installed. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 Pulling AI models (first run takes time)..."
ollama pull qwen2.5:7b
ollama pull llava:7b
ollama pull nomic-embed-text

echo "✅ Setup complete! Launching Enterprise Web UI..."
echo "🌐 Open http://localhost:7860 in your browser"
python main_enterprise.py
