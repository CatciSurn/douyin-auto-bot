@echo off
title Douyin Auto Liker (VM Side)
cd /d %~dp0

echo ==========================================
echo       Checking System Environment...
echo ==========================================

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is ready.
    goto :START_BROWSER
)

echo [WARNING] Python not found in PATH. Checking default Miniconda...

:: 2. Check standard Miniconda paths
if exist "C:\ProgramData\miniconda3\Scripts\activate.bat" (
    call "C:\ProgramData\miniconda3\Scripts\activate.bat" base
    goto :START_BROWSER
)

if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    call "%USERPROFILE%\miniconda3\Scripts\activate.bat" base
    goto :START_BROWSER
)

:: If we reach here, Python is missing
echo.
echo [ERROR] Python not found!
echo ------------------------------------------------
echo Because you are using a new user "auto", you MUST install Python again.
echo.
echo 1. Please download and install Miniconda.
echo 2. During installation, check "Add to PATH".
echo ------------------------------------------------
pause
exit /b

:START_BROWSER
echo.
echo [1/3] Cleaning up old Edge processes...
taskkill /F /IM msedge.exe /T >nul 2>&1
timeout /t 1 >nul

echo [2/3] Starting Edge Browser (Keep Logged In)...
:: Try standard Edge paths
set "EDGE_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_PATH%" (
    set "EDGE_PATH=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

if not exist "%EDGE_PATH%" (
    echo [ERROR] Microsoft Edge not found!
    pause
    exit /b
)

:: Start Edge with debugging port
start "" "%EDGE_PATH%" --remote-debugging-port=9222 https://www.douyin.com

echo.
echo [WAIT] Waiting 8 seconds for page load...
timeout /t 8

echo.
echo [3/3] Starting Python Scripts...
echo ------------------------------------------------
echo Starting Coordinate Calibration...
echo ------------------------------------------------

:: 1. 强制切换编码为 UTF-8，防止 emoji 导致批处理崩溃
chcp 65001 >nul

:: 2. 运行校准脚本
call python get_coord.py

:: 3. 无论校准脚本返回什么代码，都暂停一下让你确认
::echo.
::echo ========================================================
::echo [DEBUG] Calibration script finished.
::echo If you see errors above, close window. Otherwise, press key to run Main Bot.
::echo ========================================================
::pause

echo.
echo Starting Main Bot...
:: 4. 运行主程序
call python main.py

echo.
echo All Done.
pause

