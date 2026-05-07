@echo off
echo ============================================
echo   Smart E-Commerce + AI Setup Script
echo ============================================
echo.

REM Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

REM Install dependencies
echo [2/5] Installing Python dependencies...
pip install -r requirements.txt

REM Create media directories
echo [3/5] Creating directories...
if not exist "media\products" mkdir media\products
if not exist "media\profiles" mkdir media\profiles
if not exist "static\images" mkdir static\images

REM Run migrations
echo [4/5] Running database migrations...
python manage.py makemigrations accounts products cart orders payments ai_engine warehouse
python manage.py migrate

REM Seed data
echo [5/5] Loading sample data...
python manage.py seed_data

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo   To start the server:
echo     .venv\Scripts\activate
echo     python manage.py runserver
echo.
echo   Admin: http://127.0.0.1:8000/admin/
echo   Site:  http://127.0.0.1:8000/
echo ============================================
pause
