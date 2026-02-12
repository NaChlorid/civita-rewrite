#
# Embedium
# A list of all Embeds made for the
# Civita discord bot.
#

from datetime import datetime
from disnake import Color, Embed

def TimeToReadble(start_time):
    now = datetime.utcnow()
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
    # Deport the embed
    return Embed(
        title="Civita's Information",
        description=f"Civita is a multifunctional discord bot made on Python.\n\nUptime: {TimeToReadble(start_time)}\nVersion: {version}",
        color=Color.orange(),
    )

#
# Server Information Embed
# Needs: CTX
#
def ServerInfoEmbed(ctx):

    # Get some data before deporting it
    guild = ctx.guild
    server_name = guild.name
    member_count = guild.member_count

    # Check how many clankers and Chronically online people are there
    humans = sum(1 for member in ctx.guild.members if not member.bot)
    bots = sum(1 for member in ctx.guild.members if member.bot)

    # Deport the data back to main.py
    return Embed(
        title=f"Server Information",
        description=f"Server name: {server_name}\nMember count: {member_count} \nHumans: {humans} \nBots: {bots}\nOwner: {guild.owner}",
        color=Color.orange(),
    )

def CommandsEmbed():

    # Deport the data back to main.py
    return Embed(
        title=f"Commands",
        description=f"**General**\n`$info bot/server/commands` - Prints information about the bot, it's commands or about the server. \n---\n**Moderation**\n`$ban (mention) (reason)` - ban a user\n`$kick (mention) (reason)` - kick a user\n`$unban (User ID) (reason)` - Unban a user\n",
        color=Color.orange(),
    )

def BanSuccessEmbed(ctx, member, reason):
    return Embed(
        title="Success",
        description=f"User {member} has been banned.\n Reason: {reason}\n Banned by {ctx.author.mention}",
        color=Color.green()
    )

def KickSuccessEmbed(ctx, member, reason):
    return Embed(
        title="Success",
        description=f"User {member} has been kicked.\n Reason: {reason}\n Kicked by {ctx.author.mention}",
        color=Color.green()
    )

def UnbanSuccessEmbed(ctx, member, reason):
    return Embed(
        title="Success",
        description=f"User {member} has been unbanned.\n Reason: {reason}\n Unbanned by {ctx.author.mention}",
        color=Color.green()
    )

def CMDFail():
    return Embed(
        title="Fail",
        description="The command failed to run, do you have the privileges to run it?",
        color=Color.red()
    )