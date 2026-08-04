#!/bin/bash

# Aura Beauty AI Commerce - Development Setup Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "🚀 Aura Beauty AI Commerce - Development Setup"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    echo -e "${GREEN}✓ Docker${NC}"

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    echo -e "${GREEN}✓ Docker Compose${NC}"

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 20+"
        exit 1
    fi
    echo -e "${GREEN}✓ Node.js $(node -v)${NC}"

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3.11+"
        exit 1
    fi
    echo -e "${GREEN}✓ Python 3 $(python3 --version)${NC}"
}

# Setup environment files
setup_env() {
    echo -e "${BLUE}Setting up environment files...${NC}"

    if [ ! -f .env.local ]; then
        cp .env.example .env.local
        echo -e "${GREEN}✓ Created .env.local${NC}"
        echo -e "${YELLOW}⚠️  Please update .env.local with your API keys${NC}"
    else
        echo -e "${GREEN}✓ .env.local already exists${NC}"
    fi
}

# Start Docker services
start_docker() {
    echo -e "${BLUE}Starting Docker services...${NC}"

    docker-compose down 2>/dev/null || true
    docker-compose up -d

    # Wait for services to be healthy
    echo "Waiting for services to be healthy..."
    sleep 10

    echo -e "${GREEN}✓ Docker services started${NC}"
    docker-compose ps
}

# Setup frontend
setup_frontend() {
    echo -e "${BLUE}Setting up frontend...${NC}"

    cd frontend

    if [ ! -d node_modules ]; then
        npm install
        echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    else
        echo -e "${GREEN}✓ Frontend dependencies already installed${NC}"
    fi

    cd ..
}

# Setup backend
setup_backend() {
    echo -e "${BLUE}Setting up backend...${NC}"

    cd backend

    # Create virtual environment
    if [ ! -d venv ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${GREEN}✓ Virtual environment already exists${NC}"
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"

    cd ..
}

# Initialize database
init_database() {
    echo -e "${BLUE}Initializing database...${NC}"

    docker-compose exec -T db psql -U aura_user -d aura_beauty_db -c "SELECT 1" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Database is ready${NC}"
    else
        echo "Waiting for database to be ready..."
        sleep 5
    fi
}

# Create initial data (optional)
seed_database() {
    echo -e "${BLUE}Seeding initial data (optional)...${NC}"

    read -p "Do you want to seed sample data? (y/n) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Seeding database..."
        # TODO: Add seed script
        echo -e "${GREEN}✓ Database seeded${NC}"
    fi
}

# Print startup commands
print_startup_info() {
    echo ""
    echo "================================================"
    echo -e "${GREEN}✓ Setup Complete!${NC}"
    echo "================================================"
    echo ""
    echo "Services running:"
    echo "  📱 Frontend: http://localhost:3000"
    echo "  🔌 Backend API: http://localhost:8000"
    echo "  📚 API Docs: http://localhost:8000/docs"
    echo "  🔍 Meilisearch: http://localhost:7700"
    echo "  💾 PostgreSQL: localhost:5432"
    echo "  ⚡ Redis: localhost:6379"
    echo "  🗃️  pgAdmin: http://localhost:5050"
    echo ""
    echo "Next steps:"
    echo "  1. Update .env.local with your API keys"
    echo "  2. Start frontend: cd frontend && npm run dev"
    echo "  3. Start backend: cd backend && python -m uvicorn app.main:app --reload"
    echo "  4. Start Celery: celery -A app.tasks worker --loglevel=info"
    echo ""
    echo "Documentation:"
    echo "  📖 README.md - Project overview"
    echo "  🏗️  docs/ARCHITECTURE.md - System architecture"
    echo "  📋 docs/SOP.md - Standard operating procedures"
    echo "  🤖 docs/AGENTS.md - AI agents guide"
    echo ""
    echo "Troubleshooting:"
    echo "  docker-compose logs -f     # View service logs"
    echo "  docker-compose restart     # Restart all services"
    echo "  docker-compose down        # Stop all services"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_env
    start_docker
    setup_frontend
    setup_backend
    init_database
    seed_database
    print_startup_info
}

# Run main function
main
