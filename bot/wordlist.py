from bot import client

from discord.ext import commands

from os import environ
import psycopg2
import random
import copy


class Database:
    def __init__(self, host, name, user, passwd):
        self.connection = psycopg2.connect(dbname=name, user=user, password=passwd, host=host)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class Wordlist(commands.Cog):
# CONSTRUCTOR
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

        self.wl_remain = copy.deepcopy( self.__get() )


# PRIVATE
    def __add_word(self, word):
        add_word = """
        INSERT INTO wordlist (word) VALUES(%s);
        """
        self.db.cursor.execute( add_word, (word,) )
        self.db.connection.commit()


    def __remove_word(self, word):
        remove_word = """
        DELETE FROM wordlist WHERE word = %s;
        """
        self.db.cursor.execute( remove_word, (word,) )
        self.db.connection.commit()


    def __get(self):
        get_words = """
        SELECT * FROM wordlist;
        """
        self.db.cursor.execute( get_words )
        return [ x[1] for x in self.db.cursor.fetchall() ]


# PUBLIC
    @commands.command(aliases=['ad', 'a'])
    async def add(self, ctx, *args):
        '''Add words to wordlist'''

        wordlist = self.__get()

        new_words = [ x.strip() for x in ' '.join(args).split(',') ]
        count = 0

        for word in new_words:
            if word == '':
                continue
            elif word in wordlist:
                await ctx.send(f'{word} už je v seznamu')
                continue

            self.wl_remain.append(word)
            wordlist.append(word)

            self.__add_word(word)

            count += 1

        if count > 0:
            await ctx.send('Slova přidána')
            

    @commands.command(aliases=['remo'])
    async def remove(self, ctx, *args):
        '''Remove word from wordlist'''

        wordlist = self.__get()

        old_words = [ x.strip() for x in ' '.join(args).split(',') ]
        count = 0

        for word in old_words:
            if word == '':
                continue

            try:
                self.wl_remain.remove(word)
                wordlist.remove(word)

                self.__remove_word(word)

                count += 1
            except:
                await ctx.send(f'{word} není v seznamu')
                continue

        if count > 0:
            await ctx.send('Slova odebrána')


    @commands.command(aliases=['wordlist', 'wl'])
    async def words(self, ctx, *args):
        '''Show all words in wordlist'''

        res = ''

        for word in self.__get():
            res += word + ', '

        if res == '':
            await ctx.send('Seznam je prázdný')    
        else:
            while len(res) > 1900:
                tmp = res[0:1900]
                res = res[1900:len(res)]

                await ctx.send(tmp)
            await ctx.send(res)


    @commands.command(aliases=['sel', 's'])
    async def select(self, ctx, number, *args):
        '''Select number of random remaining words from wordlist'''

        res = ''

        for _ in range(int(number)):
            index = random.randrange( len(self.wl_remain) )
            item = self.wl_remain[index]
            res += item + ', '
            self.wl_remain.remove(item)

        await ctx.send(res)


    @commands.command(aliases=['rem', 'r'])
    async def remains(self, ctx, *args):
        '''Show remaining not used words'''

        res = ''

        for word in self.wl_remain:
            res += word + ', '

        if res == '':
            await ctx.send('Seznam je prázdný')    
        else:
            while len(res) > 1900:
                tmp = res[0:1900]
                res = res[1900:len(res)]

                await ctx.send(tmp)
            await ctx.send(res)


    @commands.command(aliases=['res'])
    async def reset(self, ctx, *args):
        '''Reset wordlist'''

        wordlist = self.__get()
        self.wl_remain = copy.deepcopy(wordlist)

        await ctx.send('Resetováno')


client.add_cog(Wordlist())
