import psycopg2

from src.main.python.configuration_storage import Configs


class ReminderDAO():
    def __init__(self, config_file_path):
        configs = Configs(config_file_path)
        config = configs.get_all_configs()
        self.conn = psycopg2.connect(dbname='mlnbot',user=config['user'],password=config['password'],port=config['port'],host=config['host'])
        self.cur = self.conn.cursor()

    def __query(self, query):
        self.cur.execute(query)

    def select_by_id_and_time(self, discord_id, time_number):
        query = "select * from reminder"
        query += " where discord_id = '" + discord_id + "'"
        query += ' and reminder_time = ' + str(time_number)
        return self.select(query)

    def select_by_player(self, player):
        query = "select * from reminder where player = " + player
        return self.select(query)

    def select_by_reddit_name(self, reddit_name):
        query = "select * from reminder where reddit_name = " + reddit_name
        return self.select(query)

    def select_all(self):
        query = "select * from reminder"
        return self.select(query)

    def select(self, query):
        results = self.__query(query)

        reminders_to_return = []
        for result in self.cur:
            reminders_to_return.append([result[0], result[1]])

        return reminders_to_return

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    reminderDao = ReminderDAO()
    reminderDao.select()