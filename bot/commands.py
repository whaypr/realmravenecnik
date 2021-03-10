from bot import client
from aws import s3_sync, wordlist

from random import randrange
import requests
from bs4 import BeautifulSoup
import copy

wl_tmp = copy.deepcopy(wordlist)


@client.command(aliases=['ad', 'a'])
async def add(ctx, *args):
    '''Add words to wordlist'''

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
        count += 1

    if count > 0:
        await ctx.send('Slova přidána')
        s3_sync(wordlist)


@client.command(aliases=['remo'])
async def remove(ctx, *args):
    '''Remove word to wordlist'''

    old_words = [ x.strip() for x in ' '.join(args).split(',') ]
    count = 0

    for word in old_words:
        if word == '':
            continue

        try:
            global wl_tmp
            wl_tmp.remove(word)
            wordlist.remove(word)
            count += 1
        except:
            await ctx.send(f'{word} není v seznamu')
            continue

    if count > 0:
        await ctx.send('Slova odebrána')
        s3_sync(wordlist)


@client.command(aliases=['wordlist', 'wl'])
async def words(ctx, *args):
    '''Show all words in wordlist'''

    res = ''

    for word in wordlist:
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
        index = randrange(len(wl_tmp))
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
        await ctx.send(res)


@client.command(aliases=['res'])
async def reset(ctx, *args):
    '''Reset wordlist'''

    global wl_tmp
    wl_tmp = copy.deepcopy(wordlist)

    await ctx.send('Resetováno')


#######################################


@client.command(aliases=['cut'])
async def cute(ctx, *args):
    '''Random cute animal'''

    if str(ctx.channel.id) != '819249350156353578':
        return

    image_number = randrange(9999)

    page = requests.get(f'http://attackofthecute.com/on/?i={image_number}')
    soup = BeautifulSoup(page.content, 'html.parser')
    image_link = soup.find('div', class_='image').find('img')['src']

    await ctx.send(image_link)
