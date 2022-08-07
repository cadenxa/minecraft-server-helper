import discord
from mcstatus import JavaServer

# ---------------------------------------------------------------
#   simple self-hosted minecraft server helper Discord bot :>
# ---------------------------------------------------------------
# (c) Cadence Boyce 2022
# Free to use and modify for personal/educational purposes.

# Requirements: 
# - Python 3.8 or higher
# - Pycord https://docs.pycord.dev/en/master/
# - mcstatus https://github.com/py-mine/mcstatus 
# - An application with a bot account on the Discord development portal https://discord.com/developers/applications 

# OAuth2 scopes needed: bot, applications.commands
# In this code, "server" refers to a Minecraft Java Edition server and "guild" refers to a Discord server.
# The Minecraft server I use this for is a private friend server, so the IP has been redacted. 
# Replace SERVER IP with the IP (and port if needed) of your own Minecraft server!

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}") # Gives console feedback when the bot logs on

# Status Change
# The bot's status becomes an easy reference for whether the server is online
# updates when a message is sent in any of the guilds the bot is in
@bot.event
async def on_message(message):
    try:
        server = JavaServer.lookup("SERVER IP") # Use quotes for server IP in JavaServer.lookup and Javaserver.query
        serverstatus = server.status()
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Minecraft with {} players | SERVER IP".format(serverstatus.players.online)))
    except:
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Server offline :( | SERVER IP"))
    return

# I created local slash commands for the 2 guilds my bot joined so that the slash commands would register immediately.
# To use these local slash commands, replace "GUILD ID" with your guild ID __without__ quotes. 
# To get a guild ID, enable Developer Mode in the Advanced section of your Discord account settings and right click your guild's name.
# To instead make global slash commands so you don't have to change the code whenever the bot joins a new guild,
# at the cost of taking up to a couple hours for the commands to register, leave the parentheses of @bot.slash_command() blank.

# /ip
# Lists the server's IP and gives other useful information to people who want to join the Minecraft server.
@bot.slash_command(guild_ids=["GUILD ID","GUILD ID"]) 
async def ip(ctx):
    await ctx.respond("The server's IP is SERVER IP. If joining for the first time, make sure you're on the whitelist!")

# /bee
# sends picture of Minecraft bee :)
@bot.slash_command(guild_ids=["GUILD ID","GUILD ID"])
async def bee(ctx):
    await ctx.respond("https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7c/Bee_types.gif")
    # GIF by Pneuma01 from the Minecraft Wiki (https://minecraft.fandom.com)

# /online
# Gives a list of usernames of the players online.
# Requires the query property to be set to true in your Minecraft server's properties.
@bot.slash_command(guild_ids=["GUILD ID","GUILD ID"]) 
async def online(ctx):
    try:
        server = JavaServer.lookup("SERVER IP")
        serverquery = server.query()
        await ctx.respond("The following players are online: {}".format(', '.join(serverquery.players.names)))
    except:
        await ctx.respond("The server is offline.")

# @bot.event
# async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
#     await ctx.respond("The server is offline.") 
# ^ I have not gotten this part to do anything </3 please ignore it!
# If you try to use /online or any slash command that queries your Minecraft server while it is offline, the
# bot will simply send a message to the command sender that it stopped responding. Not the nicest solution but it works.

bot.run("TOKEN") 
# Replace "TOKEN" with your bot's token (found in your developer portal) with quotes
# so that the bot will come online when the program runs.

# Once you've installed all the dependencies and changed all the placeholders in the code, just save and launch this .py script.
# Resetting the token in the Discord developer portal is a good way to shut down the bot quickly so you can make changes in the code.