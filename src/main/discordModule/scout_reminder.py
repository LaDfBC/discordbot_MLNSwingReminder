import sys
from time import sleep

from discordModule import user_util
from reddit.post_fetcher import get_all_players_to_swing, getPrawInstance
from scouting.pitch_fetcher import get_last_pitches_against_team

last_player_mentioned = None

async def init_scouting_timer(client, playerDAO):
    last_batter_swung = None

    while(True):
        #TODO: Get Server should be separate function
        batter_id, pitches, server = get_batter_and_pitches(client, playerDAO)

        if last_batter_swung != batter_id:
            last_batter_swung = batter_id
            channel_to_write = None
            for channel in server.channels:
                if channel.name == 'clubhouse':
                    channel_to_write = channel

            if batter_id != None and channel_to_write != None:
                await client.send_message(channel_to_write, "<@" + str(batter_id) + ">" +
                                          ", You are up to bat!  Last 5 swings: " +
                                          str(pitches[-5]) + " " + str(pitches[-4]) + " " + str(pitches[-3]) + " " + str(
                    pitches[-2]) + " " + str(pitches[-1]))

        sleep(300)

def get_batter_and_pitches(client, playerDAO):
    batter_id = None
    channel_to_write = None

    pitches = get_last_pitches_against_team('MAL', 10)
    batter_name = get_all_players_to_swing(team='MAL')[0]

    if batter_name != None:
        reddit_name = batter_name['reddit_name'][3:] # Shaves off the /u/ part of the username
        full_user_info = playerDAO.get_player_by_reddit_name(reddit_name)
        batter_id = user_util.get_user_id_by_name_and_server_id(client, full_user_info[0], server)
    return batter_id, pitches, server

if __name__ == '__main__':
    args = sys.argv
    server_id = args[2]
    config_file = args[3]
    reddit = getPrawInstance(config_file)
    print(get_all_players_to_swing(reddit=reddit, team='HMH'))