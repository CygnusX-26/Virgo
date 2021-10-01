import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases = ['l'])
    async def level(self, ctx, member = None):
        bar = ""
        if member == None:
            userid = ctx.author.id
        else:
            userid = member[3 : -1]
        guildid = ctx.guild.id
        c.execute(f"SELECT * FROM users WHERE id = {userid} AND guild = {guildid}")
        check = c.fetchone()
        #creates the bar
        if check[3] == 0 or check[2] == 0:
            green = 0
        else:
            green = check[2]/check[3]**5-1
        for i in range(10):
            if i < green:
                bar += "🟩"
                continue
            bar += "🟥"
        embed = discord.Embed(
            title=f'Stats for {str(self.bot.get_user(int(userid)))[:-5]}',
            colour= 3553599
        )
        embed.set_thumbnail(url=self.bot.get_user(int(userid)).avatar_url)
        embed.add_field(name=f'Level ▹ {check[3]}', value='\u200b', inline=False)
        embed.add_field(name=f'Total Experience ▹ {check[2]}', value='\u200b', inline=False)
        embed.add_field(name=f'Progress to level {check[3]+1}', value=f'{bar} ▹ {round(green*10, 2)}%', inline=False)
        await ctx.send(embed=embed)


