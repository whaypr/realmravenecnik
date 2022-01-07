from bot import client
from wordlist import wl

import requests
import random
import copy

wl_tmp = copy.deepcopy(wl.get())


@client.command(aliases=['ad', 'a'])
async def add(ctx, *args):
    '''Add words to wordlist'''

    wordlist = wl.get()

    new_words = [ x.strip() for x in ' '.join(args).split(',') ]
    count = 0

    for word in new_words:
        if word == '':
            continue
        elif word in wordlist:
            await ctx.send(f'{word} už je v seznamu')
            continue

        global wl_tmp
        wl_tmp.append(word)
        wordlist.append(word)

        wl.add_word(word)

        count += 1

    if count > 0:
        await ctx.send('Slova přidána')
        

@client.command(aliases=['remo'])
async def remove(ctx, *args):
    '''Remove word to wordlist'''

    wordlist = wl.get()

    old_words = [ x.strip() for x in ' '.join(args).split(',') ]
    count = 0

    for word in old_words:
        if word == '':
            continue

        try:
            global wl_tmp
            wl_tmp.remove(word)
            wordlist.remove(word)

            wl.remove_word(word)

            count += 1
        except:
            await ctx.send(f'{word} není v seznamu')
            continue

    if count > 0:
        await ctx.send('Slova odebrána')


@client.command(aliases=['wordlist', 'wl'])
async def words(ctx, *args):
    '''Show all words in wordlist'''

    res = ''

    for word in wl.get():
        res += word + ', '

    if res == '':
        await ctx.send('Seznam je prázdný')    
    else:
        while len(res) > 1900:
            tmp = res[0:1900]
            res = res[1900:len(res)]

            await ctx.send(tmp)
        await ctx.send(res)


@client.command(aliases=['sel', 's'])
async def select(ctx, number, *args):
    '''Select number of random remaining words from wordlist'''

    res = ''

    for _ in range(int(number)):
        index = random.randrange(len(wl_tmp))
        item = wl_tmp[index]
        res += item + ', '
        wl_tmp.remove(item)

    await ctx.send(res)


@client.command(aliases=['rem', 'r'])
async def remains(ctx, *args):
    '''Show remaining not used words'''

    res = ''

    for word in wl_tmp:
        res += word + ', '

    if res == '':
        await ctx.send('Seznam je prázdný')    
    else:
        while len(res) > 1900:
            tmp = res[0:1900]
            res = res[1900:len(res)]

            await ctx.send(tmp)
        await ctx.send(res)


@client.command(aliases=['res'])
async def reset(ctx, *args):
    '''Reset wordlist'''

    wordlist = wl.get()

    global wl_tmp
    wl_tmp = copy.deepcopy(wordlist)

    await ctx.send('Resetováno')


#######################################

@client.command(aliases=['cut'])
async def cute(ctx, *args):
    '''Random cute animal'''

    # on napotitku server but not in pure-cuteness channel
    if str(ctx.guild.id) == '537212948460863498' and str(ctx.channel.id) != '819249350156353578':
        return

    subreddits = ['aww', 'Awww', 'cute_animals', 'babyanimals']
    limit = 1
    timeframe = 'all' #hour, day, week, month, year, all
    listing = 'random' # controversial, best, hot, new, random, rising, top
    base_url = f'https://www.reddit.com/r/{random.choice(subreddits)}/{listing}.json?limit={limit}&t={timeframe}'

    res = ""
    while not res.lower().endswith(('.jpg', '.png', '.gif', '.jpeg')):
        response = requests.get(base_url, headers = {'User-agent': 'Pure cuteness dealer'}).json()
        res = response[0]["data"]["children"][0]["data"]["url"]

    await ctx.send(res)
