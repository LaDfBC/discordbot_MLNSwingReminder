import psycopg2

from configuration_storage import Configs

class PlayerDAO():
    def __init__(self, config_file_path):
        configs = Configs(config_file_path)
        self.config = configs.get_all_configs()

    def __start_query(self):
        self.conn = psycopg2.connect(dbname='mlnbot', user=self.config['user'], password=self.config['password'],
                                     port=self.config['port'], host=self.config['host'])
        self.cur = self.conn.cursor()

    def __end_query(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def initialize_all_players(self, player_list):
        query = "INSERT INTO player VALUES ('%s', '%s', '%s');"
        self.__start_query()

        for player in player_list:
            self.cur.execute(query % (player['discord'], player['reddit'], player['player']))

        self.__end_query()

    def get_player_by_discord_id(self, discord_id):
        query = "select * from player where discord_id = '" + discord_id + "';"
        return self.select(query)[0][1]

    def get_player_by_reddit_name(self, reddit_name):
        query = "select * from player where reddit_name = '" + reddit_name + "';"
        return self.select(query)[0][0]

    def select(self, query):
        self.__start_query()
        results = self.cur.execute(query)

        reminders_to_return = []
        for result in self.cur:
            reminders_to_return.append([result[0], result[1], result[2]])

        self.__end_query()
        return reminders_to_return
