# run.py
import shit_env
from main import bot
from api.app import start_flask
import threading

#
# Get our .env thingies using SHIT-ENV
#
env = shit_env.Env(".env")
TOKEN = env.Get("TOKEN")

# Run Flask in a separate thread
flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Run the Discord bot in the main thread
bot.run(TOKEN)
