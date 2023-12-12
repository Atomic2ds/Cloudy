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
from datetime import timedelta
import datetime
from embeds import embedutil


class utilities(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Utilities Cog      ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


    @app_commands.command(name="avatar", description="Get someones avatar up close")
    @app_commands.describe(user="Which users avatar to look at")
    async def avatar(self, interaction: discord.Interaction, user: Optional[discord.User]):
       await interaction.response.defer()
       if user == None:
          user = interaction.user
       pfp = user.avatar
       embed = discord.Embed(title=user.name.capitalize(), colour=0x4c7fff, description=f"[Avatar URL]({user.avatar})")
       embed.set_image(url=str(pfp))
       await interaction.followup.send(embed=embed)
    
          

    #Make a simple or custom poll
    @app_commands.command(name="poll", description="Make a poll instantly, simple or with custom choices")
    @app_commands.describe(question="What the poll is asking")
    async def poll_slash(self, interaction: discord.Interaction, question: str, option_a: Optional[str], option_b: Optional[str], option_c: Optional[str], option_d: Optional[str]):
     try:
      
      colour = 0x4c7fff
        
      #Option 1 Checks
      if not option_a == None:
           option_1 = str(option_a)
      else:
        option_1 = ""
            
      #Option 2 Checks
      if not option_b == None:
          option_2 = str(option_b)
      else:
          option_2 = ""
            
      #Option 3 Checks
      if not option_c == None:
          option_3 = str(option_c)
      else:
          option_3 = ""
            
      #Option 4 Checks
      if not option_d == None:
           option_4 = str(option_d)
      else:
          option_4 = ""
       
      actual_question = question
      if not option_1 == "" and not option_2 == "":
          description = "1️⃣ " + option_1 + "" + "\n2️⃣ " + option_2 + ""
          actual_description = description
      if not option_3 == "":
          actual_description = description + "\n3️⃣ " + option_3
      if not option_4 == "":
           actual_description = actual_description + "\n4️⃣ " + option_4
       #Testing if the poll is Simple or Custom
      try:
          embedVar = discord.Embed(title=actual_question, description=actual_description, colour=colour)
      except:
           embedVar = discord.Embed(title=actual_question, colour=colour)
           
      name = interaction.user.name.capitalize()
      embedVar.set_author(name=name, icon_url=str(interaction.user.avatar))
        
      #Checks that option 1 and 2 are in place
      if not option_1 == "" and option_2 == "":
          await interaction.response.send_message(embed=embedutil("denied","You require at least 2 options on a custom poll",interaction.user,interaction.guild), ephemeral=True)
      elif not option_2 == "" and option_1 == "":
          await interaction.response.send_message(embed=embedutil("denied","You require at least 2 options on a custom poll",interaction.user,interaction.guild), ephemeral=True)
      else:
          await interaction.response.defer()
          pollmsg = await interaction.followup.send(embed=embedVar)
        
     #Adding the Reactions
      if not option_1 == "":
        await pollmsg.add_reaction('1️⃣')
      if not option_2 == "":
        await pollmsg.add_reaction('2️⃣')
      if not option_3 == "":
         await pollmsg.add_reaction('3️⃣')
      if not option_4 == "":
         await pollmsg.add_reaction('4️⃣')
        
    #Simple Poll Reactions
      if option_1 == "" and option_2 == "" and option_3 == "" and option_4 == "":
        await pollmsg.add_reaction('👍')
        await pollmsg.add_reaction('👎')
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc())) 

    #Echo Command
    @app_commands.command(name="echo", description=f"Send a message as as the Donald Bot")
    @app_commands.describe(message="What message to send", channel="What channel to send the message to")
    async def echo(self, interaction: discord.Interaction, message: str, channel: Optional[discord.TextChannel]):
     await interaction.response.defer(ephemeral=True)
     try:
      if interaction.user.guild_permissions.manage_guild == True:
        try:
          channel = channel
          await channel.send(message)
        except:
          channel = interaction.channel
          await channel.send(message)
      await interaction.followup.send("Message Sent")
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #Slowmode App Command
    @app_commands.command(name="slowmode", description="Edit your current channels slowmode time or remove it")
    @app_commands.describe(seconds="How long the slowmode is")
    async def slowmode_slash(self, interaction: discord.Interaction, seconds: Optional[int], channel: Optional[discord.TextChannel]):
     await interaction.response.defer()
     try:
      if channel == None:
         channel = interaction.channel
      if interaction.user.guild_permissions.manage_channels == True:

    
        if not seconds == None:
            await channel.edit(slowmode_delay=seconds)
            await interaction.followup.send(embed=embedutil("success",f"Updated the slowmode for <#{channel.id}>"))
      
        
        else:
            await channel.edit(slowmode_delay=None)
            await interaction.followup.send(embed=embedutil("success",f"Removed slowmode for <#{channel.id}>"))
      
      else:
        await interaction.followup.send(embed=embedutil("denied","You require the manage channel permission to change slowmode"))
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    #Send a warning from the bot
    @app_commands.command(name="warning", description="Send a warning to chat")
    @app_commands.describe(msg="What message to associate with the warning")
    async def warningslash(self, interaction: discord.Interaction, msg: str):
        await interaction.response.defer()
        await interaction.followup.send(embed=embedutil("warning",msg))

    @app_commands.command(name="define",description="Get the definition of any word you want")
    @app_commands.describe(word="What word you want to define")
    async def define(self, interaction: discord.Interaction, word: str):
      try:
       await interaction.response.defer()
       response = await get_definition(word)
       await interaction.followup.send(embed=embedutil("definition",(word,response)))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))
       

     

async def setup(bot):
    await bot.add_cog(utilities(bot))

async def get_definition(term):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
      "X-RapidAPI-Key": "09efa8afd5msh469606e5298e21cp14d14ajsnfd148325b4b2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params={"term": term}) as response:
            data = await response.json()

    if len(data["list"]) > 0:
        definition = data["list"][0]["definition"]
        return definition
    else:
        return "Sorry, I couldn't find a definition for that term."
