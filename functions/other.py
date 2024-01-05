import discord

async def get_avatar(user):
  pfp = user.avatar
  embed = discord.Embed(title="Avatar Viewer", colour=0x4c7fff)
  embed.set_image(url=str(pfp))
  return embed