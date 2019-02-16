from time import sleep

from gspread.exceptions import APIError

from src.main.python.googleSheets.sheetsAuthenticator import get_gspread_service

def get_player_name_by_discord_name(discord_name, mlr=False):
    if mlr:
        sheet_id = ''
    else: # MLN
        sheet_id = '1Low-dGHEMwt4PyaJPz45Rt-WXuFqP2teXVxbyQ71zgk'

    gspread = get_gspread_service()
    overall_spreadsheet = gspread.open_by_key(sheet_id)

    current_tries = 0
    while current_tries < 5:
        try:
            for worksheet in overall_spreadsheet.worksheets():
                if worksheet.title not in ('Schedule', 'Standings', 'Power Rankings', 'Free Agents', 'Awards History'):
                    for row in range (4, 26):
                        name_on_sheet = worksheet.cell(row, 4).value
                        if discord_name == name_on_sheet:
                            return worksheet.cell(row, 3).value
        except APIError:
            sleep(100)
            current_tries += 1

if __name__ == '__main__':
    print(get_player_name_by_discord_name('LaDfBC#1246'))