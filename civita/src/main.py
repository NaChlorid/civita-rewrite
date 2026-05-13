#
# (C) Civita Contributors
# This project is licensed under MIT.
#
# Civita is a multifunctional discord bot made
# with disnake, shit-env, and the mcstatus library
#

# -> Imports
from datetime import datetime, UTC
from typing import Optional

import disnake
from disnake.ext import commands, tasks
from .embedium import BotinfoEmbed, ServerInfoEmbed, CommandsEmbed, BanSuccessEmbed, \
    CMDFail, KickSuccessEmbed, UnbanSuccessEmbed, JavaStatusEmbed, BedrockStatusEmbed, APIEmbed, CoinFlipEmbed, AnnounceEmbed
import asyncio
import aiohttp
from mistralai.client import Mistral
from config import TOKEN_MISTRAL, VERSION


# -> Variables
client = Mistral(api_key=TOKEN_MISTRAL)
intents = disnake.Intents.all()
start_time = datetime.now(UTC)

# -> Initialise the bot
bot = commands.InteractionBot(
    default_install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    default_contexts=disnake.InteractionContextTypes(
        guild=True,
        bot_dm=True,
        private_channel=True,
    ),
)
bot.server_count = 0

# Update the status every 5 minutes
@tasks.loop(minutes=5)
async def update_status():
    bot.server_count = len(bot.guilds)
    activity = disnake.Game(f"{bot.server_count} Servers | {VERSION}")
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()

# MinecraftServer command
@bot.slash_command(
    name="mcstatus",
    description="Look up a Minecraft server's status",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def mcstatus(ctx,
                   address: str,
                   edition: str = commands.Param(choices=["Java", "Bedrock"])):
    await ctx.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mcsrvstat.us/3/{address}") as resp:
                data = await resp.json()

        if not data.get("online"):
            await ctx.send(embed=CMDFail(f"Server `{address}` is offline or unreachable."))
            return

        motd = data.get("motd", {}).get("clean", ["No MOTD"])[0].strip()
        players_online = data.get("players", {}).get("online", 0)
        players_max = data.get("players", {}).get("max", 0)
        version = data.get("version", "Unknown")
        icon_url = f"https://api.mcsrvstat.us/icon/{address}"

        embed = disnake.Embed(
            title=address,
            description=f"*{motd}*",
            color=0x5C8731
        )
        embed.add_field(name="Players", value=f"{players_online}/{players_max}", inline=True)
        embed.add_field(name="Version", value=version, inline=True)
        embed.set_thumbnail(url=icon_url)
        embed.set_footer(text="Powered by mcsrvstat.us")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(embed=CMDFail(e))

@bot.slash_command(name="announce", description="[ADMIN ONLY] Sends a pretty announcement")
async def announce(
        ctx,
        title,
        text,
        mode: str = commands.Param(choices=["message", "embed"]),
        color: Optional[str] = commands.Param(choices=["green", "red", "blurple", "blue"])
):
    if ctx.author.guild_permissions.administrator:
        if mode == "embed":
            await ctx.send(embed=AnnounceEmbed(ctx, title, text, color))
        else:
            await ctx.send(f'# {title}\n\n{text}')
    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permission to run this!"))

# info command
@bot.slash_command(
    name="info",
    description="Get infos about the bot/server or commands",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
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

@bot.slash_command(name="ban", description="Ban a user")
async def ban(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await ctx.send(embed=BanSuccessEmbed(ctx, user, reason=reason))
    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))

@bot.slash_command(name="kick", description="Kick a user")
async def kick(ctx, user: disnake.Member, *, reason):
    if ctx.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await ctx.send(embed=KickSuccessEmbed(ctx, user, reason=reason))
    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))

@bot.slash_command(name="unban", description="Unban a user")
async def unban(ctx, user_id: int, reason):
    if ctx.author.guild_permissions.ban_members:
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(embed=UnbanSuccessEmbed(ctx, user, reason=reason))
        except Exception as e:
            await ctx.send(embed=CMDFail(e))
    else:
        await ctx.send(embed=CMDFail(f"{ctx.author} doesn't have the permissions to execute this!"))

