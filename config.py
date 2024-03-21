import discord
from discord.ext import commands
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

# Importing views from core
from views.core import helpoverview, welcomeview, aboutview, notify_buttons



class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned_or(">"), intents=intents)
    async def setup_hook(self) -> None:
        from cogs.facts import factview
        from views.ows import compileview, storiesview
        from views.smp import smp_panel_view, smp_status_view
        self.add_view(helpoverview())
        self.add_view(factview(None))
        self.add_view(compileview())
        self.add_view(storiesview())
        self.add_view(welcomeview())
        self.add_view(aboutview())
        self.add_view(notify_buttons())
        self.add_view(smp_panel_view())
        from views.art import submission_buttons
        self.add_view(submission_buttons())

bot = BotClient()

try:
    TESTING = os.environ["TESTING"]
except:
    TESTING = "true"

if TESTING == "false":
    client = pymongo.MongoClient("mongodb://mongodb/")
else:
    client = pymongo.MongoClient(os.environ["TESTING_MONGO_INSTANCE"])

try:
    TOKEN = os.environ["TOKEN"]
except:
    TOKEN = None

#API Keys
GIPHY_KEY = os.environ["GIPHY_KEY"]
PEXELS_API =  os.environ["PEXELS_API"]
MEDIA_AUTH_KEY = os.environ["MEDIA_AUTH_KEY"]

# Testing Bot Tokens
TESTING1 = os.environ["TESTING1_TOKEN"]
TESTING2 = os.environ["TESTING2_TOKEN"]
