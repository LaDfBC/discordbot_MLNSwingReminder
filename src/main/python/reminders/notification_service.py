from src.main.python.googleSheets.player_fetcher import get_player_name_by_discord_name


def validate_time(time_number, time_units):
    try:
        time_number = int(time_number)
    except:
        return False, ", that's not a number.  Please enter an actual value."

    if time_units == 'minutes' or time_units == 'minute':
        if time_number < 1 or time_number > 720:
            return False, ", your range doesn't make sense. Use a minute count between 1 and 720."
        else:
            return True, ""
    elif time_units == 'hours' or time_units == 'hour':
        if time_number < 1 or time_number > 13:
            return False, ", your range doesn't make sense.  Use an hour count between 1 and 12."
        else:
            return True, ""
    else:
        return False, ", I don't recognize the units you're using.  Minutes and Hours currently accepted."

def set_notification(reminderDAO, discord_id, discord_username, player, time_number, time_units):
    valid, error_string = validate_time(time_number, time_units)
    if not valid:
        return error_string
    else:
        milli_time = get_millisecond_time(time_number, time_units)

        # Fetches Reddit name and adds it if necessary
        reddit_name = reminderDAO.get_player_by_discord_id()
        if reddit_name is None:
            reddit_name = get_player_name_by_discord_name(discord_username)
            reminderDAO.insert_player(discord_id, reddit_name, player)

        results = reminderDAO.select_by_id_and_time(discord_id, milli_time)

        # If this loop executes, this reminder already exists.  Return without updating
        for result in results:
            return ", you already have a reminder for that time!"

        reminderDAO.insert_reminder(discord_id, reddit_name, time_number)
        return ", successfully inserted a reminder for you!"

'''
Converts time number and units to milliseconds.  Assumes things are correct since they've been checked above.
'''
def get_millisecond_time(time_number, time_units):
    if time_units == 'minute' or time_units == 'minutes':
        return time_number * 60 * 1000 # Seconds * Milliseconds
    elif time_units == 'hour' or time_units == 'hours':
        return time_number * 360 * 1000 # Minutes * Seconds * Milliseconds
    else:
        raise ValueError('Unrecognized units: ' + time_units)