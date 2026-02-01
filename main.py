# main.py
import time
import random
import pyautogui
from playwright.sync_api import sync_playwright
import config
import debug_utils as tool
import notify_utils as notify

# ================= 配置区域 =================
HEART_X = 1106
HEART_Y = 387

def is_red(r, g, b):
    # 红心判定阈值
    return r > 200 and g < 150 and b < 150
# ===========================================

def run_bot():
    tool.log("[INFO] Connecting to Edge Browser...")
    tool.log("[INFO] Please make sure that the page you want to like is on the first of all the pages!")
    
    with sync_playwright() as p:
        try:
            # 连接浏览器
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            if not context.pages:
                tool.log("[ERROR] No pages found. Please open a tab.")
                return
            page = context.pages[0]
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

        def ensure_focus():
            try:
                page.focus("body") 
            except Exception:
                pass

        try:
            while True:
                if success_count >= target_limit:
                    tool.log(f"\n[SUCCESS] KPI Reached! ({success_count}/{target_limit})")
                    notify.send_all(success_count)
                    break

                # 确保焦点
                ensure_focus()

                # ================= 1. 初始状态检测 =================
                initial_liked = False
                try:
                    r, g, b = pyautogui.pixel(HEART_X, HEART_Y)
                    if is_red(r, g, b):
                        initial_liked = True
                except Exception:
                    pass

                # ================= 2. 执行点赞逻辑 =================
                action_desc = ""
                
                if initial_liked:
                    # 如果本来就是红的，为了活跃度，我们需要重赞 (取消 -> 点赞)
                    action_desc = "Re-Like"
                    page.keyboard.type("z") # 取消赞
                    time.sleep(random.uniform(0.5, 0.8))
                    page.keyboard.type("z") # 重新赞
                else:
                    # 如果是白的，直接点赞
                    action_desc = "Like"
                    page.keyboard.type("z")

                # ================= 3. 循环校验 (最多5次) =================
                check_attempts = 0
                max_checks = 5
                final_status_ok = False

                while check_attempts < max_checks:
                    time.sleep(0.8) # 等待UI动画完成
                    
                    try:
                        # 检查当前颜色
                        cr, cg, cb = pyautogui.pixel(HEART_X, HEART_Y)
                        if is_red(cr, cg, cb):
                            final_status_ok = True
                            break # 只要变红了，就跳出校验循环
                        else:
                            # 还是白的，尝试补刀
                            tool.log(f"[Retry {check_attempts+1}/{max_checks}] Heart is white, retrying click...")
                            ensure_focus()
                            page.keyboard.type("z")
                    except Exception:
                        pass
                    
                    check_attempts += 1

                # ================= 4. 结果处理与计数 =================
                if final_status_ok:
                    success_count += 1
                    tool.log(f"[{success_count}/{target_limit}] Status: [{action_desc}] Success (Checks: {check_attempts})")
                else:
                    # 超过5次还是失败
                    current_url = page.url
                    error_msg = f"点赞失败警告！视频URL: {current_url} 在尝试5次后红心仍未变红，请检查账号是否受限。"
                    tool.log(f"[ERROR] {error_msg}")
                    
                    # 发送专门的报警通知 (复用 notify_utils 中的发送函数)
                    # 这里假设 notify_utils 有单独发给手机的方法，或者直接用 send_wxpusher
                    notify.send_wxpusher(error_msg) 
                    
                    # 失败不增加 success_count

                # ================= 5. 翻页 =================
                wait_time = random.uniform(config.WAIT_MIN, config.WAIT_MAX)
                time.sleep(wait_time)
                
                ensure_focus()
                page.keyboard.press(config.KEY_NEXT)
                time.sleep(1.5)

        except KeyboardInterrupt:
            tool.log(f"\n[INFO] Stopped manually. Total: {success_count}")

if __name__ == "__main__":
    run_bot()
