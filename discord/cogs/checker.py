import discord
from discord.ext import commands
import sqlite3
from discord_buttons_plugin import *

conn = sqlite3.connect('users.db')
c = conn.cursor()


#methods for sql
def getUser(id, guild):
    c.execute(f"SELECT * FROM users WHERE id = {id} AND guild = {guild}")
    return c.fetchone()

def getExp(id, guild):
    c.execute(f"SELECT * FROM users WHERE id = {id} AND guild = {guild}")
    return c.fetchone()[2]

def insertUser(id, guild):
    with conn:
        c.execute(f"INSERT INTO users VALUES ({id}, {guild}, 0, 0)")

def updateExp(id, guild):
    c.execute(f"SELECT * FROM users WHERE id = {id} AND guild = {guild}")
    temp = c.fetchone()[2]
    with conn:
        c.execute(f"""UPDATE users SET exp = {temp + 5}
                WHERE id = {id} AND guild = {guild}
                """)

def updateLevel(id, guild):
    c.execute(f"SELECT * FROM users WHERE id = {id} AND guild = {guild}")
    temp = c.fetchone()[3]
    with conn:
        c.execute(f"""UPDATE users SET level = {temp + 1}
                WHERE id = {id} AND guild = {guild}
                """)

def removeUser(id, guild):
    with conn:
        c.execute(f"DELETE from users WHERE id = {id} AND guild = {guild}")

def getSecond(list):
    return list[1]

class Checker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.buttons = ButtonsClient(bot)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author.id
        if message.author.bot:
            return
        guild = message.guild.id
        c.execute(f"SELECT * FROM users")
        check = c.fetchall()
        if len(check) == 0:
            insertUser(user, guild)
            return
        for i in range(len(check)): #either creates new, or updates
            if user in check[i] and guild in check[i]:
                updateExp(user, guild)
                c.execute(f"SELECT * FROM users WHERE id = {user} AND guild = {guild}")
                exp = c.fetchone()[2]
                c.execute(f"SELECT * FROM users WHERE id = {user} AND guild = {guild}")
                lvl_start = c.fetchone()[3]
                lvl_end = int(exp ** (1/5))
                if lvl_start < lvl_end:
                    updateLevel(user, guild)
                    await self.buttons.send(
	                    content = f'{message.author.mention} has leveled up to level {lvl_end}', 
	                    channel = message.channel.id,
	                    components = [
		                ActionRow([
			                Button(
                                emoji = {"id": '893012283930861568', "name": None, "animated": False},
				                label="Close", 
				                style=ButtonType().Danger,
				                custom_id="close_button1"
                                )])])
                return   
        insertUser(user, guild)