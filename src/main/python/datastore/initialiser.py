import psycopg2

def setup_database():
    commands = [
        '''
        CREATE TABLE reminder (
            player TEXT NOT NULL,
            timeframe long NOT NULL
            PRIMARY KEY (player, timeframe)
        '''
    ]

    try:
        # connect to the PostgreSQL server
        config = __get_config()
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

def __get_config():
    configs = {}
    config_file = open('dbconfig.cfg','r')
    for line in config_file:
        split_line = line.split('=')
        configs[split_line[0]] = split_line[1]

    return configs