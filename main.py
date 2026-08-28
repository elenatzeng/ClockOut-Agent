name: Slack Reminder

on:
  schedule:
    # 台灣時間 16:30 測試（對應 UTC 時間 08:30）
    - cron: '30 8 * * 1-5'
  workflow_dispatch: # 支援在 GitHub 上手動按按鈕觸發

jobs:
  send-reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run script
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python main.py
