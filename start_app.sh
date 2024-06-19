#!/bin/bash
#source venv/bin/activate
# Navigate to the backend directory and activate the virtual environment
cd backend


# Set environment variables (if needed)
# export FLASK_APP=app.py

# Start the backend server
gnome-terminal -- bash -c "flask run; exec bash"

# Navigate to the frontend directory
cd ../frontend

# Start the frontend server
gnome-terminal -- bash -c "npm start; exec bash"

# Go back to the root directory
cd ..
