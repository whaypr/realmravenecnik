from bot import client
from aws import s3_sync, wordlist

from random import randrange
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

        wordlist.append(word)
        count += 1

    if count > 0:
        await ctx.send('Slova přidána')
        s3_sync(wordlist)


@client.command(aliases=['remo'])
async def remove(ctx, word, *args):
    '''Remove word to wordlist'''

    try:
        wordlist.remove(word)
    except:
        await ctx.send(f'{word} není v seznamu')
        return

    await ctx.send('Slovo odebráno!')
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

    await ctx.send('Resetováno!')
