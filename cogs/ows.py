import discord
from discord.ext import commands
from discord import app_commands, ui
import random
from discord.app_commands import Choice
import aiohttp
import requests
from typing import Optional
import json
import traceback
import os
from discord import Webhook
import libraries
from datetime import timedelta
import datetime
from embeds import embedutil
from config import client
import pymongo
from functions.ows import publish_story, reset_ows, delete_story, read_story, requestedby, get_words_in_cache
from views.ows import compileview, storiesview

db = client.fun


class ows(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the OWS Cog            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    story_cmd = app_commands.Group(name="ows", description="Configure the one word story")



    @story_cmd.command(name="channel",description="Set the channel of the one word story module")
    @app_commands.describe(option="What channel you want the one word story to be in")
    async def story_channel(self, interaction: discord.Interaction, option: discord.TextChannel):
        await interaction.response.defer(ephemeral=True)
        try:
         if interaction.user.guild_permissions.manage_guild:
          channel = option
          if db.ows.find_one({"guild_id": interaction.guild.id}):
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"channel_id": channel.id}})
          else:
            db.ows.insert_one({"guild_id": interaction.guild.id,"channel_id": channel.id,"words": [],"last_author": None})
          await channel.send(embed=embedutil("ows",("welcome",interaction.guild)),view=requestedby(interaction.user))
          await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the one word story channel!"))
         else:
            await interaction.followup.send(embed=embedutil("denied","Your don't have permission to run this command"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))




    @story_cmd.command(name="logs", description="Set your one word story log channel")
    @app_commands.describe(channel="Which channel you want to be the logs channel")
    async def owslogs(self, interaction: discord.Interaction, channel: discord.TextChannel):
       await interaction.response.defer(ephemeral=True)
       try:
          if interaction.user.guild_permissions.manage_guild:

            if not db.ows.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"))
              return

            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"log_id": channel.id}})
            await channel.send(embed=embedutil("ows",("logs set",interaction.guild)),view=requestedby(interaction.user))
            await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the one word story logs channel!"))
          else:
            await interaction.followup.send(embed=embedutil("denied","You don't have permission to run this command"))
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))





    @story_cmd.command(name="disable", description="Disable the one word story and delete the configuration")
    async def owslogs(self, interaction: discord.Interaction):
      try:

        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return

        if not db.ows.find_one({"guild_id": interaction.guild.id}):
            await interaction.response.send_message(embed=embedutil("denied","The one word story is currently not configured yet!"),ephemeral=True)
            return
 
        await interaction.response.defer(ephemeral=True)

        cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
        for document in cursor: 
              channel = self.bot.get_channel(document["channel_id"])
              await channel.send(embed=embedutil("ows",("disabled",interaction.guild)),view=requestedby(interaction.user))
              db.ows.delete_many({"guild_id": interaction.guild.id})
              await interaction.followup.send(embed=embedutil("success",f"Successfully disabled the one word story module"))
         
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))





    @story_cmd.command(name="compile",description="Turn your one word story into a beautiful paragraph you can read")
    async def compile_story(self, interaction: discord.Interaction):
      try:
       if not db.ows.find_one({"guild_id": interaction.guild.id}):
            await interaction.response.send_message(embed=embedutil("denied","The one word story is currently not configured yet!"),ephemeral=True)
            return
       
       words = await get_words_in_cache(interaction)
       if len(words) < 1:
          await interaction.response.send_message(embed=embedutil("denied","Your story doesn't have any characters in it!"),ephemeral=True)
          return
       
       await interaction.response.defer()
       response = await get_words_in_cache(interaction)
       await interaction.followup.send(embed=embedutil("ows",("compile",response)),view=compileview())
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))



    @story_cmd.command(name="reset", description="Reset the current story saved in cache, doesn't disable the module")
    async def owsreset(self, interaction: discord.Interaction):
       await reset_ows(interaction, db)



    @story_cmd.command(name="publish", description="Publish your story to your servers story library")
    @app_commands.describe(name="The name of your story", info="Give your story a description")
    async def publish_ows(self, interaction: discord.Interaction, name: str, info: str):
       await publish_story(interaction, name, info, db, self.bot)



    @story_cmd.command(name="stories",description="View stories available in your server published by the community")
    async def liststories(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
       if not db.ows.find_one({"guild_id": interaction.guild.id}):
            await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"))
            return
      
       if not db.ows_stories.find_one({"guild_id": interaction.guild.id}):
         await interaction.followup.send(embed=embedutil("denied","Currently no stories available, published stories end up here"),ephemeral=True)
         return
       
       em = discord.Embed(colour=0x4c7fff, title=f"Stories in {interaction.guild.name}")
       guild_id = interaction.guild.id
       query = {"guild_id": guild_id}
       results = db.ows_stories.find(query)
       for result in results:
          em.add_field(name=result["name"], value=result["info"])
       await interaction.followup.send(embed=em,view=storiesview())
      except Exception as e:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)



    @story_cmd.command(name="read", description="Read a story from your servers story library")
    @app_commands.describe(name="The name of the story to read")
    async def readstory(self,interaction: discord.Interaction, name: str):
       await read_story(interaction, name, db)



    @story_cmd.command(name="delete",description="Delete a story from your server library")
    @app_commands.describe(name="The name of the story to delete")
    async def delete_story(self, interaction: discord.Interaction, name: str):
       await delete_story(interaction, name, db)



    @story_cmd.command(name="purge", description="Remove a certain amount of words from your story")
    @app_commands.describe(amount="How many words to purge from your one word story")
    async def purge(self, interaction: discord.Interaction, amount: int):
      if not interaction.user.guild_permissions.manage_guild:
         await interaction.response.send_message(embed=embedutil("denied","You don't have permission to use this command!"), ephemeral=True)
         return
      
      if amount > 100:
         await interaction.response.send_message(embed=embedutil("denied","You can only purge a max of 100 messages at a time!"), ephemeral=True)
         return
      
      if not db.ows.find_one({"guild_id": interaction.guild.id}):
         await interaction.response.send_message(embed=embedutil("denied","The one word story is currently not configured yet!"),ephemeral=True)
         return
      
      await interaction.response.defer(ephemeral=True)
      try:
       cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
       for document in cursor:
          words = document["words"]
          story_words = []
          for item in words:
             story_words.append(item)
          n = amount
          del story_words[-n:]
          collection = client.fun['ows']
          collection.update_one({"guild_id": interaction.guild.id}, {"$set": {"words": story_words}})
          channel = self.bot.get_channel(document["channel_id"])
          await channel.purge(limit=amount)
          await channel.send(embed=embedutil("ows",("purged",str(amount))),view=requestedby(interaction.user))
          await interaction.followup.send(embed=embedutil("success",f"Successfully purged {str(amount)} message(s) from the story!"))
      except Exception as e:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))



    @story_cmd.command(name="clearalldata", description="*DESTRUCTIVE* Clear all data on one word stories associated to your server off Cloudy")
    @app_commands.describe(type="What part of one word stories you want to clear data from")
    @app_commands.choices(type=[
      Choice(name="Story Configuration", value="config"),
      Choice(name="Story Library", value="library"),
    ])
    async def clearalldata(self, interaction: discord.Interaction, type: str):
     await interaction.response.defer(ephemeral=True)
     try:
      if not interaction.user.guild_permissions.manage_guild:
         await interaction.followup.send(embed=embedutil("denied","You don't have permission to use this command!"), ephemeral=True)
         return
      
      if type == "config":
       if not db.ows.find_one({"guild_id": interaction.guild.id}):
         await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"),ephemeral=True)
         return
       
       result = db.ows.delete_many({"guild_id":interaction.guild.id})
       await interaction.followup.send(embed=embedutil("success","Successfully cleared all of your configuration associated with your server off our systems"))
       
      if type == "library":
        if not db.ows_stories.find_one({"guild_id": interaction.guild.id}):
         await interaction.followup.send(embed=embedutil("denied","You currently have no stories in your story library!"),ephemeral=True)
         return
        
        result = db.ows_stories.delete_many({"guild_id":interaction.guild.id})
        await interaction.followup.send(embed=embedutil("success","Successfully cleared all stories associated with your server off our system"))

     except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

async def setup(bot):
    await bot.add_cog(ows(bot))
