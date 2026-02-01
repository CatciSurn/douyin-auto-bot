@echo off
:: 强制切换为 UTF-8 编码
chcp 65001 >nul
title 抖音自动化 - 总控台 (SchTasks Edition)
cd /d %~dp0

:: ================= 1. Miniconda 配置 =================
:: 请填入你之前查到的 miniconda 路径 (不要带引号)
set CONDA_PATH=C:\Users\CatciSurn\miniconda3

:: ================= 2. VirtualBox 配置 =================
set VBOX_PATH="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
set VM_NAME="win10"

:: 虚拟机登录账号 (必须是当前登录桌面的账号)
set VM_USER=auto
set VM_PASS=123456

:: 【重要修改】这里不再指定 .bat 路径，而是指定虚拟机内的“任务计划名称”
:: 请确保虚拟机里创建的任务名称与此处一致（建议使用英文，避免乱码）
set VM_TASK_NAME="DouyinAutoTask" 
:: =====================================================

echo.
echo [1/2] 正在启动宿主机监听服务 (Conda环境)...

:: 检查 Conda 路径
if not exist "%CONDA_PATH%\Scripts\activate.bat" (
    echo.
    echo ❌ 错误: 找不到 Miniconda，请检查 CONDA_PATH 路径是否正确!
    pause
    exit
)

:: 启动监听器
start "Host Listener" cmd /k "call "%CONDA_PATH%\Scripts\activate.bat" base && python host_listener.py"

echo.
echo [2/2] 正在呼叫虚拟机执行任务计划...

:: --- VBox 7.x 专用语法 (SchTasks 版本) ---
:: 原理：利用 guestcontrol 调用虚拟机里的 schtasks.exe 来触发已配置好的任务
:: --exe 指定虚拟机里的程序路径
:: -- 后面跟的是传给 schtasks.exe 的参数：/run /tn "任务名称"
%VBOX_PATH% guestcontrol %VM_NAME% run ^
  --username %VM_USER% ^
  --password %VM_PASS% ^
  --exe "C:\Windows\System32\schtasks.exe" ^
  -- /run /tn %VM_TASK_NAME%

if %errorlevel% equ 0 (
    echo.
    echo >>> ✅ 任务触发指令已发送！
    echo >>> 虚拟机应该正在启动自动化程序...
) else (
    echo.
    echo >>> ❌ 指令发送失败，请检查：
    echo 1. 虚拟机是否已开机？
    echo 2. 账号密码是否正确？
    echo 3. 任务计划名称 "%VM_TASK_NAME%" 是否在虚拟机里存在？
)

pause
