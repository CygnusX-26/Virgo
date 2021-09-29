import discord
from discord import colour
from discord.ext import commands
from discord import Colour
import sqlite3
from cogs.bot import bot
from cogs.secret import token_

conn = sqlite3.connect('users.db')

c = conn.cursor()

intents  = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')


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

# methods for sqlite
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

@client.event
async def on_message(message):
    user = message.author.id
    if message.content.startswith('-'):
        await client.process_commands(message)
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
            lvl_end = int(exp ** (1/4))
            if lvl_start < lvl_end:
                updateLevel(user, guild)
                await message.channel.send(f'{message.author.mention} has leveled up to {lvl_end}')
            #c.execute(f"SELECT * FROM users")
            #print(c.fetchall())
            return   
    insertUser(user, guild)
    #c.execute(f"SELECT * FROM users")
    #print(c.fetchall())

#commands

@client.command(aliases = ['lb'])
async def leaderboard(ctx):
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
                user = await client.fetch_user(i[0])
                embed.add_field(name=f'{user} level: {i[2]}', value=f'{i[1]}', inline=False)
                count += count
            else:
                break
    else:
        for i in explist:
            user = await client.fetch_user(i[0])
            embed.add_field(name=f'{user} level: {i[2]}', value=f'{i[1]}', inline=False)
    
    await ctx.send(embed=embed)

    
client.add_cog(bot(client))


client.run(token_.getToken())