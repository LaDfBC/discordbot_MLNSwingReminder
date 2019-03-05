from time import sleep

from gspread.exceptions import APIError

from googleSheets.sheetsAuthenticator import get_gspread_service

'''Fetches from the database, the player name given the discord name provided'''
def get_player_name_by_discord_name(discord_name, player_dao, mlr=False):
    return player_dao.get_player_by_discord_id(discord_name)


async def sync_players(team, player_dao):
    players = get_discord_to_player_map(team)
    player_dao.initialize_all_players(players)

'''Fetches and records in the database every single player in MLN (or MLR, eventually)'''
def get_discord_to_player_map(team, mlr = False):
    player_list = []
    if mlr:
        sheet_id = ''
    else: # MLN
        sheet_id = '1Low-dGHEMwt4PyaJPz45Rt-WXuFqP2teXVxbyQ71zgk'

    gspread = get_gspread_service()
    overall_spreadsheet = gspread.open_by_key(sheet_id)
    current_row = 4
    current_tries = 0
    while current_tries < 5:
        try:
            worksheet = overall_spreadsheet.worksheet(team)
            while current_row < 27:
                player_name = worksheet.cell(current_row, 1).value
                reddit_name = worksheet.cell(current_row, 3).value
                discord_name = worksheet.cell(current_row, 4).value
                if discord_name != '' and discord_name != 'Discord':
                    player_list.append({'player': player_name, 'reddit': reddit_name, 'discord' : discord_name})
                current_row += 1
            break
        except APIError:
            current_tries += 1
            print("Timed out pulling team info.  Waiting 100 and trying again.")
            sleep(100)

    return player_list

if __name__ == '__main__':
    print(get_player_name_by_discord_name('LaDfBC#1246'))