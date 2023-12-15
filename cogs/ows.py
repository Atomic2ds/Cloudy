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
from functions import publish_story, reset_ows, delete_story, read_story
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
    async def story_channel(self, interaction: discord.Interaction, option: discord.TextChannel):
        await interaction.response.defer()
        try:
         if interaction.user.guild_permissions.manage_guild:
          channel = option
          if db.ows.find_one({"guild_id": interaction.guild.id}):
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"channel_id": channel.id}})
          else:
            db.ows.insert_one({"guild_id": interaction.guild.id,"channel_id": channel.id,"words": [],"last_author": None})
          await channel.send(embed=embedutil("ows",("welcome",interaction.guild)))
          await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the one word story channel!"))
         else:
            await interaction.followup.send(embed=embedutil("denied","Your don't have permission to run this command"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @story_cmd.command(name="logs", description="Set your one word story log channel")
    @app_commands.describe(channel="Which channel you want to be the logs channel")
    async def owslogs(self, interaction: discord.Interaction, channel: discord.TextChannel):
       await interaction.response.defer()
       try:
          if interaction.user.guild_permissions.manage_guild:

            if not db.ows.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"))
              return

            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"log_id": channel.id}})
            await channel.send(embed=embedutil("ows",("logs set",interaction.guild)))
            await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the one word story logs channel!"))
          else:
            await interaction.followup.send(embed=embedutil("denied","You don't have permission to run this command"))
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @story_cmd.command(name="disable", description="Disable the one word story and delete the configuration")
    async def owslogs(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
       if interaction.user.guild_permissions.manage_guild:
         if not db.ows.find_one({"guild_id": interaction.guild.id}):
            await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"))
            return
         cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
         for document in cursor: 
              channel = self.bot.get_channel(document["channel_id"])
              await channel.send(embed=embedutil("ows",("disabled",interaction.guild)))
              db.ows.delete_many({"guild_id": interaction.guild.id})
              await interaction.followup.send(embed=embedutil("success",f"Successfully disabled the one word story module and cleared all data associated with it"))
       else:
          await interaction.followup.send(embed=embedutil("denied","You don't have permission to use this command"))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @story_cmd.command(name="compile",description="Turn your one word story into a beautiful paragraph you can read")
    async def compile_story(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
       cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
       for document in cursor:
          words = document["words"]
          story_words = []
          for item in words:
             story_words.append(item)
             story_words.append(" ")
          story_words = "".join(story_words)
          await interaction.followup.send(embed=embedutil("ows",("compile",story_words)),view=compileview())
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
    async def delete_story(self, interaction: discord.Interaction, name: str):
       await delete_story(interaction, name, db)

    @story_cmd.command(name="purge", description="Remove a certain amount of words from your story")
    async def purge(self, interaction: discord.Interaction, amount: int):
      if not interaction.user.guild_permissions.manage_guild:
         await interaction.response.send_message(embed=embedutil("bot",["error","You require the manage server permission"],interaction.user,interaction.guild), ephemeral=True)
         return

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
          await interaction.response.send_message(embed=embedutil("bot",["success",f"Successfully purged {str(amount)} message(s) from the story!"],interaction.user,interaction.guild))
      except Exception as e:
         await interaction.response.send_message(embed=embedutil("bot",["error",traceback.format_exc()],interaction.user,interaction.guild))

async def setup(bot):
    await bot.add_cog(ows(bot))
