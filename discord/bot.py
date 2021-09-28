import discord
from discord.ext import commands

intents  = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print('This bot is online!')

@client.command()
async def ping(ctx):
    ctx.send('pong')


client.run('Mjc3NTg4NTgzNjkzNjgwNjQw.WJZqgw.pM2qIjTTMh-IfSnL5NrH0vRV-I0')