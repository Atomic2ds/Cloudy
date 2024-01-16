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
from functions.smp import fetch_server_info, fetch_server_resources

db = client.servers

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
            
async def send_server_status(server_id):
    try:
        results = db.list.find_one({"server_id": server_id})

        api_key = results["api_key"]
        panel_url = results["panel_url"]
        server_id = results["server_id"]

        headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/json'}

        server_info = await fetch_server_info(panel_url, server_id, headers)
        server_resources = await fetch_server_resources(panel_url, server_id, headers)

        state = server_resources['attributes']['current_state']
        is_suspended = server_resources['attributes']['is_suspended']
        name = server_info['attributes']['name']
        description = server_info['attributes']['description']

        stats = server_resources
        memory_bytes = stats['attributes']['resources']['memory_bytes']
        cpu_absolute = stats['attributes']['resources']['cpu_absolute']
        disk_bytes = stats['attributes']['resources']['disk_bytes']
        network_tx_bytes = stats['attributes']['resources']['network_tx_bytes']
        network_rx_bytes = stats['attributes']['resources']['network_rx_bytes']
        uptime = stats['attributes']['resources']['uptime']

        if is_suspended == True:
            is_suspended = "is suspended"
        else:
            is_suspended = "is not suspended"

        embed = discord.Embed(colour=0x4c7fff, title=name, description=description)

        embed.add_field(name="State", value=state.capitalize())
        embed.add_field(name="Memory Usage", value=f"{bytes_to_gb(memory_bytes)}GiB")
        embed.add_field(name="CPU Usage", value=f"{str(cpu_absolute)}%")
        embed.add_field(name="Disk Usage", value=f"{bytes_to_gb(disk_bytes)}GiB")
        embed.add_field(name="Network RX", value=f"{bytes_to_mb(network_rx_bytes)}MiB")
        embed.add_field(name="Network TX", value=f"{bytes_to_mb(network_tx_bytes)}MiB")


        embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

        return embed

    except Exception:
        embed = embedutil("error",traceback.format_exc())
        return embed

def bytes_to_mb(bytes):
    """Convert bytes to megabytes and round to 4 decimal places."""
    return round(bytes / (2**20), 2)

def bytes_to_gb(bytes):
    """Convert bytes to gigabytes and round to 4 decimal places."""
    return round(bytes / (2**30), 2)