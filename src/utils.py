# filepath: /c:/Users/Abnet/Desktop/telethon_bot/telethon_bot/src/utils.py
import pandas as pd

def generate_report(recipients):
    data = [{'Name': recipient.name, 'Username': recipient.username} for recipient in recipients]
    df = pd.DataFrame(data)
    df.to_excel('broadcast_report.xlsx', index=False)