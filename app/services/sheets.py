import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def write_to_google_sheet(data: dict):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # 🔽 ЗАМІСТЬ читання з файлу
    # with open("credentials/alpha-platforms-creds.json") as f:
    #     creds_info = json.load(f)

    # ✅ Читання з середовища
    creds_info = json.loads(os.environ.get("GOOGLE_CREDS_JSON"))

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)

    sheet = client.open("ssp-submissions").sheet1
    row = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data.get('name'),
        data.get('email'),
        data.get('department'),
        data.get('comment'),
        data.get('photo_url')
    ]
    sheet.append_row(row)
