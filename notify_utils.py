# notify_utils.py
import requests
import json
import debug_utils as tool

# ================= 配置区域 =================
# 1. WxPusher 配置 (替代 PushPlus)
# 请填入刚才在网页上复制的内容
WX_APP_TOKEN = "你的WX_APP_TOKEN"   # 例如: AT_xxx...
WX_UID = "你的WX_UID"              # 例如: UID_xxx...

# 2. 宿主机通讯配置 (用于给真实电脑弹窗)
# 虚拟机的网关通常是 10.0.2.2 (VirtualBox NAT模式)
# 如果不通，请换成真实电脑的局域网IP
HOST_IP = "10.0.2.2"
HOST_PORT = 8888
# ===========================================

def send_to_host_machine():
    """给宿主机(真实电脑)发送信号，让它弹窗"""
    url = f"http://{HOST_IP}:{HOST_PORT}"
    try:
        # tool.log(f"正在呼叫真实电脑 ({url})...")
        requests.get(url, timeout=2)
        tool.log("✅ 电脑弹窗通知已发送")
    except Exception as e:
        tool.log(f"⚠️ 无法连接到真实电脑: {e}")
        # 失败了也不影响后续发送手机通知

def send_wxpusher(content):
    """发送微信通知 (基于 WxPusher)"""
    if "你的" in WX_APP_TOKEN or "你的" in WX_UID:
        tool.log("⚠️ 未配置 WxPusher Token/UID，跳过手机通知")
        return

    url = "https://wxpusher.zjiecode.com/api/send/message"
    
    if "点赞失败警告" in content:
        payload = {
            "appToken": WX_APP_TOKEN,
            "content": content,
            "summary": "点赞失败警告", # 消息卡片上的标题
            "contentType": 1, # 1表示文本，2表示HTML
            "uids": [WX_UID]  # 发给谁，可以是一个列表
        }
    else:
        payload = {
            "appToken": WX_APP_TOKEN,
            "content": content,
            "summary": "抖音任务完成汇报", # 消息卡片上的标题
            "contentType": 1, # 1表示文本，2表示HTML
            "uids": [WX_UID]  # 发给谁，可以是一个列表
        }
    
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        if res_json.get("code") == 1000: # 1000 代表成功
            tool.log("✅ 手机微信通知已发送 (WxPusher)")
        else:
            tool.log(f"⚠️ WxPusher 发送失败: {res_json.get('msg')}")
    except Exception as e:
        tool.log(f"⚠️ 网络请求出错: {e}")

def send_all(finished_count):
    """同时发送电脑和手机通知"""
    msg = f"老板，任务搞定！助手已成功完成 {finished_count} 个视频的点赞KPI，现已自动停止休息。"
    
    # 1. 通知真实电脑 (局域网)
    send_to_host_machine()
    
    # 2. 通知手机微信 (WxPusher)
    send_wxpusher(msg)