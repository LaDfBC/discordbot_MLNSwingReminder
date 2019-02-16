from src.main.python.reddit.Post import Post
import sys
import praw

def get_all_players_to_swing(reddit):
    posts = reddit.subreddit("BaseballbytheNumbers").hot(limit = 25)
    players = []

    for post in posts:
        if post.link_flair_text == None:
            continue

        current_post = Post(post)
        # try:
        if current_post.is_game_day_thread and not current_post.has_current_player_swung():
            player = current_post.get_current_player()
            if player is not None:
                players.append(player, post_time)

    return players

''' 
Gets a Reddit instance via PRAW, which is a nice wrapper over Reddit
'''
def getPrawInstance(configs):
    client_id = configs.get_config_by_name('client_id')
    client_password = configs.get_config_by_name('client_secret')
    if client_id is None or client_password is None:
        print("Failed to get reddit client authentication information from config!")

    reddit = praw.Reddit(client_id = client_id,
                         client_secret = client_password,
                         user_agent = 'MLNStatsv0.1')
    return reddit

if __name__ == '__main__':
    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    reddit_client = getPrawInstance(client_id, client_secret)
    remind_all_players(reddit_client)
