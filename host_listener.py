# host_listener.py (运行在真实电脑上)
from http.server import BaseHTTPRequestHandler, HTTPServer
from plyer import notification
import time

# 配置监听端口
HOST_PORT = 8888

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """收到 GET 请求时触发"""
        print(f"[{time.strftime('%H:%M:%S')}] 收到虚拟机发来的信号！")
        
        # 1. 弹窗通知
        try:
            notification.notify(
                title="【任务完成】",
                message="虚拟机发来贺电：抖音点赞 KPI 已达标！",
                app_name="抖音小助手",
                timeout=10
            )
        except Exception as e:
            print(f"弹窗失败: {e}")

        # 2. 回复虚拟机收到
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        # 屏蔽繁琐的默认日志，只看关键信息
        pass

if __name__ == "__main__":
    print(f">>> 宿主机监听服务已启动...")
    print(f">>> 正在监听端口 {HOST_PORT}，等待虚拟机呼叫...")
    print(">>> (如果弹出防火墙警告，请点击“允许访问”)")
    
    # 0.0.0.0 表示允许任何机器（包括虚拟机）访问
    server = HTTPServer(('0.0.0.0', HOST_PORT), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n监听已停止")