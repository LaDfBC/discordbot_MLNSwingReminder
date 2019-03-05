from googleSheets.sheetsAuthenticator import get_spreadsheet_service
from googleSheets.row_organizer import PITCHER, PITCH_VALUE, get_row_as_dict, BATTER, SWING_VALUE, GAME_NUMBER
from scouting.distributionAnalyzer import groupValuesByRange, analyzeStreak

'''
Uses a filename on the local machine and a pitcher name to analyze to fetch all of pitches thrown by the named person
and then return them all in the order they were thrown, as well as the "Deltas" between the pitches - that is, the difference
between the values of each pitch thrown by that person.

These lists are commonly fed into the distributation analyzer stuff to produce reports about the pitches
'''
def fetchPitchesByPitcherAndLocalFile(file_name, player_name, batter = False, mlr = False):
    values = []
    deltas = []
    first_pitches = []

    player_name = player_name.lower()
    previous_pitch = None

    file = open(file_name, 'r')

    current_game = None
    for original_row in file:
        row = get_row_as_dict(original_row, mlr, is_list=False)


        if not batter:
            # If not, just do nothing
            if PITCHER in row.keys() and row[PITCHER].lower() == player_name:
                if row[PITCH_VALUE] != '':
                    if current_game is None or current_game != row[GAME_NUMBER]:
                        current_game = row[GAME_NUMBER]
                        first_pitches.append(int(row[PITCH_VALUE]))

                    values.append(int(row[PITCH_VALUE]))

                    if previous_pitch is not None:
                        deltas.append(int(row[PITCH_VALUE]) - int(previous_pitch))
                    previous_pitch = row[PITCH_VALUE]

        else:
            if BATTER in row.keys() and row[BATTER].lower() == player_name:
                if row[SWING_VALUE] != '':
                    if current_game is None or current_game != row[GAME_NUMBER]:
                        current_game = row[GAME_NUMBER]
                        first_pitches.append(int(row[SWING_VALUE]))

                    values.append(int(row[SWING_VALUE]))

                    if previous_pitch is not None:
                        deltas.append(int(row[SWING_VALUE]) - int(previous_pitch))
                    previous_pitch = row[SWING_VALUE]

    file.close()
    # return pitches
    return values, deltas, first_pitches

'''
Uses a Google Spreadsheet ID and a pitcher name to analyze to fetch all of pitches thrown by the named person
and then return them all in the order they were thrown, as well as the "Deltas" between the pitches - that is, the difference
between the values of each pitch thrown by that person.

These lists are commonly fed into the distributation analyzer stuff to produce reports about the pitches
'''
def fetchPitchesByPitcherAndGoogleSheet(spreadsheet_id, player_name, batter = False, mlr=False):
    spreadsheets = get_spreadsheet_service()

    data = []
    deltas = []
    first_pitches = []
    player_name = player_name.lower()
    previous_pitch = None

    if mlr:
        result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range="All PA's").execute()
    else:
        result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range="All PAs").execute()
    values = result.get('values')
    row_number = 1

    current_game = None
    for row in values:
        if len(row) >= 19 and row_number >= 2:
            converted_row = get_row_as_dict(row, mlr, is_list=True)
            if not batter:
                if converted_row[PITCHER].lower() == player_name:
                    if converted_row[PITCH_VALUE] != '':
                        # if current_game is None or current_game != converted_row[GAME_NUMBER]:
                        #     current_game = converted_row[GAME_NUMBER]
                        #     first_pitches.append(int(converted_row[PITCH_VALUE]))
                        data.append(int(converted_row[PITCH_VALUE]))

                        if previous_pitch is not None:
                            deltas.append(int(converted_row[PITCH_VALUE]) - int(previous_pitch))
                        previous_pitch = converted_row[PITCH_VALUE]
            else:
                if converted_row[BATTER].lower() == player_name:
                    if converted_row[SWING_VALUE] != '':
                        # if current_game is None or current_game != converted_row[GAME_NUMBER]:
                        #     current_game = converted_row[GAME_NUMBER]
                        #     first_pitches.append(int(converted_row[SWING_VALUE]))
                        data.append(int(converted_row[SWING_VALUE]))

                        if previous_pitch is not None:
                            deltas.append(int(converted_row[SWING_VALUE]) - int(previous_pitch))
                        previous_pitch = converted_row[SWING_VALUE]
        else:
            row_number += 1
    return data, deltas, first_pitches

def get_pitches_and_deltas_for(pitcher_name, is_batter=False):
    pitches, deltas, first_pitches = fetchPitchesByPitcherAndLocalFile("/home/george/Downloads/mlnmaster1.csv", pitcher_name,
                                                        batter = is_batter)
    pitches_s2, deltas_s2, first_pitches_s2 = fetchPitchesByPitcherAndGoogleSheet('1vR8T-nZwJFYj8yKDwt0999FHzfZEEfFArZ2m1OsxPx8',
                                                                pitcher_name, batter = is_batter)

    pitches = pitches + pitches_s2
    deltas = deltas + deltas_s2
    first_pitches = first_pitches + first_pitches_s2

    # pitches = pitches_s2
    # deltas = deltas_s2
    # first_pitches = first_pitches_s2

    return pitches, deltas, first_pitches

def get_scouting_data_as_list(data, range_size, deltas=False):
    if deltas:
        numbers = [-999, 1001]
    else:
        numbers = [1, 1001]
    result = groupValuesByRange(data, range_size = range_size, numbers = numbers)

    return result

def run_report_on(pitcher_name, show_deltas=False, split=100):
    pitches, deltas, first_pitches = get_pitches_and_deltas_for(pitcher_name)

    if show_deltas:
        return get_scouting_data_as_list(deltas, split)
    else:
        return get_scouting_data_as_list(pitches, split)

if __name__ == '__main__':
    # MLN
    pitches, deltas, first_pitches = get_pitches_and_deltas_for("Miss Bats")

    #MLR
    # pitches,deltas, fp = fetchPitchesByPitcherAndGoogleSheet("1cLXbbffR0Ra1yHfFDI6fihkaXJA1rOrnrrocAXNzHKw", 'Y.E. Wally', mlr=True, batter = False)
    # pitches2,deltas2, fp = fetchPitchesByPitcherAndGoogleSheet("1JxXUlVbF_c72OA_f9wdykNNkJ0k4Z49vsUl8J-qNzJA", 'Y.E. Wally', mlr=True, batter = False)
    # pitches = pitches + pitches2
    # deltas = deltas + deltas2

    result = get_scouting_data_as_list(pitches, 50, deltas=False)

    result = analyzeStreak(deltas, range_size=100, numbers=[-999,1001])
    print(result)