# run.py
from src.main import bot
from api.app import start_flask
import threading
from config import TOKEN

#
# Get our .env thingies using SHIT-ENV
#

# Run Flask in a separate thread
flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Run the Discord bot in the main thread
bot.run(TOKEN)

