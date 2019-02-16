import sys

import discord

from datastore.reminderDAO import ReminderDAO
from reminders.notification_service import set_notification
from scouting.scoutingBotRunner import handle_scouting_request

bot = discord.Client()
ready = False
token = None
reminder_dao = ReminderDAO("/home/george/repos/discordSwingReminder/dbconfig.cfg")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content
    if content.startswith('!activate'):
        bot.send_message(message.channel, "I am alive!")
    if content.startswith('!help'):
        __show_help(message.channel)
    if content.startswith('!player-notify'):
        player = message.author
        words = content.split(' ')
        response = set_notification(reminder_dao, player.id, str(player), player.name, words[1], words[2])
        await bot.send_message(message.channel, "<@" + str(player.id) + ">" + response)
    if content.startswith('!scouting'):
        response = handle_scouting_request(content)
        await bot.send_message(message.channel, response)
    if content.startswith('!gm-notify'):
        pass
    if content.startswith('!show-reminders'):
        results = reminder_dao.select_all()
        all_data = 'I found the following results for you: \n'
        for result in results:
            all_data += result[0] + ": " + str(result[1]) + '\n'
        bot.send_message(message.channel, all_data)

def __show_help(channel):
    bot.send_message(channel,
                   "!player-notify: <time>\n" +
                   "!gm-notify: <time>\n")

async def send_message_to_channel(message, text):
    await bot.wait_until_ready()
    bot.send_message(message.channel, text)

if __name__ == '__main__':
    args = sys.argv
    token = args[1]

    bot.run(token)