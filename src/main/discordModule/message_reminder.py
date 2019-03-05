import discordModule
import sys

from configuration_storage import Configs
from datastore.playerDAO import PlayerDAO
from datastore.reminderDAO import ReminderDAO
from reddit import post_fetcher
from reddit.post_fetcher import getPrawInstance

bot = None

# TODO: Make player class.  Test member calls.  Add Reminder DAO method
# TODO: This shit don't work.
def remind_players(config_path):
    praw = getPrawInstance(config_path)
    players_who_need_to_swing = post_fetcher.get_all_players_to_swing(praw)

    if len(players_who_need_to_swing) > 0:
        reminderDao = ReminderDAO(config_path)
        playerDao = PlayerDAO(config_path)
    else:
        return

    reminder_list = []
    for player in players_who_need_to_swing:
        reminders = reminderDao.select_by_reddit_name(player['reddit_name'])
        discord_id = playerDao.get_player_by_reddit_name(player['reddit_name'])[0]
        for reminder in reminders:
            if reminder.time < player[1]:
                reminder_list.append({'discord': discord_id, 'time': player['time']})

    return players_who_need_to_swing


if __name__ == '__main__':
    config_path = sys.argv[1]

    remind_players(config_path)