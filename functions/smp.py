
import aiohttp

from config import client
db = client.smp
from embeds import embedutil
import libraries
import traceback
import discord
from views.core import infoview

# -- Fetching Server Resources -- 
async def fetch_server_resources(panel_url, server_id, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{panel_url}/api/client/servers/{server_id}/resources", headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Request to panel failed with status {response.status}")
            

# -- Fetching basic server info -- 
async def fetch_server_info(panel_url, server_id, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{panel_url}/api/client/servers/{server_id}", headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Request to panel failed with status {response.status}")
            

async def send_detailed_Stats(interaction, ephemeral):
    try:
        results = db.config.find_one({"guild_id": interaction.guild.id})
        if not results:
            await interaction.response.send_message(embed=embedutil("denied","There is currently no server linked to your discord community"),ephemeral=True)
            return

        await interaction.response.defer()
    
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

        await interaction.followup.send(embed=embed,ephemeral=ephemeral)

    except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

def bytes_to_mb(bytes):
    """Convert bytes to megabytes and round to 4 decimal places."""
    return round(bytes / (2**20), 2)

def bytes_to_gb(bytes):
    """Convert bytes to gigabytes and round to 4 decimal places."""
    return round(bytes / (2**30), 2)



async def send_smp_info(interaction, ephemeral):
    try:
        results = db.config.find_one({"guild_id": interaction.guild.id})
        if not results:
            await interaction.response.send_message(embed=embedutil("denied","There is currently no server linked to your discord community"),ephemeral=True)
            return

        await interaction.response.defer()
    
        api_key = results["api_key"]
        panel_url = results["panel_url"]
        server_id = results["server_id"]

        headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/json'}

        server_info = await fetch_server_info(panel_url, server_id, headers)
        server_resources = await fetch_server_resources(panel_url, server_id, headers)
        try:
            feature_limits = server_info['attributes']['feature_limits']
        except:
            feature_limits = server_info['attributes']['limits']

        name = server_info['attributes']['name']
        description = server_info['attributes']['description']

        stats = server_info
        memory_limit = stats['attributes']['limits']['memory']
        disk_limit = stats['attributes']['limits']['disk']
        io_limit = stats['attributes']['limits']['io']
        cpu_limit = stats['attributes']['limits']['cpu']
        threads_limit = stats['attributes']['limits']['threads']
        oom_disabled = stats['attributes']['limits']['oom_disabled']

        embed = discord.Embed(colour=0x4c7fff, title=name, description=description)

        embed.add_field(name="Memory Limit", value=f"{memory_limit} MB")
        embed.add_field(name="Disk Limit", value=f"{disk_limit} MB")
        embed.add_field(name="IO Limit", value=f"{io_limit}")
        embed.add_field(name="CPU Limit", value=f"{cpu_limit}%")
        embed.add_field(name="Threads Limit", value=f"{threads_limit}")
        if oom_disabled != True:
            oom_status = "Enabled"
        else:
            oom_status = "Disabled"
        embed.add_field(name="OOM Killer", value=str(oom_status))

        embed.add_field(name="Databases", value=f"{feature_limits['databases']}")
        embed.add_field(name="Allocations", value=f"{feature_limits['allocations']}")
        embed.add_field(name="Backups", value=f"{feature_limits['backups']}")


        embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)


        await interaction.followup.send(embed=embed,ephemeral=ephemeral)

    except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)