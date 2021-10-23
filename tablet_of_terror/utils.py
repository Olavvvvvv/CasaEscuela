from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '10xs12jq5lmIO4VzvwUz5K7rAfX-cNDZ9Nj5LQfGS7Zg'
READING_RANGE = 'Blad1!A1:D60'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=READING_RANGE).execute()

#get data, return empty list if empty
values = result.get('values', [])


for i in values[0:5]:
    print(i)

