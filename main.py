name: Slack Reminder

on:
  schedule:
    # 台灣時間 08:30 (UTC 00:30) 與 17:00 (UTC 09:00)
    - cron: '30 0 * * 1-5'
    - cron: '0 9 * * 1-5'
  workflow_dispatch:

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
