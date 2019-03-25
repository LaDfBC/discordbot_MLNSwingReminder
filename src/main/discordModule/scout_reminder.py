import sys
from time import sleep

from discordModule import user_util
from reddit.post_fetcher import get_all_players_to_swing, getPrawInstance
from scouting.pitch_fetcher import get_last_pitches_against_team

async def init_scouting_timer(token, client, playerDAO):
    await send_reminder_ping_with_scouting(token, client, playerDAO)
    sleep(300)

async def send_reminder_ping_with_scouting(token, client, playerDAO):
    channel_to_write = None

    server = client.get_server('448977585658134539') # This is the server id
    for channel in server.channels:
        if channel.name == 'clubhouse':
            channel_to_write = channel
    pitches = get_last_pitches_against_team('MAL', 10)
    batter_name = get_all_players_to_swing(team='MAL')[0]

    if batter_name != None:
        reddit_name = batter_name['reddit_name'][3:] # Shaves off the /u/ part of the username
        full_user_info = playerDAO.get_player_by_reddit_name(reddit_name)
        batter_id = user_util.get_user_id_by_name_and_server_id(client, full_user_info[0], server)

        if batter_id != None:
            await client.send_message(channel_to_write, "<@" + str(batter_id) + ">" +
                                         ", You are up to bat!  Last 5 swings: " +
                                         str(pitches[-5]) + " " + str(pitches[-4]) + " " + str(pitches[-3]) + " " + str(pitches[-2]) + " " + str(pitches[-1]))

if __name__ == '__main__':
    args = sys.argv
    server_id = args[2]
    config_file = args[3]
    reddit = getPrawInstance(config_file)
    print(get_all_players_to_swing(reddit=reddit, team='HMH'))