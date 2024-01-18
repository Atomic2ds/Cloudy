import discord
from discord.ext import commands
from discord import app_commands, ui
import random
from discord.app_commands import Choice
import aiohttp
import requests
from typing import Optional
import traceback
import os
from discord import Webhook
import libraries
from datetime import timedelta
import datetime
from embeds import embedutil
from config import client
import pymongo

from functions.servers import check_server_credentials, grab_server_info
from views.servers import statusserversview, deleteserversview
db = client.servers


class servers(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Servers Cog        ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    server_cmd = app_commands.Group(name="server", description="An advanced server linking module for linking servers with pterodactyl")
    


    server_categories = [
        Choice(name="Minecraft", value="minecraft"),
        Choice(name="Modded Minecraft", value="moddedminecraft"),
        Choice(name="ARK: Survival Evolved", value="ark"),
        Choice(name="Counter Strike 2", value="cs2"),
        Choice(name="Unturned", value="unturned"),
        Choice(name="Terraria", value="terraria"),
        Choice(name="Stardew Valley", value="stardewvalley"),
        Choice(name="Astroneer", value="astroneer"),
        Choice(name="7 Days to Die", value="7daystodie"),
        Choice(name="Satisfactory", value="satisfactory"),
        Choice(name="Mindustry", value="mindustry"),
        Choice(name="Squad", value="squad"),
        Choice(name="The Forest", value="theforest"),
        Choice(name="Icarus", value="icarus"),
        Choice(name="Sons of the forest", value="sonsoftheforest"),
        Choice(name="Project Zomboid", value="projectzomboid"),
        Choice(name="Team Fortress 2", value="teamfortress2"),
        Choice(name="Arma 3", value="arma3"),
        Choice(name="Hytale", value="hytale"),
        Choice(name="Assetto Corsa", value="assettocorsa"),
        Choice(name="DayZ", value="dayz"),
        Choice(name="Space Engineers", value="spaceengineers"),
        Choice(name="Starbound", value="starbound"),
        Choice(name="Unturned", value="ark"),
        Choice(name="Other (Not Listed)", value="other"),
    ]

    @server_cmd.command(name="add",description="Link a new server using the server linking module")
    @app_commands.describe(category="What kind of game server is this, used for searching your servers if you have a lot of them",apikey="Get this from the pterodactyl panel account settings, Dashboard > Account > API Credentials",serverid="The id of the server on the panel, Dashboard > Your Server > Settings > Debug Information",panelurl="The url of your providers server dashboard, don't include the https:// part")
    @app_commands.choices(category=server_categories)
    async def add(self, interaction: discord.Interaction, category: str, apikey: str, serverid: str, panelurl: str):
      await interaction.response.defer(ephemeral=True)
      try:

        if db.list.find_one({"server_id":serverid, "guild_id": interaction.guild.id, "panel_url":panelurl}):
          await interaction.followup.send(embed=embedutil("denied","This server already exists on the system"),ephemeral=True)
          return
        
        await check_server_credentials(serverid, apikey, panelurl)
        server_count = db.list.count_documents({"guild_id": interaction.guild.id})
        server_count = int(server_count)
        new_server_count = server_count + 1
        if server_count == 25 or new_server_count > 25:
           await interaction.followup.send(embed=embedutil("denied","You have reached the limit on how many servers can be linked, when we release premium you will be able to add more hower it is currently a discord api limit that we need to make a workaround for"),ephemeral=True)
           return
        
        db.list.insert_one({"guild_id": interaction.guild.id, "api_key": apikey, "panel_url": panelurl, "server_id": serverid, "category": category})
        await interaction.followup.send(embed=embedutil("success","Successfully added your server to your linked servers!"))
        
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @server_cmd.command(name="status",description="View the stats of your linked servers, quickly and easily")
    @app_commands.describe(category="What kind of game server is this, used for searching your servers if you have a lot of them")
    @app_commands.choices(category=server_categories)
    async def status(self, interaction: discord.Interaction, category: Optional[str]):
       await interaction.response.defer()
       try:
         await interaction.followup.send(embed=embedutil("simple","Use the dropdown menu below to select servers currently linked via Cloudy, if you want to add a new server use /server add.\n\nThis module is in an early beta stage and this layout is not final"),view=statusserversview(interaction.guild.id,category))
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @server_cmd.command(name="delete",description="Open the server delete menu where you can select servers from the dropdown to delete them")
    async def delete(self, interaction: discord.Interaction):
       await interaction.response.defer()
       try:
         await interaction.followup.send(embed=embedutil("simple","You can select servers below to remove them from the linked servers list\n\nThis module is in an early beta stage and this layout is not final"),view=deleteserversview(interaction.guild.id))
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @server_cmd.command(name="panel",description="Send a server panel where members can easily")
    async def panel(self, interaction: discord.Interaction, channel: discord.TextChannel):
       pass


async def setup(bot):
    await bot.add_cog(servers(bot))
