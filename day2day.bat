@echo off
echo Starting Day-2-Day backend...

cd backend
call venv\Scripts\activate

cd src
echo Running backend server...
start cmd /k "python -m calendar_app.app"

echo Opening browser...
start http://localhost:5000

echo Day-2-Day is running!