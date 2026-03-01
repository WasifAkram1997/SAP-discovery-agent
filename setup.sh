#!/bin/bash
# One-command setup for SAP Process Discovery

echo "🚀 SAP Process Discovery - Automated Setup"
echo "==========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found. Make sure PostgreSQL is installed and running."
fi

echo ""
echo "[1/3] Setting up Backend..."
cd backend

# Create venv
python3 -m venv venv

# Activate (OS-specific)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
fi

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys!"
fi

# Run database migration
echo "Setting up database..."
python run_migration.py

cd ..

echo ""
echo "[2/3] Setting up Frontend..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env with your API keys"
echo "  2. Start backend:  cd backend && python api/main.py"
echo "  3. Start frontend: cd frontend && npm run dev"
echo ""
echo "📚 See docs/QUICKSTART.md for detailed instructions"
