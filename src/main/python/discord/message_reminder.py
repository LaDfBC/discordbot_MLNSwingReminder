import discord
import sys

from src.main.python.configuration_storage import Configs
from src.main.python.datastore.reminderDAO import ReminderDAO
from src.main.python.reddit import post_fetcher
from src.main.python.reddit.post_fetcher import getPrawInstance

bot = None

# TODO: Make player class.  Test member calls.  Add Reminder DAO method
# TODO: This shit don't work.
def remind_players(configs):
    praw = getPrawInstance(configs)
    players_who_need_to_swing = post_fetcher.get_all_players_to_swing(praw)

    if len(players_who_need_to_swing) > 0:
        reminderDao = ReminderDAO(configs)
        members = bot.get_all_members()
    else:
        return

    for player in players_who_need_to_swing:
        reminders = reminderDao.select_by_reddit_name(player.user)
        for reminder in reminders:
            if reminder.time < player.time:
                for member in members:
                    if member.id == reminders.discord_id:
                        bot.send_message(member, "Hey " + member.name +
                                         ", this is your reminder to swing!  You have " + player.time + " left to do so!")

    return players_who_need_to_swing


if __name__ == '__main__':
    configs = Configs(sys.argv[1])
    bot = discord.Client()
    bot.wait_until_ready()

    remind_players(configs)