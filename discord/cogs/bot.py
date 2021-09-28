import discord
from discord.ext import commands
from discord import Status
from discord import Game
class bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('This bot is online!')
        await self.bot.change_presence(
            status=Status.online,
            activity=Game("nothing in particular"))

    
    @commands.command(aliases = ['h'])
    async def help(self, ctx):
        await ctx.send('why doesnt this work')

