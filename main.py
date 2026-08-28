import os
import requests
from datetime import datetime
import pytz

# 從 GitHub Secrets 讀取 Slack Webhook 網址
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_message(text, title):
    if not SLACK_WEBHOOK_URL:
        print("[錯誤] 未設定 SLACK_WEBHOOK_URL 變數！")
        return
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=5)
        if response.status_code == 200:
            print(f"[成功] {title} 已發送至 Slack！")
        else:
            print(f"[失敗] 發送失敗，HTTP 狀態碼：{response.status_code}")
    except Exception as e:
        print(f"[異常] 發送過程發生錯誤: {e}")

if __name__ == "__main__":
    # 強制使用台灣時區 (Asia/Taipei) 判斷時間
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now_hour = datetime.now(taiwan_tz).hour

    # 判斷時間：中午 12 點前發送上班提醒，12 點後發送下班提醒
    if now_hour < 12:
        msg = "☀️ **上班打卡提醒**\n大家早安！記得確認今天是否已完成 104 打卡喔！"
        send_slack_message(msg, "上班打卡提醒")
    else:
        msg = "⏰ **下班打卡提醒**\n各位夥伴辛苦了！已經到下班時間囉，記得去 104 打卡！"
        send_slack_message(msg, "下班打卡提醒")
