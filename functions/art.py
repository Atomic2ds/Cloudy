
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
from views.core import infoview
import libraries

async def upload_art_image(image_url):
  url = image_url
  response = requests.get(url)

  if response.status_code == 200:
      with open("./images/cache/art.jpg", "wb") as f:
          f.write(response.content)

  files = {'file': open('./images/cache/art.jpg', 'rb')}
  headers = {'Authorization': f'Bearer {config.MEDIA_AUTH_KEY}'}
  response = requests.post(f"{libraries.MEDIA_URL}/upload", files=files, headers=headers)
  json_response = response.json()
  filename = json_response.get('filename')
  response_url = f"{libraries.MEDIA_URL}/uploads/{filename}"

  return response_url
