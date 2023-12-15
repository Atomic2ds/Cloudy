import discord
import traceback
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional
#from config import developers
import os
from discord.app_commands import Choice
import datetime
from embeds import embedutil
import json
import pymongo
import io
#from config import developers
import libraries
from config import client

db = client.utils

class autoroles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Autoroles Cog      ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    autoroles_cmd = app_commands.Group(name="autorole", description="Automatic role adding")

    @autoroles_cmd.command(name="add", description="Add a role to the list of autoroles")
    @app_commands.describe(type="What type of user you want the role to be added to", role="What role to add to the list")
    @app_commands.choices(type=[
      Choice(name="Human", value="human"),
      Choice(name="Bot", value="bot"),
    ])
    async def add(self, interaction: discord.Interaction, type: str, role: discord.Role):
     await interaction.response.defer()
     try:
      if interaction.user.guild_permissions.manage_guild == True:
        if type == "human":
                if client.utils.autoroles.find_one({"guild_id": interaction.guild.id}):
                  new_value = { "$push": { "human_roles": role.id } }
                  my_query = { "guild_id": interaction.guild.id }
                  client.utils.autoroles.update_one(my_query, new_value)
                  await interaction.followup.send(embed=embedutil("success","Successfully added role to the autoroles list"))
                else:
                   client.utils.autoroles.insert_one({"guild_id": interaction.guild.id,"human_roles": [role.id],"bot_roles":[]})
                   await interaction.followup.send(embed=embedutil("success","Successfully added role to the autoroles list"))
        elif type == "bot":
                if client.utils.autoroles.find_one({"guild_id": interaction.guild.id}):
                  new_value = { "$push": { "bot_roles": role.id } }
                  my_query = { "guild_id": interaction.guild.id }
                  client.utils.autoroles.update_one(my_query, new_value)
                  await interaction.response.followup.send(embed=embedutil("success","Successfully added role to the autoroles list"))
                else:
                   client.utils.autoroles.insert_one({"guild_id": interaction.guild.id,"bot_roles": [role.id],"human_roles":[]})
                   await interaction.followup.send(embed=embedutil("success","Successfully added role to the autoroles list"))
      else:
         await interaction.followup.send(embed=embedutil("bot",["denied","You're not allowed to do this!"],interaction.user,interaction.guild),ephemeral=True)

     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))
        

    @autoroles_cmd.command(name="remove", description="Remove an autorole from the autorole list")
    @app_commands.choices(type=[
      Choice(name="Human", value="human"),
      Choice(name="Bot", value="bot"),
    ])
    @app_commands.describe(type="What type of user you want the role to be removed from", role="What role to remove from the list")
    async def remove(self, interaction: discord.Interaction, type: str, role: discord.Role):
     await interaction.response.defer()
     try:
      if interaction.user.guild_permissions.manage_guild == True:
        if type == "human":
                new_value = { "$pull": { "human_roles": role.id } }
                my_query = { "guild_id": interaction.guild.id }
                client.utils.autoroles.update_one(my_query, new_value)
                await interaction.followup.send(embed=embedutil("success","Successfully removed role from the autoroles human list"))
        elif type == "bot":
                new_value = { "$pull": { "bot_roles": role.id } }
                my_query = { "guild_id": interaction.guild.id }
                client.utils.autoroles.update_one(my_query, new_value)
                await interaction.followup.send(embed=embedutil("success","Successfully removed role from the autoroles bot list"))
      else:
         await interaction.followup.send(embed=embedutil("denied","You don't have permission to run this command!"))

     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @autoroles_cmd.command(name="reset", description="Reset all autoroles")
    @app_commands.choices(type=[
      Choice(name="Human", value="human"),
      Choice(name="Bot", value="bot"),
    ])
    @app_commands.describe(type="Which list to reset")
    async def remove(self, interaction: discord.Interaction, type: str):
     await interaction.response.defer()
     try:
      if interaction.user.guild_permissions.manage_guild == True:
        if type == "human":
             client.utils.autoroles.update_one({"guild_id": interaction.guild.id},{"$set": {"human_roles": []}})
             await interaction.followup.send(embed=embedutil("success","Successfully reset the human list"))
        elif type == "bot":
            client.utils.autoroles.update_one({"guild_id": interaction.guild.id},{"$set": {"bot_roles": []}})
            await interaction.followup.send(embed=embedutil("success","Successfully reset the bot list"))
      else:
         await interaction.followup.send(embed=embedutil("denied","You don't have permission to run this command!"))
     except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @autoroles_cmd.command(name="list", description="List all the autoroles")
    async def remove(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
        if not client.utils.autoroles.find_one({"guild_id": interaction.guild.id}):
          await interaction.followup.send(embed=embedutil("denied","Autoroles have not been setup yet!"))
          return
        
        cursor = client.utils.autoroles.find({"guild_id": interaction.guild.id,})
        for document in cursor:
          roles = document["bot_roles"]
          bot_roles = []
          for item in roles:
             item = f"<@&{str(item)}>"
             bot_roles.append(item)
             bot_roles.append(" ")
          bot_roles = "".join(bot_roles)

          roles = document["human_roles"]
          human_roles = []
          for item in roles:
             item = f"<@&{str(item)}>"
             human_roles.append(item)
             human_roles.append(" ")
          human_roles = "".join(human_roles)

        embed = discord.Embed(color=0x4c7fff, title=f"Autoroles in {interaction.guild.name}")  
        embed.add_field(name="Bot Roles", value=bot_roles, inline=False)
        embed.add_field(name="Human Roles", value=human_roles, inline=False)
        embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        await interaction.followup.send(embed=embed)
                  
      except Exception as e:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))
    
async def setup(bot):
    await bot.add_cog(autoroles(bot))