from config import client, bot
import discord
import random
from embeds import embedutil
import traceback
import config
import aiohttp
import asyncio
import json
import libraries

async def check_server_credentials(server_id, api_key, panel_url):
  headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/json'}
  async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{panel_url}/api/client/", headers=headers
        ) as response:
            if response.status == 200:
                return True
            else:
                raise Exception(f"Request to panel failed with status {response.status}")

async def grab_server_info(panel_url, server_id, api_key):
    headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{panel_url}/api/client/servers/{server_id}", headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Request to panel failed with status {response.status}")