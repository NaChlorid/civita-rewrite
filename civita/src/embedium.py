#
# Embedium
# A list of all Embeds made for the
# Civita discord bot.
#

from datetime import datetime, UTC

import disnake
from disnake import Color, Embed
from mcstatus import JavaServer, BedrockServer
import shit_env
import random

env = shit_env.Env(".env")
CAPI = env.Get("CAPI_ADDRESS")

def TimeToReadable(start_time):
    now = datetime.now(UTC)
    delta = now - start_time

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_str = ""
    if days > 0:
        uptime_str += f"{days}d "
    if hours > 0 or days > 0:
        uptime_str += f"{hours}h "
    if minutes > 0 or hours > 0 or days > 0:
        uptime_str += f"{minutes}m "
    uptime_str += f"{seconds}s"

    return uptime_str


def BotinfoEmbed(start_time, version):
    # Return the embed
    return Embed(
        title="<:logo:1474439803670892737> Civita's Information",
        description=f"Civita is a multifunctional discord bot made on Python.\n\nUptime: {TimeToReadable(start_time)}\nVersion: {version}\n\n Thanks to:\n - <:NaCl:1477258011415281765> Opt1mi [Developer]\n - <:InfX:1477258309097488385> InfiniteX321 [Helper] \n - <:NaCl:1477258011415281765> Frosteyyy__ [NaChlorid Team]\n\n Without these people Civita wouldn't exist right now, thank you to each one of them!\n\nFind my source code at https://git.chlorid.org/civita/civita-base",
        color=Color.orange(),
    )

#
# Server Information Embed
# Needs: CTX
#
def ServerInfoEmbed(ctx):

    # Get some data before returning it
    guild = ctx.guild
    server_name = guild.name
    member_count = guild.member_count

    # Check how many clankers and Chronically online people are there
    humans = sum(1 for member in ctx.guild.members if not member.bot)
    bots = sum(1 for member in ctx.guild.members if member.bot)

    # Return the data back to main.py
    return Embed(
        title=f"Server Information",
        description=f"Server name: {server_name}\nMember count: {member_count} \nHumans: {humans} \nBots: {bots}\nOwner: {guild.owner}",
        color=Color.orange(),
    )

def CommandsEmbed():

    # Deport the data back to main.py
    return Embed(
        title=f"Commands",
        description=f"**General**\n`/announce` - Announce something to the server \n `/info bot/server/commands` - Prints information about the bot, it's commands or about the server. \n---\n**Moderation**\n`$ban (mention) (reason)` - ban a user\n`$kick (mention) (reason)` - kick a user\n`/unban (User ID) (reason)` - Unban a user\n\n**API**\n`/api` - Shows all the API features of Civita and CAPI\n\n**Fun**\n`/mcjs_status (IP WITH PORT)` - Show the status of a minecraft: java edition server\n`/coinflip` - flips a coin, I bet it's Tails :p\n`/search` - Searches for something on the internet ",
        color=Color.orange(),
    )

def AnnounceEmbed(ctx, title, text, color):
    if color == "green":
        return Embed(
            title=title,
            description=text,
            color=disnake.Color.green()
        )

    if color == "red":
        return Embed(
            title=title,
            description=text,
            color=disnake.Color.red()
        )

    if color == "blue":
        return Embed(
            title=title,
            description=text,
            color=disnake.Color.blue()
        )

    if color == "blurple":
        return Embed(
            title=title,
            description=text,
            color=disnake.Color.blurple()
        )

    return Embed(
        title=title,
        description=text,
        color=disnake.Color.light_gray()
    )


def BanSuccessEmbed(ctx, member, reason):
    return Embed(
        title="<:worked:1474435965530669098> Success",
        description=f"User {member} has been banned.\n Reason: {reason}\n Banned by {ctx.author.mention}",
        color=Color.green()
    )

def KickSuccessEmbed(ctx, member, reason):
    return Embed(
        title="<:worked:1474435965530669098> Success",
        description=f"User {member} has been kicked.\n Reason: {reason}\n Kicked by {ctx.author.mention}",
        color=Color.green()
    )

def UnbanSuccessEmbed(ctx, member, reason):
    return Embed(
        title="<:worked:1474435965530669098> Success",
        description=f"User {member} has been unbanned.\n Reason: {reason}\n Unbanned by {ctx.author.mention}",
        color=Color.green()
    )

def JavaStatusEmbed(address):
    server = JavaServer.lookup(address)

    try:
        status = server.status()
    except Exception as e:
        raise Exception(f"Failed to retrieve Minecraft server status for '{address}': {e}")

    try:
        query = server.query()
        player_list = ", ".join(query.players.names) if query.players.names else "No players listed"
    except Exception:
        player_list = "Query disabled"

    try:
        ping = server.ping()
    except Exception:
        ping = "Unknown"

    return Embed(
        title=f"<:mcserver:1474437524473647216> {address} Status",
        description=(
            f"**General**\n"
            f"IP: {address}\n"
            f"Players: {status.players.online}/{status.players.max}\n"
            f"Ping: {ping}\n\n"
            f"**Players Online**\n"
            f"{player_list}"
        ),
        color=Color.green()
    )

def BedrockStatusEmbed(address):
    server = BedrockServer.lookup(address)

    try:
        status = server.status()
    except Exception as e:
        raise Exception(f"Failed to retrieve Minecraft server status for '{address}': {e}")

    try:
        query = server.query()
        player_list = ", ".join(query.players.names) if query.players.names else "No players listed"
    except Exception:
        player_list = "Query disabled"

    try:
        ping = server.ping()
    except Exception:
        ping = "Unknown"

    return Embed(
        title=f"<:mcserver:1474437524473647216> {address} Status",
        description=(
            f"**General**\n"
            f"IP: {address}\n"
            f"Players: {status.players.online}/{status.players.max}\n"
            f"Ping: {ping}\n\n"
            f"**Players Online**\n"
            f"{player_list}"
        ),
        color=Color.green()
    )

def APIEmbed():
    return Embed(
        title=f"API Documentation",
        description=f'''
        cAPI is an API made with Flask which comes in the Civita-rewrite package.
        It's a powerful API to get info about discord servers by their IDs and general Civita information which you can also get by using `$info bot`
        
        Current cAPI Host:
        **{CAPI}**
        
        **Usage**
        `/v2/server/<ID>` - Get information about a specific server by its ID
        `/v2/server_count/` - Get Civita's server count
        `/v2/servers` - Get all servers which use Civita (yes you agreed to that when you checked our Privacy Policy page ;) )        
        ''',
        color=Color.green()
    )

def CoinFlipEmbed():
    res = random.choice(['heads', 'tails'])
    return Embed(
        title=f"Coin Flip",
        description=f'''
            It's {res}
        ''',
        color=Color.green()
    )

def CMDFail(err):
    return Embed(
        title="<:failed:1474435933465219216> Fail",
        description=f"The command failed to run\n```{err}```",
        color=Color.red()
    )
