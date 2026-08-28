import os
import requests
from datetime import datetime
import pytz

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_message(text, title):
    if not SLACK_WEBHOOK_URL:
        print("[錯誤] 未設定 SLACK_WEBHOOK_URL")
        return
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=5)
        if response.status_code == 200:
            print(f"[成功] {title}已發送至 Slack！")
    except Exception as e:
        print(f"[失敗] 發送失敗: {e}")

if __name__ == "__main__":
    # 取得台灣當前小時 (0-23)
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now_hour = datetime.now(taiwan_tz).hour

    # 12 點前發上班提醒，12 點後發下班提醒
    if now_hour < 12:
        msg = "☀️ **上班打卡提醒**\n大家早安！記得確認今天是否已完成 104 打卡喔！"
        send_slack_message(msg, "上班打卡提醒")
    else:
        msg = "⏰ **下班打卡提醒**\n各位夥伴辛苦了！已經到下班時間囉，記得去 104 打卡！"
        send_slack_message(msg, "下班打卡提醒")
