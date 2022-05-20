import gspread
from oauth2client.service_account import ServiceAccountCredentials

emails = ["themillibit@gmail.com", "hello@gmail.com", "testing@gmail.com"]
names = ["the Millibit", "hello", "testing"]
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)
client = gspread.authorize(creds)


# One
spreadsheet = client.open("Bluetooth")

# worksheet = spreadsheet.get_worksheet("Email Subscribers", len(emails),
#                                       len(names))
worksheet = spreadsheet.get_worksheet(0)


for i in range(1, len(emails)+1):
    worksheet.update_cell(i, 1, names[i])
    worksheet.update_cell(i, 2, emails[i])

# #
