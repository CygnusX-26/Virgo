import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
def getSecond(list):
    return list[1]
    
class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(aliases = ['lb'])
    async def leaderboard(self, ctx):
        guild = ctx.guild.id
        explist = []
        c.execute(f"SELECT * FROM users WHERE guild = {guild}")
        check = c.fetchall()
        for i in check:
            explist.append([i[0], i[2], i[3]])
        explist.sort(key=getSecond, reverse=True)
        embed = discord.Embed(
            title=f'Leaderboard for {ctx.guild}',
            color=3553599
        )
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        if len(explist) > 5:
            count = 0
            for i in explist:
                if count <= 5:
                    user = await self.bot.fetch_user(i[0])
                    embed.add_field(name=f'{user} ▹ level: {i[2]}', value=f'{i[1]}', inline=False)
                    count += count
                else:
                    break
        else:
            for i in explist:
                user = await self.bot.fetch_user(i[0])
                embed.add_field(name=f'{user} ▹ level: {i[2]}', value=f'{i[1]}', inline=False)
    
        await ctx.send(embed=embed)
    