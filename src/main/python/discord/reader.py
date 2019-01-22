import sys
from time import sleep

import discord
from discord.ext import commands

# Will be set in main runner
from src.main.python.datastore import initialiser

token = None
bot = discord.Client()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content
    if content.startswith('!activate'):
        await bot.send_message(message.channel, "I am alive!")
    if content.startswith('!help'):
        await __show_help(message.channel)
    if content.startswith('!player-notify'):
        pass
    if content.startswith('!gm-notify'):
        pass
    if content.startswith('!init'):
        initialiser.setup_database()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def __show_help(channel):
    bot.send_message(channel,
                   "!player-notify: <time>\n" +
                   "!gm-notify: <time>\n")

    # server = bot.get_server(448977585658134539)
bot.run('NTM2NTgxOTIwMzU2NTY0OTky.DyYzvg.BsvZgT2YpPJUNW1Nfz2r5pvKK00')


# if __name__ == '__main__':
#     args = sys.argv
#     token = args[1]
#     bot.login(token)
#     bot.get_server(448977585658134539)
#     bot.run(token)
#     channels.append(discord.Object(id = 448977585658134539))