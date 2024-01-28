import discord
from discord.ext import commands
from discord import app_commands, ui
import traceback
from discord.app_commands import Choice
import aiohttp
import requests
from typing import Optional
import os
from embeds import embedutil
from config import client

db = client.fun

class gcs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the GCs Cog            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    gc = app_commands.Group(name="gc", description="Enable or disable the group chat mode")

    @gc.command(name="enable",description="Enable the group chat mode, allowing members to change the server name and icon")
    async def enable(self, interaction: discord.Interaction):
      if interaction.permissions.manage_guild:
         try:
          if db.gcs.find_one({"guild_id": interaction.guild.id}):
            db.gcs.update_one({"guild_id": interaction.guild.id},{"$set": {"status": "enabled"}})
          else:
            db.gcs.insert_one({"guild_id": interaction.guild.id,"status": "enabled",})
          await interaction.response.send_message(embed=embedutil("success","Successfully enabled the group chat mode!"))
         except Exception:
            await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)
      else:
          await interaction.response.send_message(embed=embedutil("denied","You don't have permission to run this command!"),ephemeral=True)

    @gc.command(name="disable",description="Disable the group chat mode, allowing members to change the server name and icon")
    async def enable(self, interaction: discord.Interaction):
      if interaction.permissions.manage_guild:
         try:
          if db.gcs.find_one({"guild_id": interaction.guild.id}):
            db.gcs.update_one({"guild_id": interaction.guild.id},{"$set": {"status": "disabled"}})
          else:
            db.gcs.insert_one({"guild_id": interaction.guild.id,"status": "disabled",})
          await interaction.response.send_message(embed=embedutil("success","Successfully disabled the group chat mode!"))
         except Exception:
            await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)
      else:
          await interaction.response.send_message(embed=embedutil("denied","You don't have permission to run this command!"),ephemeral=True)

    @gc.command(name="name", description="Change the group chats (servers) name without admin")
    @app_commands.describe(name="What name to change the server to")
    async def name(self, interaction: discord.Interaction, name: str):
      try:
       gc_status = False
       
       cursor = db.gcs.find({"guild_id": interaction.guild.id,})
       for document in cursor:
          gc_status = document["status"]

       if not gc_status or gc_status == "disabled":
          await interaction.response.send_message(embed=embedutil("denied","Group chat mode is currently disabled, use /gc enable to activate it"),ephemeral=True)
          return
       
       if gc_status == "enabled":
          await interaction.guild.edit(name=name)
          await interaction.response.send_message(embed=embedutil("success","Successfully updated the servers name!"))

      except Exception:
         await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @gc.command(name="icon", description="Upload a custom icon to the Group Chat") 
    @app_commands.describe(image="Upload an image to set the server icon")
    async def icon(self,interaction: discord.Interaction, image: discord.Attachment):
     try:
       gc_status = False
       
       cursor = db.gcs.find({"guild_id": interaction.guild.id,})
       for document in cursor:
          gc_status = document["status"]

       if not gc_status or gc_status == "disabled":
          await interaction.response.send_message(embed=embedutil("denied","Group chat mode is currently disabled, use /gc enable to activate it"),ephemeral=True)
          return
       
       await interaction.response.defer(ephemeral=True)

       if gc_status == "enabled":
         if not image.content_type and "image" in image.content_type:
            await interaction.response.send_message(embed=embedutil("denied","That doesn't seem to be an image mate"),ephemeral=True)
            return
         icon_data = await image.read()
         await interaction.guild.edit(icon=icon_data)
         await interaction.followup.send(embed=embedutil("success","Successfully updated the group chat icon!"))

     except Exception:
        await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

async def setup(bot):
    await bot.add_cog(gcs(bot))