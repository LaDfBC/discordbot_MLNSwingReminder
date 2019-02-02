import discord

# Will be set in main runner
from src.main.python.datastore import initialiser
from src.main.python.datastore.reminderDAO import ReminderDAO
from src.main.python.discord.message_parser import parse_timeframe

token = None
bot = discord.Client()
reminder_dao = ReminderDAO()

def handle_message(message):
    if message.author == bot.user:
        return

    content = message.content
    if content.startswith('!activate'):
        bot.send_message(message.channel, "I am alive!")
    if content.startswith('!help'):
        __show_help(message.channel)
    if content.startswith('!player-remind'):
        player = message.author
        words = content.split(' ')
        timeframe = parse_timeframe(words)
        if(reminder_dao.add_reminder(player.id, player.name, int(words[1]))):
            bot.send_message(message.channel, "Added a reminder for you, <@" + str(player.id) + ">.")
        else:
            bot.send_message(message.channel, "I already a reminder for you at this time")
    if content.startswith('!gm-notify'):
        pass
    if content.startswith('!show-reminders'):
        results = reminder_dao.select_all()
        all_data = 'I found the following results for you: \n'
        for result in results:
            all_data += result[0] + ": " + str(result[1]) + '\n'
        bot.send_message(message.channel, all_data)
    if content.startswith('!init'):
        initialiser.setup_database()

def __show_help(channel):
    bot.send_message(channel,
                   "!player-notify: <time>\n" +
                   "!gm-notify: <time>\n")

