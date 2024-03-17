from config import client, bot
import discord
import random
from embeds import embedutil
import traceback
import requests
import config
import aiohttp
import asyncio
import json
import libraries
from functions.core import hyperlink_button

async def handle_quote_save(msg: discord.Message, interaction: discord.Interaction):
 try:
  if not client.fun.quotes.find_one({"guild_id": interaction.guild.id}):
    await interaction.response.send_message(embed=embedutil("denied","The quotes module hasn't been configured yet!"),ephemeral=True)
    return
  embed = discord.Embed(colour=0x4c7fff, description=f'"{msg.content}"')
  embed.set_author(name=f"{msg.author.name.capitalize()}", icon_url=msg.author.avatar)
  embed.set_footer(text=f"Saved by {interaction.user.name.capitalize()}")

  document = client.fun.quotes.find_one({"guild_id": msg.guild.id,})
  channel_id = int(document["channel_id"])
  channel = bot.get_channel(channel_id)

  await channel.send(embed=embed,view=hyperlink_button(msg.jump_url,"Original"))
  await interaction.response.send_message(embed=embedutil("success","Successfully saved your requested quote"),ephemeral=True)
 except Exception:
  await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)
