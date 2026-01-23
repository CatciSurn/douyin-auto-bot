
# get_coord.py
import pyautogui
import time
import os

print(">>> 坐标校准工具启动")
print(">>> 请将鼠标移动到【点赞红心】的中心位置...")
print(">>> 按 Ctrl+C 退出")

try:
    while True:
        # 获取鼠标当前坐标
        x, y = pyautogui.position()
        
        # 获取该点的颜色
        # 注意：MacOS/Linux可能需要权限，Windows通常直接可用
        try:
            r, g, b = pyautogui.pixel(x, y)
            color_str = f"RGB({r}, {g}, {b})"
        except:
            color_str = "颜色获取失败"

        # 打印信息 (使用 \r 实现单行刷新)
        print(f"\r当前坐标: X={x}, Y={y} | 颜色: {color_str}   ", end="")
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n>>> 已退出。请把上面的坐标填入 main.py")