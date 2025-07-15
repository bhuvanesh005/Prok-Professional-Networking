#!/bin/bash

# Posts Listing Demo Startup Script
# This script will start both backend and frontend for testing the posts listing functionality

echo "🚀 Starting Posts Listing Demo..."
echo "=================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python 3 is installed
if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Start Backend
echo ""
echo "🔧 Starting Backend Server..."
cd app/backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run the backend setup first."
    exit 1
fi

# Activate virtual environment and start backend
echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "🗄️  Setting up database..."
python main.py &
BACKEND_PID=$!

echo "✅ Backend started with PID: $BACKEND_PID"
echo "🌐 Backend will be available at: http://localhost:5000"

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Backend is running successfully!"
else
    echo "⚠️  Backend might still be starting up..."
fi

# Start Frontend
echo ""
echo "🎨 Starting Frontend Server..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting development server..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Frontend started with PID: $FRONTEND_PID"
echo "🌐 Frontend will be available at: http://localhost:5173"

# Wait a moment for frontend to start
sleep 5

# Check if frontend is running
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Frontend is running successfully!"
else
    echo "⚠️  Frontend might still be starting up..."
fi

echo ""
echo "🎉 Posts Listing Demo is now running!"
echo "======================================"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5000"
echo "📄 Posts Page: http://localhost:5173/posts"
echo ""
echo "🧪 To test the API endpoints, run:"
echo "   cd app/backend && source venv/bin/activate && python test_api.py"
echo ""
echo "📊 To add sample posts, run:"
echo "   cd app/backend && source venv/bin/activate && python sample_posts.py"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped."
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep the script running
wait 