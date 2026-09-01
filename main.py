import os
import sys
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ 內建時區庫


def send_slack_notification(webhook_url: str, message: str):
    """發送訊息至 Slack Webhook"""
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("Slack 訊息發送成功！")
    except Exception as e:
        print(f"Slack 訊息發送失敗: {e}")
        sys.exit(1)


def main():
    # 取得環境變數中的 SLACK_WEBHOOK_URL
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("錯誤: 未設定 SLACK_WEBHOOK_URL 環境變數")
        sys.exit(1)

    # 1. 強制切換至台灣時區 (Asia/Taipei)
    tw_tz = ZoneInfo("Asia/Taipei")
    now = datetime.now(tw_tz)
    current_hour = now.hour

    print(f"目前台灣時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 2. 精準時間範圍判定（避免 GitHub Actions 延遲時發錯訊息）

    # 上班提醒：僅限台灣時間 08:00 ~ 09:59 執行
    if 8 <= current_hour < 10:
        message = "☀️ **上班打卡提醒**\n大家早安！記得確認今天是否已完成 104 打卡喔！"
        print("觸發: 上班打卡提醒")
        send_slack_notification(webhook_url, message)

    # 下班提醒：僅限台灣時間 17:00 ~ 18:59 執行
    elif 17 <= current_hour < 19:
        message = "⏰ **下班打卡提醒**\n各位夥伴辛苦了！已經到下班時間囉，記得去 104 打卡！"
        print("觸發: 下班打卡提醒")
        send_slack_notification(webhook_url, message)

    # 非指定時間（包含半夜、下午、或 GitHub 延遲過久的狀況）
    else:
        print(
            f"目前台灣時間為 {now.strftime('%H:%M')}，不在設定的提醒時間區間內（08:00-10:00 / 17:00-19:00），跳過發送。"
        )


if __name__ == "__main__":
    main()
