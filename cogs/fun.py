import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional
import os
from discord.app_commands import Choice
import datetime
import json
import traceback
import io
import requests
import config
import aiohttp
from embeds import embedutil
from functions.fun import fetch_gif
from functions.core import infoview

from PIL import Image
from io import BytesIO

class fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Fun Cog            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    @app_commands.command(name="8ball",description="Ask the magic 8 ball a question")
    @app_commands.describe(question="What question to ask the magic 8 ball")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
      await interaction.response.defer()
      try:
       await interaction.followup.send(embed=embedutil("8ball",question))
      except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @app_commands.command(name="gif", description="Get a random gif or enter a query")
    @app_commands.describe(query="Send a custom query to the Gif API")
    async def gif_slash(self, interaction: discord.Interaction, query: Optional[str]):
      await interaction.response.defer()
      embed = await fetch_gif(query)
      await interaction.followup.send(embed=embed)

    @app_commands.command(name="curry", description="Fetch a beautiful curry picture")
    async def gif_slash(self, interaction: discord.Interaction):
      await interaction.response.defer()
      embed = await fetch_gif("Indian Curry")
      await interaction.followup.send(embed=embed)

    @app_commands.command(name="meme", description="Get a Random Meme from Reddit")
    @app_commands.describe(subreddit="Which subreddit to grab the meme from")
    @app_commands.choices(subreddit=[
      Choice(name="r/dankmemes", value="dankmemes"),
      Choice(name="r/memes", value="memes"),
      Choice(name="r/surrealmemes", value="surrealmemes"),
      Choice(name="r/funny", value="funny"),
      Choice(name="r/terriblefacebookmemes", value="terriblefacebookmemes"), 
      Choice(name="r/wholesomememes", value="wholesomememes"), 
    ])
    async def meme_slash(self, interaction: discord.Interaction, subreddit: Optional[str]):
      await interaction.response.defer()
      try:
        if subreddit == None:
          subreddits = ("dankmemes","memes","surrealmemes","funny","memeeconomy","wholesomememes","terriblefacebookmemes")
          subreddit = random.choice(subreddits)
        async with aiohttp.ClientSession() as cs:
          async with cs.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot') as r:
             res = await r.json()
             await interaction.followup.send(embed=embedutil("meme",(res['data']['children'] [random.randint(0, 25)]['data']['url'],subreddit)))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @app_commands.command(name="template", description="Put a users face on one of our Templates!")
    @app_commands.describe(type="Which Template to use for the image", user="What users face you want to put on the Template")
    @app_commands.choices(type=[
      Choice(name="Nerd Template", value="nerd"),
      Choice(name="Wanted Template", value="wanted"),
      Choice(name="NPC Template", value="npc"),
    ])
    async def template(self, interaction: discord.Interaction, type: str, user: discord.User):
      try:
        await interaction.response.defer()
        if user is None:
            user = interaction.user

        if type == "nerd":
            wanted = Image.open("./images/templates/nerd-template.jpg")
            data = BytesIO(await user.display_avatar.read())
            pfp = Image.open(data)
            pfp = pfp.resize((100, 100))
            wanted.paste(pfp, (80, 5))
            result_path = "./images/results/nerd-result.jpg"
            wanted.save(result_path)

        elif type == "wanted":
            wanted = Image.open("./images/templates/wanted-template.jpg")
            data = BytesIO(await user.display_avatar.read())
            pfp = Image.open(data)
            pfp = pfp.resize((275, 275))
            wanted.paste(pfp, (85, 160))
            result_path = "./images/results/wanted-result.jpg"
            wanted.save(result_path)

        elif type == "npc":
            npc = Image.open("./images/templates/npc-template.jpg")
            data = BytesIO(await user.display_avatar.read())
            pfp = Image.open(data)
            pfp = pfp.resize((125, 125))
            npc.paste(pfp, (60, 40))
            result_path = "./images/results/npc-result.jpg"
            npc.save(result_path)

        # Upload the file to Discord
        file = discord.File(result_path)
        #channel = self.bot.get_channel(1183413750557065287)

        # Get the URL of the uploaded file
        #file_url = message.attachments[0].url

        # Now you can use file_url in your embed
        #embed = discord.Embed(title="Image Template", color=0x4c7fff)
        #embed.set_image(url=file_url)
        #embed.set_footer(text=f"Template: {type.capitalize()}")
        await interaction.followup.send(file=file,view=infoview(f"User: {user.name.capitalize()}"))

      except Exception:
        await interaction.followup.send(embed=embedutil("error", traceback.format_exc()))


async def setup(bot):
    await bot.add_cog(fun(bot))
