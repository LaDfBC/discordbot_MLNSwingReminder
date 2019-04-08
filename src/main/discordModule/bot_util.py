import sys

import discord

from datastore.playerDAO import PlayerDAO
from datastore.reminderDAO import ReminderDAO
from discordModule import user_util
from discordModule.scout_reminder import init_scouting_timer
from googleSheets.player_fetcher import get_discord_to_player_map, sync_players
from reddit.post_fetcher import get_time_left_for_swing, getPrawInstance, get_all_players_to_swing
from reminders.notification_service import set_notification
from scouting.pitch_fetcher import get_last_pitches_against_team
from scouting.scoutingBotRunner import handle_scouting_request

bot = discord.Client()
ready = False
token = None

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await init_scouting_timer(bot, player_dao)
    # init_reminder_timer()

def send_reminder_ping_with_scouting(token, server_id):
    client = discord.Client()
    client_ready = client.run(token)
    channel_to_write = None

    server = client.get_server(server_id) # This is the server id
    for channel in server.channels:
        if channel.name == 'swing-bot-testing':
            channel_to_write = channel
    pitches = get_last_pitches_against_team('MAL', 10)
    batter_name = get_all_players_to_swing()
    batter_id = user_util.get_user_id_by_name_and_server_id(client, batter_name, server_id)

    client.send_message(channel_to_write, "<@" + str(batter_id) + ">" +
                                 ", You are up to bat!  Last 5 swings: " +
                                 pitches[-5] + " " + pitches[-4] + " " + pitches[-3] + " " + pitches[-2] + " " + pitches[-1])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content
    if content.startswith('!activate'):
        for member in message.server.members:
            print(member)
        bot.send_message(message.channel, "I am alive!")
    if content.startswith('!help'):
        __show_help(message.channel)
    if content.startswith('!player-notify'):
        player = message.author
        words = content.split(' ')
        # e.g., "!player-notify 5 minutes
        response = set_notification(reminder_dao, player_dao, str(player), words[1], words[2])
        await bot.send_message(message.channel, "<@" + str(player.id) + ">" + response)
    if content.startswith('!scouting'):
        response = handle_scouting_request(content)
        await bot.send_message(message.channel, response)
    if content.startswith('!gm-notify'):
        pass
    if content.startswith('!sync'):
        split_content = content.split(' ')
        if len(split_content) != 2:
            await bot.send_message(message.channel, "<@" + str(message.author.id) + ">" + ", I need a team name for that command.  Use !sync <team>.")
        else:
            team = split_content[1]
            await bot.send_message(message.channel, "<@" + str(message.author.id) + ">" + ", starting sync, this can take a while..")
            await sync_players(team, player_dao)
            await bot.send_message(message.channel, "<@" + str(message.author.id) + ">" + ", finished syncing %s!" % team)
    if content.startswith('!clock'):
        player = player_dao.get_player_by_discord_id(message.author.id)
        time_remaining = get_time_left_for_swing(player)

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
    file_path = args[2]

    reddit = getPrawInstance(file_path)
    player_dao = PlayerDAO(file_path)
    reminder_dao = ReminderDAO(file_path)
    bot.run(token)

