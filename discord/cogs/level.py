import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases = ['l'])
    async def level(self, ctx):
        userid = ctx.author.id
        guildid = ctx.guild.id
        c.execute(f"SELECT * FROM users WHERE id = {userid} AND guild = {guildid}")
        check = c.fetchone()
        embed = discord.Embed(
            title=f'Stats for {ctx.author.name}',
            colour= 3553599
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f'Level ▹ {check[3]}', value='\u200b', inline=False)
        embed.add_field(name=f'Total Experience ▹ {check[2]}', value='\u200b', inline=False)
        await ctx.send(embed=embed)

