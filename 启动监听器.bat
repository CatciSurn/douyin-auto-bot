@echo off
title 宿主机通知监听器
cd /d %~dp0

echo >>> 正在启动监听服务...
echo >>> 请确保此窗口不要关闭，否则收不到通知。

:: 运行监听 Python 脚本
call C:\Users\CatciSurn\miniconda3\Scripts\activate.bat base
python host_listener.py

pause