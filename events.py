import discord
from functions import save, send_vk, isImage
from settings import token, group_id, album_id, ok_photos, client
from time import strftime


@client.event
async def on_ready():
	print("Hi!")
	print("bot is ready")


@client.event
async def on_message(message):
	user = "<@" + str(message.author.id) + ">"
	embed = discord.Embed(
		title="Sent to VK!",
		description="Поздравляем, " + user,
		colour=discord.Colour.blue()
		)
	if message.channel.name == "success":
		if message.attachments:
			data = message.attachments[0].url
			if isImage(data) in ok_photos:
				save(data)
				send_vk(message.author.name, token, group_id, album_id)
				await message.channel.send(embed=embed)
