import psycopg2

from src.main.python.configuration_storage import Configs


def setup_database(config_file_path):
    commands = [
        '''
        CREATE TABLE reminder (
            discord_id TEXT NOT NULL,
            player TEXT NOT NULL,
            reminder_time INTEGER NOT NULL,
            PRIMARY KEY (discord_id, reminder_time)
        );
        '''
    ]

    try:
        # connect to the PostgreSQL server
        config = Configs(config_file_path).get_all_configs()
        conn = psycopg2.connect(dbname='mlnbot',user=config['user'],password=config['password'],port=config['port'],host=config['host'])
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def purge_database():
    pass


if __name__ == '__main__':
    setup_database()