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
from functions.fun import fetch_gif, get_pexels_image
from functions.core import infoview
import libraries

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

    @app_commands.command(name="monkey",description="Grab a monkey picture")
    async def monkey(self, interaction: discord.Interaction, name: str):
      if random.randint(1, 1000) == 1:
         query = "gorilla"
      else:
         query = f"monkey named {name}"
      await interaction.response.defer()
      api_key = "LUou1G0GPKICgLpylPXedl2akKv08RNHwS435x9TB2NDBnkvh8CYwgjk"
      image_url = await get_pexels_image(api_key, query)
      if image_url is not None:
        embed = discord.Embed(colour=0x4A4A4A,description=f"The monke below is named {name}")
        embed.set_image(url=image_url)
        await interaction.followup.send(embed=embed)
      else:
        await interaction.followup.send(embed=embedutil("denied","No image found."))


    @app_commands.command(name="gif", description="Get a random gif or enter a query")
    @app_commands.describe(query="Send a custom query to the Gif API")
    async def gif_slash(self, interaction: discord.Interaction, query: Optional[str]):
      await interaction.response.defer()
      embed = await fetch_gif(query)
      await interaction.followup.send(embed=embed)

    @app_commands.command(name="legacygif", description="Get a random gif from our old gif library")
    async def legacygif(self, interaction: discord.Interaction):
      await interaction.response.defer()
      await interaction.followup.send(random.choice(libraries.gifs))

    @app_commands.command(name="meme", description="Get a Random Meme from Reddit")
    @app_commands.describe(subreddit="Which subreddit to grab the meme from")
    @app_commands.choices(subreddit=[
      Choice(name="r/dankmemes", value="dankmemes"),
      Choice(name="r/memes", value="memes"),
      Choice(name="r/surrealmemes", value="surrealmemes"),
      Choice(name="r/terriblefacebookmemes", value="terriblefacebookmemes"), 
      Choice(name="r/wholesomememes", value="wholesomememes"), 
    ])
    async def meme_slash(self, interaction: discord.Interaction, subreddit: Optional[str]):
      await interaction.response.defer()
      try:
        if subreddit == None:
          subreddits = ("dankmemes","memes","surrealmemes","wholesomememes","terriblefacebookmemes")
          subreddit = random.choice(subreddits)
        async with aiohttp.ClientSession() as cs:
          async with cs.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot') as r:
             res = await r.json()
             await interaction.followup.send(embed=embedutil("meme",(res['data']['children'] [random.randint(0, 25)]['data']['url'],subreddit)))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @app_commands.command(name="template", description="Put a users face on one of our Templates!")
    @app_commands.describe(type="Which Template to use for the image", user="What users face you want to put on the Template")
    @app_commands.choices(type=[
      Choice(name="Nerd Template", value="nerd"),
      Choice(name="Wanted Template", value="wanted"),
      Choice(name="NPC Template", value="npc"),
    ])
    async def template(self, interaction: discord.Interaction, type: str, user: Optional[discord.User]):
      await interaction.response.defer()
      try:
        if user is None:
            user = random.choice(interaction.guild.members)

        data = BytesIO(await user.display_avatar.read())
        template = Image.open(f"./images/templates/{type}-template.jpg")
        pfp = Image.open(data)
 
        if type == "nerd":
           pfp = pfp.resize((100, 100))
           template.paste(pfp, (80, 5))
        elif type == "wanted":
           pfp = pfp.resize((275, 275))
           template.paste(pfp, (85, 160))
        elif type =="npc":
           pfp = pfp.resize((125, 125))
           template.paste(pfp, (60, 40))
        
        result_path = f"./images/results/{type}-result.jpg"
        template.save(result_path)

        file = discord.File(result_path)
        await interaction.followup.send(file=file,view=infoview(f"User: {user.name.capitalize()}"))

      except Exception:
        await interaction.followup.send(embed=embedutil("error", traceback.format_exc()))


async def setup(bot):
    await bot.add_cog(fun(bot))
