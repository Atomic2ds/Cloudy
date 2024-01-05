
import aiohttp


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