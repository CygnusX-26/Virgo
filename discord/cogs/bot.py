import discord
from discord.ext import commands
class bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('This bot is online!')
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game("nothing in particular"))

    
    @commands.command(aliases = ['h'])
    async def help(self, ctx):
        embed = discord.Embed(
            title=f'Help menu for Virgo',
            descriprion='List of commands for Virgo',
            colour=discord.Colour.green()
        )
        embed.add_field(name='Help ', value='▹ displays this menu!', inline=False)
        embed.add_field(name='Leaderboard', value='▹ displays the guild leaderboard', inline=False)

        await ctx.send(embed=embed)

