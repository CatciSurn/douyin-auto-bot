# get_coord.py
import pyautogui
import time
import re
import os

def update_main_py(new_x, new_y):
    file_path = 'main.py'
    
    if not os.path.exists(file_path):
        print(f"❌ 错误: 找不到 {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则替换 HEART_X 和 HEART_Y 的值
    content_new = re.sub(r'HEART_X\s*=\s*\d+', f'HEART_X = {new_x}', content)
    content_new = re.sub(r'HEART_Y\s*=\s*\d+', f'HEART_Y = {new_y}', content_new)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f"✅ 坐标已自动写入 main.py: ({new_x}, {new_y})")

def main():
    print(">>> 坐标校准工具启动")
    print(">>> 请将鼠标移动到【点赞红心】的中心位置。")
    print(">>> 移动到位后，请不要移动鼠标，用另一只手按【回车键】确认...")
    
    # 这里会阻塞程序，直到你按下回车
    input()

    # 按下回车后立即抓取坐标
    final_x, final_y = pyautogui.position()
    
    # 获取颜色仅用于展示
    try:
        r, g, b = pyautogui.pixel(final_x, final_y)
        color_str = f"RGB({r}, {g}, {b})"
    except:
        color_str = "颜色未知"

    print(f"\n🎯 锁定坐标: X={final_x}, Y={final_y} | 颜色: {color_str}")
    
    # 执行写入操作
    update_main_py(final_x, final_y)
    
    print(">>> 校准完成，2秒后自动退出...")
    time.sleep(2)

if __name__ == "__main__":
    main()
