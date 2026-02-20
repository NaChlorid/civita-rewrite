from flask import Flask, jsonify
from src.main import bot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return "<h1>This is Civita's API Server</h1><p>An A* Project</p>"

# JSON API route: total server count
@app.route('/v2/server_count')
def server_count():
    return jsonify({"server_count": len(bot.guilds)})

# JSON API route: info for a specific server by ID
@app.route('/v2/server/<int:guild_id>')
def server_info(guild_id):
    guild = bot.get_guild(guild_id)
    if not guild:
        return jsonify({"error": "Bot is not in that server"}), 404

    data = {
        "id": guild.id,
        "name": guild.name,
        "owner": str(guild.owner),
        "member_count": guild.member_count,
        "channels": len(guild.channels),
        "roles": len(guild.roles),
        "icon_url": str(guild.icon.url) if guild.icon else None
    }
    return jsonify(data)

# JSON API route: list all servers the bot is in
@app.route('/v2/servers')
def all_servers():
    return jsonify([
        {
            "id": guild.id,
            "name": guild.name,
            "owner": str(guild.owner),
            "member_count": guild.member_count
        }
        for guild in bot.guilds
    ])

# Start Flask in a separate thread to not block Disnake
def start_flask():
    app.run(port=7471)