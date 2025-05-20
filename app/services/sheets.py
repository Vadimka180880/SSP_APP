import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def write_to_google_sheet(data: dict):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # ✅ читаємо з JSON-файлу, а не з os.environ
    with open("credentials/alpha-platforms-creds.json") as f:
        creds_info = json.load(f)

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
