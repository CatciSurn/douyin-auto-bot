import time
import random
from playwright.sync_api import sync_playwright

def run():
    print(">>> 正在连接到 Edge 浏览器...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            if not context.pages:
                print("错误：Edge 似乎没有打开任何标签页。")
                return
            page = context.pages[0] 
        except Exception as e:
            print(f"连接失败: {e}")
            return

        print(f">>> 已连接页面: {page.title()}")
        input(">>> 请确保已进入【群聊界面】并加载了历史消息，按【回车键】开始...\n")

        print("正在扫描视频消息...")
        
        # ==================== 修正 1: 直接找图片元素 ====================
        # 之前是找 div，容易被遮挡。现在直接找那个 base64 的播放按钮图片
        # 或者是封面图。我们优先找封面图，因为它面积大。
        
        # 查找所有作为视频封面的 img (根据你之前的 HTML 分析)
        # 你的 HTML: <img class="rQng0a00 lBozEagZ" src="https://...">
        # 以及播放按钮: <img ... src="data:image...">
        
        # 我们直接定位那个“播放按钮图标”，因为它一定在最上面
        video_imgs = page.query_selector_all("img[src^='data:image']")
        
        print(f">>> 扫描结束，共发现 {len(video_imgs)} 个视频播放按钮。")

        if len(video_imgs) == 0:
            print("!! 未找到视频。请确保你已滚动加载了历史消息。")
            return

        # ==================== 循环处理 ====================
        for i, video_img in enumerate(video_imgs):
            print(f"\n--- 正在处理第 {i+1} 个视频 ---")
            
            try:
                # 1. 滚动到该元素位置
                video_img.scroll_into_view_if_needed()
                time.sleep(0.5)
                
                # ==================== 修正 2: 强制点击 ====================
                print("动作：尝试点击视频...")
                try:
                    # force=True: 即使被遮挡也强制点击
                    # no_wait_after=True: 不等待页面加载，立即进行下一步（因为是弹窗）
                    video_img.click(force=True, timeout=3000)
                except Exception as click_err:
                    print(f"普通点击失败，尝试JS点击: {click_err}")
                    # 如果上面的点击还不行，用 JS 直接触发
                    page.evaluate("element => element.click()", video_img)

                # 等待视频弹窗出现 (检测弹窗层是否存在)
                time.sleep(2)
                
                # ==================== 寻找点赞按钮 ====================
                # 更新选择器：增加容错
                try:
                    # 优先找 data-e2e 属性
                    like_btn = page.wait_for_selector("[data-e2e='video-item-digg']", state="visible", timeout=3000)
                except:
                    print("跳过：未找到点赞按钮（可能点击没生效，或者不是视频）。")
                    # 尝试按 Esc 兜底
                    page.keyboard.press("Escape")
                    continue

                if like_btn:
                    # 3. 判断状态
                    class_text = like_btn.get_attribute("class")
                    # 抖音的点赞状态通常在 svg 或者父级 div 上
                    # 这里打印一下 class 方便调试
                    # print(f"DEBUG: 按钮Class为 {class_text}")
                    
                    is_liked = "active" in class_text or "selected" in class_text
                    
                    if is_liked:
                        print("状态：[已点赞] -> 执行重置")
                        like_btn.click(force=True) # 取消
                        time.sleep(random.uniform(0.5, 1.0))
                        like_btn.click(force=True) # 重赞
                    else:
                        print("状态：[未点赞] -> 执行点赞")
                        like_btn.click(force=True)
                    
                    time.sleep(0.5)

                # 4. 关闭弹窗
                page.keyboard.press("Escape")
                
                wait_t = random.uniform(1.0, 2.0)
                print(f"休息 {wait_t:.1f} 秒...")
                time.sleep(wait_t)

            except Exception as e:
                print(f"出错跳过: {e}")
                page.keyboard.press("Escape")
                continue

    print("\n>>> 全部完成！")

if __name__ == "__main__":
    run()