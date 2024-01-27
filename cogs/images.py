import discord
from discord.ext import commands
#from utils import embedutil
from discord import app_commands
import json
from embeds import embedutil
import traceback
import pymongo
import requests
import random
from config import client
from functions.images import img2text

db = client.images

class images(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Images Cog         ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    image_cmd = app_commands.Group(name="image", description="Manage an image channel on your discord server")

    @image_cmd.command(name="channel", description="Choose where the channel for movie submissions will be")
    async def movie_channel(self, interaction: discord.Interaction, option: discord.TextChannel):
       await interaction.response.defer()
       if interaction.user.guild_permissions.manage_guild:
         try:
          
          if db.config.find_one({"guild_id": interaction.guild.id}):
            db.config.update_one({"guild_id": interaction.guild.id},{"$set": {"channel_id": option.id}})
          else:
            db.config.insert_one({"guild_id": interaction.guild.id,"channel_id": option.id,"status": "enabled",})
          await option.send(embed=embedutil("simple","This channel has been configured as the text to image channel"))
          await interaction.followup.send(embed=embedutil("success",f"Successfully set {option.mention} as the text to image channel!"))
         except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))
       else:
          await interaction.followup.send(embed=embedutil("denied","You need the manage guild permission to run this command"))

    
    @image_cmd.command(name="disable",description="Disable the text to image channel")
    async def disable(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
         try:
          if not db.config.find_one({"guild_id": interaction.guild.id}):
            await interaction.followup.send(embed=embedutil("denied","The text to image channel is currently not configured yet!"))
            return

          if db.config.find_one({"guild_id": interaction.guild.id}):
            db.config.update_one({"guild_id": interaction.guild.id},{"$set": {"status": "disabled"}})
          else:
            db.config.insert_one({"guild_id": interaction.guild.id,"status": "disabled",})
          
          await interaction.followup.send(embed=embedutil("success","Successfully disabled the image to text channel"))
         except Exception:
            await interaction.followup.send(embed=embedutil("denied","You need the manage guild permission to run this command"))
      except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @image_cmd.command(name="enable",description="Enable the text to image channel")
    async def disable(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
        if not db.config.find_one({"guild_id": interaction.guild.id}):
          await interaction.followup.send(embed=embedutil("denied","The text to image channel is currently not configured yet!"))
          return
        
        if interaction.permissions.manage_guild:
          if db.config.find_one({"guild_id": interaction.guild.id}):
            db.config.update_one({"guild_id": interaction.guild.id},{"$set": {"status": "enabled"}})
          else:
            db.config.insert_one({"guild_id": interaction.guild.id,"status": "enabled",})
          await interaction.followup.send(embed=embedutil("success","Successfully enabled the image to text channel"))
        else:
            await interaction.followup.send(embed=embedutil("denied","You need the manage guild permission to run this command"))
      except Exception:
        await interaction.followup.send(embed=embedutil("erorr",traceback.format_exc()))

    @image_cmd.command(name="fetch", description="Fetch a image from our image to text")
    async def fetch(self, interaction: discord.Interaction, query: str):   
     await interaction.response.defer()
     embed = await img2text(query)
     await interaction.followup.send(embed=embed)
     
async def setup(bot):
    await bot.add_cog(images(bot))
