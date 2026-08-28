import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# 從環境變數讀取 Slack Webhook，若讀不到則提示
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_clock_in_reminder():
    payload = {
        "text": "☀️ **上班打卡提醒**\n大家早安！已經 09:00 囉，記得確認今天是否已完成 104 打卡喔！"
    }
    send_slack_message(payload, "上班打卡提醒")

def send_clock_out_reminder():
    payload = {
        "text": "⏰ **下班打卡提醒**\n各位夥伴辛苦了！已經 17:00 囉，記得完成 104 打卡再下班喔！"
    }
    send_slack_message(payload, "下班打卡提醒")

def send_slack_message(payload, title):
    if not SLACK_WEBHOOK_URL:
        print(f"[錯誤] 未設定 SLACK_WEBHOOK_URL 環境變數，無法發送 {title}")
        return

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[成功] {title}已發送至 Slack！")
        else:
            print(f"[錯誤] Slack 回傳異常: {response.status_code}")
    except Exception as e:
        print(f"[失敗] 訊息發送失敗: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Taipei")

    # 1. 每週一至週五 09:00 提醒上班打卡
    scheduler.add_job(
        send_clock_in_reminder,
        trigger='cron',
        day_of_week='mon-fri',
        hour=08,
        minute=30
    )

    # 2. 每週一至週五 17:00 提醒下班打卡
    scheduler.add_job(
        send_clock_out_reminder,
        trigger='cron',
        day_of_week='mon-fri',
        hour=15,
        minute=50
    )

    print("🚀 打卡提醒服務已啟動...")
    print("⏰ 排程：每週一至週五 09:00 與 17:00 自動發送！")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("🛑 服務已安全停止。")
