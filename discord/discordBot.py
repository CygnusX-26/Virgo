import discord
from discord.ext import commands
import sqlite3
from cogs.bot import bot
from cogs.secret import token_
from cogs.level import Level
from cogs.leaderboard import Leaderboard
from cogs.checker import Checker
from discord_buttons_plugin import *

conn = sqlite3.connect('users.db')

c = conn.cursor()

intents  = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')
buttons = ButtonsClient(client)


#creates a new user table if one doesn't currently exist
try:
    c.execute("""CREATE TABLE users (
            id integer,
            guild integer,
            exp integer,
            level integer       
            )""")
except:
    pass

@buttons.click
async def close_button(ctx):
    await ctx.reply(content='Message removed',flags=MessageFlags().EPHEMERAL)
    await ctx.message.delete()

client.add_cog(bot(client))
client.add_cog(Level(client))
client.add_cog(Leaderboard(client))
client.add_cog(Checker(client))


client.run(token_.getToken())