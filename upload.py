import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    
    def __init__(self, cred_path):
        self.cred_path = cred_path 
        self.creds()
    
    def creds(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_path, scope)
        self.client = gspread.authorize(creds)
        
    def open_sheet_by_name(self, sheet_name):
        self.spreadsheet = self.client.open(sheet_name)
        self.worksheet = self.spreadsheet.get_worksheet(0)
        
        return self.worksheet
        
if __name__ == "__main__":
    obj = Sheets()
    emails = ["themillibit@gmail.com", "hello@gmail.com", "testing@gmail.com"]
    names = ["the Millibit", "hello", "testing"]
    
    worksheet = obj.open_sheet_by_name("Blueetooth")
    # worksheet.append_row(10, table_range='A1')
    print(worksheet)
    for i in range(10):
        worksheet.append_rows([['1']])
    # for i in range(1, len(emails)+1):
    #     worksheet.update_cell(i, 1, names[i])
    #     worksheet.update_cell(i, 2, emails[i])

    # One
    

    # worksheet = spreadsheet.get_worksheet("Email Subscribers", len(emails),
    #                                       len(names))
    



