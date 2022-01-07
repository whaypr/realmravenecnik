from discord.ext import commands
from discord import Game

client = commands.Bot(
    command_prefix='!',
    activity=Game("with ants")
)
