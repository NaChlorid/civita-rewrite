#
# (C) Civita Contributors
# This project is licensed under MIT.
#
# Civita is a multifunctional discord bot made
# with disnake, shit-env, and the mcstatus library
#

# -> Imports
from datetime import datetime, UTC
import disnake
import shit_env
from disnake.ext import commands, tasks
from .embedium import BotinfoEmbed, ServerInfoEmbed, CommandsEmbed, BanSuccessEmbed, \
    CMDFail, KickSuccessEmbed, UnbanSuccessEmbed, ServerStatusEmbed, APIEmbed, CoinFlipEmbed
import asyncio
from google import genai

# -> Variables
env = shit_env.Env(".env")
VERSION = env.Get("VERSION")
TOKEN_GENAI = env.Get("TOKEN_GEMINI")
client = genai.Client(api_key=TOKEN_GENAI)
intents = disnake.Intents.all()
start_time = datetime.now(UTC)

# -> Initialise the bot
bot = commands.Bot(intents=intents)
bot.server_count = 0

# Update the status every 5 minutes
@tasks.loop(minutes=5)
async def update_status():
    bot.server_count = len(bot.guilds)
    activity = disnake.Game(f"{bot.server_count} Servers | {VERSION}")
    await bot.change_presence(activity=activity)

# When the bot starts and is ready:
# \
#  | -> Say it
#  | -> Start updating the status
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()

# mcjs command
@bot.slash_command(name="mcjs_status", description="Get a Minecraft: Java Edition server status")
async def mcjs_status(ctx, address: str):
    try:
        await ctx.response.defer()
        await ctx.send(embed=ServerStatusEmbed(address))
    except Exception as e:
        await ctx.send(embed=CMDFail(e))

# info command
@bot.slash_command(name="info", description="Get info about the bot/server or commands")
async def info(
    ctx,
    additional: str = commands.Param(choices=["bot", "server", "commands"])
):
    if additional == "bot":
        await ctx.send(embed=BotinfoEmbed(start_time, version=VERSION))

    elif additional == "server":
        await ctx.send(embed=ServerInfoEmbed(ctx))

    elif additional == "commands":
        await ctx.send(embed=CommandsEmbed())

#
#   Moderation commands
#

#ban command
@bot.slash_command(name="ban", description="Ban a user")
async def ban(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await ctx.send(embed=BanSuccessEmbed(ctx, user, reason=reason))

    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))
#kick command
@bot.slash_command(name="kick", description="Kick a user")
async def kick(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await ctx.send(embed=KickSuccessEmbed(ctx, user, reason=reason))

    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))

#unban command
@bot.slash_command(name="unban", description="Unban a user")
async def unban(ctx, user_id: int, reason):
    if ctx.author.guild_permissions.ban_members:
        try:
            user = await bot.fetch_user(user_id)  # Fetch user from ID
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(embed=UnbanSuccessEmbed(ctx, user, reason=reason))
        except Exception as e:
            await ctx.send(embed=CMDFail(e))

    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))
# API command
@bot.slash_command(name="api", description="Get the cAPI documentation")
async def api(ctx):
    await ctx.send(embed=APIEmbed())

# Coinflip command
@bot.slash_command(name="coinflip", description="Flip a coin")
async def coinflip(ctx):
    await ctx.send(embed=CoinFlipEmbed())

# Ask command
@bot.slash_command(name="ask", description="Use the AI")
async def ask(ctx, *, question: str):
    await ctx.response.defer()
    loop = asyncio.get_event_loop()

    def run_gemini():
        try:
            # One-off chat; no history
            chat = client.chats.create(model="gemini-2.5-flash-lite")
            response = chat.send_message(question)
            return response.text
        except Exception as e:
            return f"AI exploded, check this:\n{e}"

    try:
        response_text = await loop.run_in_executor(None, run_gemini)

        # Discord message limit safety
        if len(response_text) > 2000:
            for i in range(0, len(response_text), 2000):
                await ctx.send(response_text[i:i+2000])
        else:
            await ctx.send(response_text)

    except Exception as e:
        await ctx.send(f"Unexpected error:\n```{e}```")
