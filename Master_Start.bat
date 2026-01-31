@echo off
:: 强制切换为 UTF-8 编码，防止中文乱码和语法解析错误
chcp 65001 >nul
title 抖音自动化 - 总控台 (Ultimate Fix)
cd /d %~dp0

:: ================= 1. Miniconda 配置 =================
:: 请填入你之前查到的 miniconda 路径 (不要带引号)
:: 例如: C:\Users\CatciSurn\miniconda3
set CONDA_PATH=C:\Users\CatciSurn\miniconda3

:: ================= 2. VirtualBox 配置 =================
set VBOX_PATH="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
set VM_NAME="win10"

:: 虚拟机登录账号 (必须是当前登录桌面的账号)
set VM_USER=auto
set VM_PASS=123456

:: 虚拟机脚本路径
set VM_SCRIPT="C:\DouyinAutoLike\一键启动.bat"
:: =====================================================

echo.
echo [1/2] 正在启动宿主机监听服务 (Conda环境)...

:: 检查 Conda 路径是否存在，防止闪退
if not exist "%CONDA_PATH%\Scripts\activate.bat" (
    echo.
    echo ❌ 错误: 找不到 Miniconda，请检查 CONDA_PATH 路径是否正确!
    pause
    exit
)

:: 使用 call 激活 base 环境，然后运行 python
start "Host Listener" cmd /k "call "%CONDA_PATH%\Scripts\activate.bat" base && python host_listener.py"

echo.
echo [2/2] 正在呼叫虚拟机执行任务...

:: --- VBox 7.x 专用语法 ---
:: 使用 -- 将参数隔开，并用 /c start 确保宿主机不卡死
%VBOX_PATH% guestcontrol %VM_NAME% run ^
  --username %VM_USER% ^
  --password %VM_PASS% ^
  --exe "C:\Windows\System32\cmd.exe" ^
  -- /c start /max "" %VM_SCRIPT%

if %errorlevel% equ 0 (
    echo.
    echo >>> ✅ 指令已发送！
    echo >>> 请切换到虚拟机查看运行情况。
) else (
    echo.
    echo >>> ❌