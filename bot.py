services:
  - type: web
    name: avito-audit-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: API_TOKEN
        value: "8758062883:AAHdUUQLR2yZehCgmrMp1IVg_79GqakzZZo"
      - key: ADMIN_ID
        value: "1256835529"
