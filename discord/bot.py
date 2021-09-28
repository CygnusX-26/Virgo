import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()

intents  = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')

try:
    c.execute("""CREATE TABLE users (
            id integer,
            guild integer,
            exp integer,
            level integer       
            )""")
except:
    pass

def getUser(id, guild):
    c.execute(f"SELECT * FROM users WHERE id = {id} AND guild = {guild}")
    return c.fetchone()

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



@client.event
async def on_ready():
    print('This bot is online!')

@client.event
async def on_message(message):
    user = message.author.id
    if message.author.bot:
        return
    guild = message.guild.id
    c.execute(f"SELECT * FROM users")
    check = c.fetchall()
    if len(check) == 0:
        insertUser(user, guild)
        return
    #either creates new, or updates
    for i in range(len(check)):
        if user in check[i] and guild in check[i]:
            updateExp(user, guild)
            c.execute(f"SELECT * FROM users WHERE id = {user} AND guild = {guild}")
            exp = c.fetchone()[2]
            c.execute(f"SELECT * FROM users WHERE id = {user} AND guild = {guild}")
            lvl_start = c.fetchone()[3]
            lvl_end = int(exp ** (1/4))
            if lvl_start < lvl_end:
                updateLevel(user, guild)
                await message.channel.send(f'{message.author.mention} has leveled up to {lvl_end}')
            c.execute(f"SELECT * FROM users")
            print(c.fetchall())
            return   
    insertUser(user, guild)
    c.execute(f"SELECT * FROM users")
    print(c.fetchall())



@client.command()
async def ping(ctx):
    ctx.send('pong')


client.run('token')