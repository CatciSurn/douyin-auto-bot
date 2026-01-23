import time
import random
from playwright.sync_api import sync_playwright

# ================= 配置区域 =================
# 注意：你需要先运行一次命令启动一个开启调试端口的 Chrome，
# 这样脚本才能接管你已经登录的浏览器。
# 在终端运行: 
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_profile"
# (请根据你电脑Chrome的实际路径调整)
# ===========================================

def run():
    print("正在连接到已打开的浏览器...")
    
    with sync_playwright() as p:
        # 连接到你手动打开的 Chrome 浏览器
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0] # 获取当前活动的标签页
        except Exception as e:
            print("连接失败！请确保你已经用调试命令启动了 Chrome。")
            print(f"错误信息: {e}")
            return

        print(f"已连接到页面: {page.title()}")
        print("请确保你现在停留在【群聊界面】，并且聊天记录已经加载出来。")
        input("准备好后，按回车键开始分析...")

        # 获取所有的聊天气泡（这里需要根据实际网页结构调整选择器）
        # 假设视频卡片有一个特定的标识，比如包含 'video' 的 class 或特定的标签
        # 警告：抖音的类名是动态的，下面是基于通用结构的伪代码逻辑
        
        # 查找页面上所有的视频容器（这里是核心难点，需要配合开发者工具调整）
        # 假设群聊里的视频链接通常包含 'modal_id' 或者特定的视频类名
        video_elements = page.query_selector_all("div[data-e2e='chat-message-video']") 
        
        if not video_elements:
            print("未检测到视频消息，或者是选择器失效了。请检查页面元素。")
            # 备用方案：尝试找包含视频封面的元素
            video_elements = page.query_selector_all("div.video-card") 

        print(f"检测到 {len(video_elements)} 个视频消息。开始逐个处理...")

        for index, video in enumerate(video_elements):
            print(f"\n正在处理第 {index + 1} 个视频...")
            
            try:
                # 1. 点击视频，使其在弹窗或大屏中播放
                video.click()
                time.sleep(2) # 等待视频加载
                
                # 2. 定位点赞按钮 (通常在一个 Modal 弹窗里)
                # 抖音网页版点赞按钮通常有一个 data-e2e 属性，比如 'like-icon'
                # 或者通过 aria-label="点赞" 来找
                like_btn = page.wait_for_selector("[data-e2e='video-player-digg']", timeout=5000)
                
                if not like_btn:
                    print("没找到点赞按钮，跳过。")
                    continue

                # 3. 检查点赞状态
                # 通常已点赞状态的 class 会包含 'active' 或颜色属性
                class_attr = like_btn.get_attribute("class")
                is_liked = "active" in class_attr or "selected" in class_attr
                
                print(f"当前状态: {'已点赞' if is_liked else '未点赞'}")

                if is_liked:
                    # 需求：如果已赞，先取消，再点赞
                    print("执行：取消点赞 -> 重新点赞")
                    like_btn.click() # 取消
                    time.sleep(random.uniform(0.5, 1.5))
                    like_btn.click() # 点赞
                else:
                    # 需求：如果未赞，直接点赞
                    print("执行：直接点赞")
                    like_btn.click()

                # 4. 关闭当前视频弹窗，回到列表 (通常按 Esc 或者点关闭按钮)
                page.keyboard.press("Escape")
                time.sleep(1)

            except Exception as e:
                print(f"处理视频时出错: {e}")
                # 尝试按 Esc 恢复状态
                page.keyboard.press("Escape")

    print("\n所有操作已完成。")

if __name__ == "__main__":
    run()