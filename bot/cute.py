from bot import client

import requests
import random


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
