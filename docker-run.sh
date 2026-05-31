#!/usr/bin/env bash
set -e

echo "🚀 CrewGraph-AI | Docker Deployment"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker detected!"

# Determine docker compose command
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Build and start
echo "📦 Building Docker image (this may take a few minutes)..."
$COMPOSE_CMD build

echo "🚀 Starting CrewGraph-AI container..."
$COMPOSE_CMD up -d

echo ""
echo "✅ CrewGraph-AI is now running!"
echo "🌐 Open http://localhost:7860 in your browser"
echo ""
echo "📝 Useful commands:"
echo "   View logs:          $COMPOSE_CMD logs -f"
echo "   Stop:               $COMPOSE_CMD down"
echo "   Restart:            $COMPOSE_CMD restart"
echo "   Rebuild:            $COMPOSE_CMD up -d --build"
echo ""
