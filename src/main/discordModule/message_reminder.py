import discordModule
import sys

from configuration_storage import Configs
from datastore.reminderDAO import ReminderDAO
from reddit import post_fetcher
from reddit.post_fetcher import getPrawInstance

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
        reminders = reminderDao.get_reminders_by_reddit_name(player[0])
        for reminder in reminders:
            if reminder.time < player[1]:
                for member in members:
                    if member.id == reminders.discord_id:
                        bot.send_message(member, "Hey " + member.name +
                                         ", this is your reminder to swing!  You have " + player.time + " left to do so!")

    return players_who_need_to_swing


if __name__ == '__main__':
    configs = Configs(sys.argv[1])
    bot = discordModule.Client()
    bot.wait_until_ready()

    remind_players(configs)