from os import environ
import psycopg2


class Database:
    def __init__(self, host, name, user, passwd):
        self.connection = psycopg2.connect(dbname=name, user=user, password=passwd, host=host)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class Wordlist:
    def __init__(self):
        self.db = Database(
            "ec2-18-203-64-130.eu-west-1.compute.amazonaws.com",
            environ['DB_NAME'],
            environ['DB_USER'],
            environ['DB_PASS']
        )

        create_table = """
        CREATE TABLE IF NOT EXISTS
        wordlist(id SERIAL PRIMARY KEY, word VARCHAR);
        """
        self.db.cursor.execute(create_table)

    def add_word(self, word):
        add_word = """
        INSERT INTO wordlist (word) VALUES(%s);
        """
        self.db.cursor.execute( add_word, (word,) )
        self.db.connection.commit()

    def remove_word(self, word):
        remove_word = """
        DELETE FROM wordlist WHERE word = %s;
        """
        self.db.cursor.execute( remove_word, (word,) )
        self.db.connection.commit()

    def get(self):
        get_words = """
        SELECT * FROM wordlist;
        """
        self.db.cursor.execute( get_words )
        return [ x[1] for x in self.db.cursor.fetchall() ]


wl = Wordlist()
