@echo off
echo 🚀 Starting DevOps Automation Hub (Simple Version)
echo ================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    echo.
    echo 📋 Steps to fix:
    echo 1. Open Docker Desktop
    echo 2. Wait for it to fully start
    echo 3. Run this script again
    pause
    exit /b 1
)

echo ✅ Docker is running!

REM Create directories
if not exist logs mkdir logs
if not exist monitoring mkdir monitoring

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env >nul 2>&1
    if %errorlevel% neq 0 (
        echo 📝 Creating basic .env file...
        echo DATABASE_URL=postgresql://devops_user:devops_password@postgres:5432/devops_automation > .env
        echo FLASK_ENV=development >> .env
        echo SECRET_KEY=dev_secret_key_change_in_production >> .env
    )
)

echo 🔨 Starting services...
docker-compose up -d --build

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo.
echo 🎉 DevOps Automation Hub should be starting!
echo ==========================================
echo 📊 Main Dashboard: http://localhost:5000
echo 📋 Health Check: http://localhost:5000/api/health
echo.
echo 📖 Check status: docker-compose ps
echo 📖 View logs: docker-compose logs -f
echo 🛑 Stop services: docker-compose down
echo.
pause
