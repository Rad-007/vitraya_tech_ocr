@echo off
REM Navigate to the backend directory and activate the virtual environment
cd backend
//call venv\Scripts\activate

REM Set environment variables (if needed)
REM set FLASK_APP=app.py

REM Start the backend server
start cmd /k "flask run"

REM Navigate to the frontend directory
cd ../frontend

REM Start the frontend server
start cmd /k "npm start"

REM Go back to the root directory
cd ..