@bot.slash_command(
    name="capi",
    description="Info's about the Civita API",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def api(ctx):
    await ctx.send(embed=APIEmbed())

@bot.slash_command(
    name="coinflip",
    description="Heads or Tails?",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def coinflip(ctx):
    await ctx.send(embed=CoinFlipEmbed())

@bot.slash_command(
    name="userinfo",
    description="Get info about a user",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def userinfo(ctx, user: disnake.User = None):
    user = user or ctx.author
    created_at = user.created_at.strftime("%B %d, %Y")

    embed = disnake.Embed(title=user.name, color=user.accent_color or 0x5865F2)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="ID", value=f"`{user.id}`", inline=True)
    embed.add_field(name="Account Created", value=created_at, inline=True)

    in_guild = ctx.context.guild
    if in_guild:
        member = ctx.guild.get_member(user.id)
        if member:
            joined_at = member.joined_at.strftime("%B %d, %Y")
            roles = [r.mention for r in member.roles if r.name != "@everyone"]
            roles_value = ", ".join(roles) if roles else "No roles"
            embed.add_field(name="Joined Server", value=joined_at, inline=True)
            embed.add_field(name="Roles", value=roles_value, inline=False)

    await ctx.send(embed=embed)

@bot.slash_command(
    name="mcwiki",
    description="Search the Minecraft wiki",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def mcwiki(ctx, query: str):
    await ctx.response.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://minecraft.wiki/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 1,
            }
        ) as resp:
            search_data = await resp.json()

        results = search_data["query"]["search"]
        if not results:
            await ctx.send(embed=CMDFail(f"No results found for `{query}`."))
            return

        page_title = results[0]["title"]
        page_url = f"https://minecraft.wiki/w/{page_title.replace(' ', '_')}"

        async with session.get(
            "https://minecraft.wiki/api.php",
            params={
                "action": "query",
                "prop": "extracts|pageimages",
                "titles": page_title,
                "format": "json",
                "exintro": "1",
                "explaintext": "1",
                "pithumbsize": 256,
            }
        ) as resp:
            extract_data = await resp.json()

    page = next(iter(extract_data["query"]["pages"].values()))
    extract = page.get("extract", "")
    thumbnail = page.get("thumbnail", {}).get("source")

    try:
        response = await client.chat.complete_async(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this Minecraft wiki article in 3-4 sentences, keep it simple and clear:\n\n{extract}"
                }
            ]
        )
        summary = response.choices[0].message.content
    except Exception as e:
        summary = f"AI error: {e}"

    embed = disnake.Embed(
        title=page_title,
        url=page_url,
        description=summary,
        color=0x5C8731
    )
    embed.set_footer(text="Summarized from minecraft.wiki")
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    await ctx.send(embed=embed)

@bot.slash_command(
    name="mcplayer",
    description="Look up a Minecraft player",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def mcplayer(ctx, username: str):
    await ctx.response.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as resp:
            if resp.status == 404:
                await ctx.send(embed=CMDFail(f"Player `{username}` not found."))
                return
            data = await resp.json()

    uuid = data["id"]
    name = data["name"]
    formatted_uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

    namemc_url = f"https://namemc.com/profile/{uuid}"
    skin_render = f"https://mc-heads.net/body/{uuid}/right"

    embed = disnake.Embed(title=name, url=namemc_url, color=0x5865F2)
    embed.add_field(name="UUID", value=f"`{formatted_uuid}`", inline=False)
    embed.add_field(name="NameMC", value=f"[View Profile]({namemc_url})", inline=False)
    embed.set_image(url=skin_render)

    await ctx.send(embed=embed)

@bot.slash_command(
    name="ask",
    description="Ask the AI",
    install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
    contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True),
)
async def ask(ctx, *, question: str):
    await ctx.response.defer()

    try:
        response = await client.chat.complete_async(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        response_text = response.choices[0].message.content

        if len(response_text) > 2000:
            for i in range(0, len(response_text), 2000):
                await ctx.send(response_text[i:i+2000])
        else:
            await ctx.send(response_text)

    except Exception as e:
        await ctx.send(f"Unexpected error:\n```{e}```")

