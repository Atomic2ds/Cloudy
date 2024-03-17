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
    client = pymongo.MongoClient("mongodb://vyD4TmsB7tWvwoogAkzDbWY:PJsFqnt3QPJFBqMJFUVkswjaGMZUAeu6x2wGq72qLLZTXfHgzQbQFJ8To3t8@mongodb/")
else:
    client = pymongo.MongoClient("mongodb://yyX7BeyVoUguQAX69gP6UxrHkXKKtAEdV:ZZFA97mvqYU5s5WhANnPaaPw7LrotjWP8@140.238.206.46:25623/")

try:
    TOKEN = os.environ["TOKEN"]
except:
    TOKEN = None

#API Keys
IMGUR_API = "46beb6aef663a4f"
GIPHY_KEY = "IXND99OPhaatCVy98tmefJkydzIkGG7x"
PEXELS_API = "LUou1G0GPKICgLpylPXedl2akKv08RNHwS435x9TB2NDBnkvh8CYwgjk"
MEDIA_AUTH_KEY = "oK2MAwQJujz3CGCBZWZ4UrYRT5bVjV"

# Testing Bot Tokens
TESTING1 = "MTA5NTI5MDkyMDM1MTU3MjA0OQ.GPyKoT.l2zECS4m1yEXroSvB0W6uVx2B3gQ_JnNoplYkY"
TESTING2 = "MTA5NjM1MzE2NDM4NDU1MDk2Mg.G-tdcF.DS9Y3umu78EFifKykQHpXwbXyFSifa0Tm2pVIM"
