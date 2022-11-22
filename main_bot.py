import discord
import admin_data
import os
import sys
sys.path.append("./Helper_Programs")
import random
import embed_help

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '$', intents = intents)

@client.event
async def on_ready():

	print("Bot is good to go!")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_member_join(member: discord.Member):

	channel = client.get_channel(997395580026355843)

	role = discord.utils.get(member.guild.roles, name = "The Familgia")

	await member.add_roles(role)

	await channel.send(f'Welcome to the **LFNM Server** {member.mention}. *Enjoy and stay a while!*')

	await member.send(embed = embed_help.payhelp())
	await member.send(file = discord.File(fp = "./logs/acc_ser_abb.txt", filename = "Account/Service Abbreviations.txt"))


@client.command(hidden = True)

async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command(hidden = True)

async def avatar(ctx, member: discord.Member):
	if not member:
		member = ctx.author

	userAv = member.avatar_url
	print(userAv)

@client.command(hidden = True)

async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')




client.run(admin_data.TOKEN)
