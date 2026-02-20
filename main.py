#
# (C) Civita Contributors and NaChlorid Germany UG
# This project is licensed under MIT.
#
# Civita is a multifucktional discord bot made
# with disnake, shit-env, and pure columbian cocaine.
#
# "
# To whom it may concern,
# This letter is to verify that The NaChlorid Germany Organisation(d.b.a NaChlorid) is acting as the Technical Sponsor for The NaChlorid Germany Organisation since 10.02.2026.
# As part of this arrangement, NaChlorid provides technical support to The NaChlorid Germany Organisation, including the provision of hardware and related equipment necessary for their operations and programs.
# The NaChlorid Germany is a § (52 AO) public charity.
# "
#

from datetime import datetime
import mcstatus
import disnake
import shit_env
from disnake.ext import commands, tasks
from embedium import BotinfoEmbed, ServerInfoEmbed, CommandsEmbed, BanSuccessEmbed, BanSuccessEmbed, \
    CMDFail, KickSuccessEmbed, UnbanSuccessEmbed, ServerStatusEmbed, APIEmbed
import asyncio
from google import genai


env = shit_env.Env(".env")
VERSION = env.Get("VERSION")
TOKEN_GENAI = env.Get("TOKEN_GEMINI")
client = genai.Client(api_key=TOKEN_GENAI)
intents = disnake.Intents.all()
# intents.guilds = True     # Stupid Optimi doesnt know how to code. Burn in hell!
start_time = datetime.utcnow()

bot = commands.Bot(command_prefix="$", intents=intents)
bot.server_count = 25

@tasks.loop(minutes=5)
async def update_status():
    bot.server_count = len(bot.guilds)
    activity = disnake.Game(f"{bot.server_count} Servers | {VERSION}")
    await bot.change_presence(activity=activity)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()

@bot.command()
async def mcjs_status(ctx, address):
    try:
        await ctx.send(embed=ServerStatusEmbed(address))
    except Exception as e:
        await ctx.send(f"Something went wrong, did you enter the port?\n if still doesnt work, please send the following text to opt1mi:\n```{e}```")

@bot.command()
async def info(ctx, additional):
    if additional == "bot":
        await ctx.send(embed=BotinfoEmbed(start_time, version=VERSION))

    elif additional == "server":
        await ctx.send(embed=ServerInfoEmbed(ctx))

    elif additional == "commands":
        await ctx.send(embed=CommandsEmbed())

@bot.command()
async def ban(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await ctx.send(embed=BanSuccessEmbed(ctx, user, reason=reason))

    else:
        await ctx.send(embed=CMDFail())

@bot.command()
async def kick(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await ctx.send(embed=KickSuccessEmbed(ctx, user, reason=reason))

    else:
        await ctx.send(embed=CMDFail())

@bot.command()
async def unban(ctx, user_ID: int, reason):
    if ctx.author.guild_permissions.ban_members:
        try:
            user = await bot.fetch_user(user_ID)  # Fetch user from ID
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(embed=UnbanSuccessEmbed(ctx, user, reason=reason))
        except Exception as e:
            await ctx.send(f"Failed to unban user ID {user_ID}: {e}")

    else:
        await ctx.send(embed=CMDFail())

@bot.command()
async def api(ctx):
    await ctx.send(embed=APIEmbed())

@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """
    Ask the Gemini model something (no chat history).
    Usage: $ask Why is the sky blue?
    """
    await ctx.trigger_typing()

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