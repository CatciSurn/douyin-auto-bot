# main.py
import time
import random
import pyautogui
from playwright.sync_api import sync_playwright
import config
import debug_utils as tool
import notify_utils as notify

# ================= 配置区域 =================
HEART_X = 1872
HEART_Y = 437

def is_red(r, g, b):
    return r > 200 and g < 150 and b < 150
# ===========================================

def run_bot():
    tool.log("[INFO] Connecting to Edge Browser...")
    
    with sync_playwright() as p:
        try:
            # 连接浏览器
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            # 获取当前上下文的第一个页面
            context = browser.contexts[0]
            if not context.pages:
                tool.log("[ERROR] No pages found. Please open a tab.")
                return
            page = context.pages[0]
            
            # 【关键修复1】强制将页面前置，确保活跃
            page.bring_to_front()
            
        except Exception as e:
            tool.log(f"[ERROR] Connection failed: {e}")
            return

        tool.log(f"[INFO] Controlled Page: {page.title()}")
        
        # === 设定 KPI ===
        try:
            target_input = input(">>> KPI Target (Default 500): ")
            target_limit = int(target_input) if target_input.strip() else 500
        except ValueError:
            target_limit = 500
            
        tool.log(f"[INFO] Target set to {target_limit}. ensure window is visible.")
        input(">>> Press [ENTER] to start...\n")

        success_count = 0

        # 【关键修复2】定义一个聚焦函数
        # 抖音的视频容器通常是这个类名，或者我们直接聚焦 body 也可以尝试
        # 但最稳妥的是聚焦到视频容器上
        def ensure_focus():
            try:
                # 尝试聚焦到视频播放器外层容器 (抖音网页版常见容器)
                # 如果这个selector不起作用，可以换成 'body' 或者 '#slider-video'
                page.focus("body") 
                # 或者显式点击一下屏幕中心(Playwright层面的点击，不抢鼠标)
                # page.mouse.click(960, 540) 
            except Exception:
                pass

        try:
            while True:
                if success_count >= target_limit:
                    tool.log(f"\n[SUCCESS] KPI Reached! ({success_count}/{target_limit})")
                    tool.log("[INFO] Sending notification...")
                    notify.send_all(success_count)
                    break

                # ================= 1. 取色判断 =================
                is_liked = False
                try:
                    # 使用 PyAutoGUI 进行取色（这是不抢焦点的）
                    r, g, b = pyautogui.pixel(HEART_X, HEART_Y)
                    if is_red(r, g, b):
                        is_liked = True
                except Exception:
                    is_liked = False

                # ================= 2. 执行操作 =================
                
                # 【关键修复3】操作前确保焦点
                ensure_focus()

                if is_liked:
                    tool.log(f"[{success_count+1}/{target_limit}] Status: [Liked] -> Re-Like")
                    # 取消赞
                    page.keyboard.type("z") 
                    time.sleep(random.uniform(0.5, 0.8)) # 稍微延长中间间隔，防止太快被吞
                    # 重新赞
                    page.keyboard.type("z")
                else:
                    tool.log(f"[{success_count+1}/{target_limit}] Status: [Not Liked] -> Like")
                    # 点赞
                    page.keyboard.type("z")

                success_count += 1

                # ================= 3. 翻页 =================
                wait_time = random.uniform(config.WAIT_MIN, config.WAIT_MAX)
                time.sleep(wait_time)
                
                # 翻页前也确保一下焦点，防止刚才的操作丢焦
                ensure_focus()
                page.keyboard.press(config.KEY_NEXT)
                
                # 等待视频加载
                time.sleep(1.5)

        except KeyboardInterrupt:
            tool.log(f"\n[INFO] Stopped manually. Total: {success_count}")

if __name__ == "__main__":
    run_bot()
