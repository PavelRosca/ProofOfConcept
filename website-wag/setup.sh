#!/bin/bash
# Django Backend Setup Script

set -e

echo "================================"
echo "Partito Politico - Backend Setup"
echo "================================"
echo ""

# Check if running from correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the back-end directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env created - Please edit it with your settings"
else
    echo "✅ .env file already exists"
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
    source venv/bin/activate
fi

# Install requirements
echo "📦 Installing Python requirements..."
pip install -r requirements.txt
echo "✅ Requirements installed"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate
echo "✅ Migrations applied"

# Create superuser
echo ""
echo "👤 Creating superuser (admin account)..."
python manage.py createsuperuser

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📌 Next steps:"
echo "1. Start development server:"
echo "   python manage.py runserver"
echo ""
echo "2. Open admin panel:"
echo "   http://localhost:8000/admin"
echo ""
echo "3. Start adding data to the website!"
echo ""
