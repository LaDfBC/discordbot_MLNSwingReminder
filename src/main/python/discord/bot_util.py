from time import sleep

import discord
import sys

from src.main.python.discord import reader

bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    reader.handle_message(message)

async def send_message_to_channel(message, text):
    await bot.wait_until_ready()
    bot.send_message(message.channel, text)

async def send_reminder_direct_message():
    await bot.wait_until_ready()
    bot.send_message(person, text)

'''
Waits until ready and then is able to return the instance for better
'''
def get_bot_instance():
    while not ready:
        sleep(5)

    return bot

if __name__ == '__main__':
    args = sys.argv
    token = args[1]

    bot.run(token)