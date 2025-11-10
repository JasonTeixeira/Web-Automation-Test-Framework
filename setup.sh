#!/bin/bash
# Quick setup script for Web Automation Test Framework

set -e

echo "🚀 Setting up Web Automation Test Framework..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium firefox webkit

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. You can customize it as needed."
else
    echo "⚠️  .env file already exists. Skipping..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p reports logs screenshots test_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run all tests: pytest tests/"
echo "  3. Run smoke tests: pytest -m smoke"
echo "  4. Generate HTML report: pytest tests/ --html=reports/report.html --self-contained-html"
echo ""
echo "For more information, see README.md"
