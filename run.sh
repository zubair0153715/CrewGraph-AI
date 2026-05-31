#!/usr/bin/env bash
set -e

echo "🚀 CrewGraph-AI | Setting up local environment..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+ first."
    exit 1
fi

if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not detected. Please install: https://ollama.com"
    echo "   Run: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 Pulling local models (first run may take a few minutes)..."
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

echo ""
echo "✅ Setup complete!"
echo "🌐 Launching UI at http://localhost:7860"
echo "💡 Keep Ollama running in another terminal: ollama serve"
echo ""
python main.py
