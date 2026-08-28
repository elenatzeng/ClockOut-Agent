import os
import sys
import requests

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_message(text, title):
    if not SLACK_WEBHOOK_URL:
        print(f"[錯誤] 未設定 SLACK_WEBHOOK_URL 環境變數")
        return

    payload = {"text": text}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[成功] {title}已發送至 Slack！")
        else:
            print(f"[錯誤] Slack 回傳異常: {response.status_code}")
    except Exception as e:
        print(f"[失敗] 發送失敗: {e}")

if __name__ == "__main__":
    # 根據傳入的參數決定發送哪種提醒
    type_arg = sys.argv[1] if len(sys.argv) > 1 else "out"
    
    if type_arg == "in":
        msg = "☀️ **上班打卡提醒**\n大家早安！記得確認今天是否已完成 104 打卡喔！"
        send_slack_message(msg, "上班打卡提醒")
    else:
        msg = "⏰ **下班打卡提醒**\n各位夥伴辛苦了！已經到下班時間囉，記得去 104 打卡！"
        send_slack_message(msg, "下班打卡提醒")
