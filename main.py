from rich.console import Console
from rich.rule import Rule
from time import perf_counter
import signal
import discord
import requests
import os
import asyncio
import random
import re
import shlex
import logging
import aioconsole
import traceback
from config import bot
import config
from functions import process_ows, handle_autoroles, process_img2text
import aioschedule

console = Console()

#Scheduling
from schedules import daily_task
aioschedule.every().day.at("12:00").do(daily_task)

# Sets up logging and initializes it.
logger = logging.getLogger('ErrorLogging')
logger.setLevel(logging.INFO)

# Create a console handler and set its level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a Formatter object and set it on the handler
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s\n%(exc_info)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
logger.addHandler


#Login Messages
@bot.event
async def on_ready():

  print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
  print(f"┃  Connected to Discord API          ┃")
  print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
  print(f"\nLogged in as {bot.user}")
  print("\nLoading Bot Cogs..\n")
  
  #Syncing the Slash Command Tree
  try:
    synced = await bot.tree.sync()
    print(f"\n{len(synced)} slash commands Synced\n")
  except Exception as e:
    logger.error(traceback.format_exc())


  #Updating the bots presence
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))

  while True:
    await aioschedule.run_pending()
    await asyncio.sleep(5)

@bot.event
async def on_message(msg):
  await process_ows(msg)
  await process_img2text(msg)

@bot.event
async def on_member_join(member):
  await handle_autoroles(member)

#Loading the bot
async def main():
  try:
    testing = os.environ["TESTING"]
  except:
    testing = "true"
    
  if testing == "true":
    #Asking the user which bot they want to boot off
    botchoice = input("Choose a bot to boot on (1-2): ")
    bots = ["1","2"]
    if not botchoice in bots:
      print("Invalid Bot Choice, Deploying on Bot 1")
      botchoice = "1"

    #Asking the user what cogs to load
    cogschoices = input("List cogs you want to load: ")
    if cogschoices == "all" or cogschoices == "":
      await load()
    else:
      cogschoices = shlex.split(cogschoices)
      for item in cogschoices:
        try:
          await bot.load_extension(f'cogs.{item}')
        except Exception:
          logger.error(traceback.format_exc())

    if botchoice == "1":
      await bot.start(config.TESTING1)
    elif botchoice == "2":
      await bot.start(config.TESTING2)

  else:
    #dashboard()
    await load()
    if config.TOKEN == None:
      print("Unable to boot the bot, no token env was set")
    else:
      await bot.start(config.TOKEN)
      

#Loading Bot Cogs on Production Server
async def load():
  for file in os.listdir('./cogs'):
    if file.endswith('.py'):
      await bot.load_extension(f'cogs.{file[:-3]}')
    

global loading_start_time; loading_start_time = perf_counter()
# Initialize Bot
asyncio.run(main())
