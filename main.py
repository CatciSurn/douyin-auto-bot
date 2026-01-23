# main.py
import time
import random
import pyautogui
from playwright.sync_api import sync_playwright
import config
import debug_utils as tool
import notify_utils as notify  # 引入我们写好的通知模块

# ================= 配置区域 (记得检查坐标！) =================
HEART_X = 1872   # 举例：左边距
HEART_Y = 437    # 举例：上边距

def is_red(r, g, b):
    return r > 200 and g < 150 and b < 150
# =======================================================

def run_bot():
    tool.log(">>> 正在连接到 Edge 浏览器...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
        except Exception as e:
            tool.log(f"连接失败: {e}")
            return

        tool.log(f">>> 已接管: {page.title()}")
        
        # === 设定 KPI ===
        try:
            target_input = input(">>> 🎯 请输入KPI目标 (默认500): ")
            target_limit = int(target_input) if target_input.strip() else 500
        except ValueError:
            target_limit = 500
            
        tool.log(f">>> 目标设定: {target_limit} 个。请确保窗口固定且不遮挡。")
        input(">>> 按【回车】开始工作...\n")

        success_count = 0

        try:
            while True:
                # === 检查 KPI 是否达成 ===
                if success_count >= target_limit:
                    tool.log(f"\n✅ KPI 达成！({success_count}/{target_limit})")
                    
                    # >>>>> 核心修改：触发通知 <<<<<
                    tool.log(">>> 正在发送通知...")
                    notify.send_all(success_count)
                    # >>>>> 修改结束 <<<<<
                    
                    break

                # ================= 1. 取色判断 =================
                is_liked = False
                color_info = "未知"
                try:
                    r, g, b = pyautogui.pixel(HEART_X, HEART_Y)
                    color_info = f"{r},{g},{b}"
                    if is_red(r, g, b):
                        is_liked = True
                except Exception:
                    is_liked = False

                # ================= 2. 执行操作 =================
                if is_liked:
                    tool.log(f"[{success_count+1}/{target_limit}] 状态：[已赞] -> 重赞")
                    page.keyboard.press(config.KEY_LIKE)
                    time.sleep(random.uniform(0.8, 1.2))
                    page.keyboard.press(config.KEY_LIKE)
                else:
                    tool.log(f"[{success_count+1}/{target_limit}] 状态：[未赞] -> 点赞")
                    page.keyboard.press(config.KEY_LIKE)

                success_count += 1

                # ================= 3. 翻页 =================
                wait_time = random.uniform(config.WAIT_MIN, config.WAIT_MAX)
                time.sleep(wait_time)
                page.keyboard.press(config.KEY_NEXT)
                time.sleep(1.5)

        except KeyboardInterrupt:
            tool.log(f"\n>>> 手动停止。完成数: {success_count}")

if __name__ == "__main__":
    run_bot()