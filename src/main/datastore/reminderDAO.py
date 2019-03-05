import psycopg2

from configuration_storage import Configs

class ReminderDAO():
    def __init__(self, config_file_path):
        configs = Configs(config_file_path)
        self.config = configs.get_all_configs()

    def __query(self, query):
        self.cur.execute(query)

    def insert_reminder(self, discord_id, reddit_name, time_number):
        self.__start_query()
        query = "INSERT INTO reminder VALUES ('%s', '%s', '%s');"
        self.cur.execute(query % (discord_id, reddit_name, time_number))
        self.__end_query()

    def select_by_id_and_time(self, discord_id, time_number):
        query = "select * from reminder"
        query += " where discord_id = '" + discord_id + "'"
        query += ' and reminder_time = ' + str(time_number)
        return self.select(query)

    def select_by_reddit_name(self, reddit_name):
        query = "select * from reminder where player = '" + reddit_name + "'"
        return self.select(query)

    def select_all(self):
        query = "select * from reminder"
        return self.select(query)

    def select(self, query):
        self.__start_query()
        results = self.__query(query)

        reminders_to_return = []
        for result in self.cur:
            reminders_to_return.append([result[0], result[1], result[2]])

        self.__end_query()
        return reminders_to_return

    def __start_query(self):
        self.conn = psycopg2.connect(dbname='mlnbot', user=self.config['user'], password=self.config['password'],
                                     port=self.config['port'], host=self.config['host'])
        self.cur = self.conn.cursor()

    def __end_query(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    reminderDao = ReminderDAO()
    reminderDao.select()