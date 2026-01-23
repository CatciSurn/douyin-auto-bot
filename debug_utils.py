import time

# 只需要导入 DEBUG_MODE，不再需要 LIKE_BUTTON_SELECTORS
from config import DEBUG_MODE

def log(message):
    """带时间戳的日志输出"""
    # 强制刷新缓冲区，确保你能在终端实时看到日志
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)

def save_page_source(page, prefix="debug_fail"):
    """
    保存网页快照（仅在调试模式下）
    """
    if not DEBUG_MODE:
        return
    
    filename = f"{prefix}_{int(time.time())}.html"
    try:
        content = page.content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"⚠️ 调试快照已保存: {filename}")
    except Exception as e:
        log(f"保存失败: {e}")

# 注意：之前的 find_like_button_robust 和 check_is_liked 函数
# 在最新的 Z 键方案中已经不再使用了，所以这里可以直接删掉，
# 或者保留为空函数以防万一。为了保持干净，我把它们删了。