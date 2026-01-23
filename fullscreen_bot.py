import time
import random
from playwright.sync_api import sync_playwright

# ================= 配置区域 =================
# 切换方向： "ArrowUp" (看上一条/旧消息) 
SWITCH_KEY = "ArrowUp" 
# ===========================================

def run():
    print(">>> 正在连接到 Edge 浏览器...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            if not context.pages:
                print("错误：请先打开 Edge 标签页。")
                return
            page = context.pages[0]
        except Exception as e:
            print(f"连接失败: {e}")
            return

        print(f">>> 已连接页面: {page.title()}")
        print(">>> ⚠️ 操作指引：")
        print("1. 请手动在群聊里【点开最后一条（最新）视频】，进入全屏播放界面。")
        print("2. 确保鼠标焦点在网页上。")
        input(">>> 准备好后，按【回车键】开始自动化...\n")

        print(">>> 自动化已启动！按 Ctrl+C 停止。")

        try:
            while True:
                # ================= 1. 寻找点赞按钮 =================
                # 策略：寻找包含特定路径(path)数据的 svg 元素
                # 或者直接找包含 "点赞" 文本的容器（aria-label）
                # 为了最稳健，我们通过 data-e2e 属性找父级容器
                
                try:
                    # 等待点赞按钮容器出现
                    # 抖音全屏页点赞按钮通常有 data-e2e="video-item-digg" 或 "xg-player-digg"
                    like_btn = page.wait_for_selector("[data-e2e='video-item-digg']", timeout=4000)
                except:
                    print(f"⚠️ 未找到点赞按钮（可能加载慢），尝试切换下一条...")
                    page.keyboard.press(SWITCH_KEY)
                    time.sleep(2)
                    continue

                if like_btn:
                    # ================= 2. 判断状态（核心修复） =================
                    # 我们直接检查那个 SVG 里的 path 颜色
                    # 你的 SVG 代码显示：已赞时 fill="rgb(254,44,85)"
                    
                    # 获取按钮内部 SVG 的 HTML 代码
                    inner_html = like_btn.inner_html()
                    
                    # 判断逻辑：如果 HTML 里包含这个红色值，说明已赞
                    is_liked = "rgb(254, 44, 85)" in inner_html or "rgba(254, 44, 85" in inner_html
                    
                    if is_liked:
                        print(f"[{time.strftime('%H:%M:%S')}] 状态：❤️ 已赞 (检测到红色) -> 🔄 重置")
                        # 取消点赞
                        like_btn.click(force=True)
                        time.sleep(random.uniform(0.5, 0.8))
                        # 重新点赞
                        like_btn.click(force=True)
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] 状态：🤍 未赞 -> ❤️ 点赞")
                        like_btn.click(force=True)
                
                # ================= 3. 切换视频 =================
                watch_time = random.uniform(2.0, 4.0)
                # print(f"    --> 观看 {watch_time:.1f} 秒...")
                time.sleep(watch_time)

                print(f"    --> 切换上一条 ({SWITCH_KEY})")
                page.keyboard.press(SWITCH_KEY)
                
                # 等待加载
                time.sleep(random.uniform(1.5, 2.0))

        except KeyboardInterrupt:
            print("\n>>> 程序已手动停止。")

if __name__ == "__main__":
    run()