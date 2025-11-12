# Quick Start Script for AI Recruitment Enhancement Microservice
# Run this script to set up and start the application

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "AI-Powered Recruitment Enhancement Microservice" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10 or higher" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
Write-Host ""
Write-Host "[2/6] Setting up virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/6] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install --quiet --upgrade pip
pip install --quiet fastapi uvicorn pydantic python-multipart
Write-Host "✓ Core dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "[5/6] Setting up configuration..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    Write-Host "  Note: Edit .env to add your API keys" -ForegroundColor Gray
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Start the application
Write-Host ""
Write-Host "[6/6] Starting the application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Server starting on http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run the application
python main.py
