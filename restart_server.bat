@echo off
chcp 65001 >nul
echo Activating virtual environment...
call C:\FastAPI\Fems_FastAPI\.venv\Scripts\activate

echo [1/3] Stopping existing uvicorn process...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    echo Killing PID %%a...
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

echo [2/3] Cleaning up processes...
taskkill /IM uvicorn.exe /F >nul 2>&1
timeout /t 2 /nobreak >nul

echo [3/3] Starting server...
start /b uvicorn fems_fastApi.web.application:get_app --host 0.0.0.0 --port 8000 --factory

echo Server started. (http://0.0.0.0:8000)
