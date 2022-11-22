import discord
from discord.ext import commands

class Admin_tools(commands.Cog):

	def __init__(self, client):
		self.client = client


	#Admin Commands

	#Kick command with error handler
	@commands.command(hidden = True)
	@commands.has_any_role("Server Owner(s)", "Modz")
	async def kick(self, ctx, member : discord.Member, *, reason = "apparently no given reason"):

		await ctx.message.delete()
		emoji = "<a:wow:1008145225186811975>"
		channel = self.client.get_channel(997395580026355843)
		await channel.send(f' {member.mention} has been kicked for {reason}. Don\'t do that again buddy{emoji}')
		await member.kick(reason = reason)

	#Ban command with error handler
	@commands.command(hidden = True)
	@commands.has_any_role("Server Owner(s)", "Modz")
	async def ban(self, ctx, member : discord.Member, *, reason = "apparently no given reason"):

		await ctx.message.delete()
		ban_hammer = "<a:ban:997022875473158154>"
		channel = self.client.get_channel(997395580026355843)
		await channel.send(f'{member.mention} has been banned for {reason}. Ciao buddy {ban_hammer}.')
		await member.ban(reason = reason)

	#Unban command with error handler
	@commands.command(hidden = True)
	@commands.has_any_role("Server Owner(s)", "Modz")
	async def unban(self, ctx, *, member):

		channel = self.client.get_channel(997395580026355843)
		await ctx.message.delete()
		banned_users = await ctx.guild.bans()
		member_name, member_discrimintor = member.split('#')

		for banned_entry in banned_users:
			user = banned_entry.user

			if (user.name, user.discriminator) == (member_name, member_discrimintor):
				await ctx.guild.unban(user)
				await channel.send(f'Welcome back {user.mention}. You have been resurrected. Cheers.')


	#Error handlers
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.UserInputError):
			embed = discord.Embed(
				title = "Ban Command Usage",
				description = "Please use this command properly as follows:\nban @[specified user] [reason(optional)]",
				colour = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			)
			embed.set_thumbnail(url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")
			embed.set_author(name = "Darth Vader", icon_url = "https://cdn.discordapp.com/avatars/995921314512638022/60275f59e5a1794d7d020e4c00e4051c.webp?size=1024")
			await ctx.send(embed = embed)

def setup(client):
	client.add_cog(Admin_tools(client))
