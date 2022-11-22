import discord
from discord.ext import commands
import sys
sys.path.append("..")
sys.path.append("./Helper_Programs")
sys.path.append("./database_queue")
import admin_data
from queue_sys import Queue
import embed_help
import pickle
import random
import databaseFunc
import logs_func
from datetime import datetime

class Payment_tools(commands.Cog):

	def __init__(self, client):
		self.client = client


	def cog_check(self, ctx):

		return isinstance(ctx.channel, discord.DMChannel)


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):

		if isinstance(error, commands.CommandNotFound):
			await ctx.send("No such command exists. Please use the $payhelp command to see the appropriate commands accepted and $help [specific command] to see what the command needs to run accordingly. Thanks!")


	@commands.command(name = "paynow", aliases = ["Paynow", "PayNow"])
	async def pay_now(self, ctx, account: str):

		found = False

		i = 0

		while (i < len(admin_data.list_links) and found == False):

			for key in admin_data.list_links[i]:

				if key == account:

					keep_data = admin_data.list_links[i][key]
					found = True
					break

			i += 1


		if found:


			embed = discord.Embed(
				title = "**The Account/Service You Wish To Purchase is: {} for ${} CAD**".format(keep_data[1], keep_data[2]),
				colour = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))

			)

			embed.set_thumbnail(url = "https://cdn.discordapp.com/banners/708882229094383677/a_421cd9d29071da4fb24d910502e9a2e1.png?size=600")
			embed.set_author(name = "Darth Vader", icon_url = "https://cdn.discordapp.com/avatars/995921314512638022/60275f59e5a1794d7d020e4c00e4051c.webp?size=1024")
			embed.add_field(name = "To complete your purchase, **CLICK** the following **LINK BELOW** which will redirect you to PayPal:", value = "\u200b", inline = False)
			embed.add_field(name = f'**{keep_data[0]}**', value = "\u200b")
			embed.set_footer(text = "Sincerly, the lfnm team", icon_url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")

			await ctx.send(embed = embed)

			await ctx.message.add_reaction("<a:mavisiren1:997022856284225586>")



		else:

			raise commands.UserInputError

		logs_func.write_to_payment_log(ctx.author, ctx.command.name)

	@commands.command(name = "paid")
	# @commands.cooldown(1, 60, commands.BucketType.user)
	async def paid(self, ctx, order_id : str, first_name: str, last_name: str, account: str, email_psn = None, pass_psn = None, *, backup_code = None):


		channel = self.client.get_channel(994442251092627467)
		completion_mess = True
		current_time = datetime.now()
		date_time_string = current_time.strftime("%d/%m/%Y at %H:%M:%S")

		if account in admin_data.list_links[0]:

			acc_queue = databaseFunc.add_to_queue_at_db(1, [str(ctx.author), f'Time Bought: {date_time_string}', f'Order id: {order_id}', f'First Name: {first_name}', f'Last Name: {last_name}', f'Service Bought: {account}', f'PSN Email: {email_psn}', f'PSN Password: {pass_psn}', f'2FA Code: {backup_code}'])


			await channel.send("{} just bought a Base Account!\nThe Updated Account Queue is {}".format(ctx.author.mention, acc_queue))


		elif account in admin_data.list_links[1]:

			div_queue = databaseFunc.add_to_queue_at_db(2, [str(ctx.author), f'Time Bought: {date_time_string}', f'Order id: {order_id}', f'First Name: {first_name}', f'Last Name: {last_name}', f'Service Bought: {account}', f'PSN Email: {email_psn}', f'PSN Password: {pass_psn}', f'2FA Code: {backup_code}'])
			await channel.send("{} just bought Liquid Divinium!\nThe Updated Liquid Divinium Queue is {}".format(ctx.author.mention, div_queue))

		elif account in admin_data.list_links[2]:

			acc_div_queue = databaseFunc.add_to_queue_at_db(3, [str(ctx.author), f'Time Bought: {date_time_string}', f'Order id: {order_id}', f'First Name: {first_name}', f'Last Name: {last_name}', f'Service Bought: {account}', f'PSN Email: {email_psn}', f'PSN Password: {pass_psn}', f'2FA Code: {backup_code}'])
			await channel.send("{} just bought an Account with Liquid Divinium!\nThe Updated Accounts with Liquid Divinium Queue is {}".format(ctx.author.mention, acc_div_queue))


		else:
			raise commands.UserInputError

		await ctx.send(f'**Congratulations {ctx.author.mention}**, your order has been successfully received by our team and is awaiting completion within our said **24 hour time frame**.\nWith this, Darth Vader will send you another message containing your account details and/or completion message of the specified service. Cheers and be in touch soon!')
		await ctx.message.add_reaction(u"\u2705")

		logs_func.write_to_payment_log(ctx.author, ctx.command.name)


	#Help pay command for buyers in Darth Vader Direct Messages
	@commands.command(name = "payhelp")
	async def pay_help(self, ctx):

		await ctx.send(embed = embed_help.payhelp())
		await ctx.send(file = discord.File(fp = "./logs/acc_ser_abb.txt", filename = "Account/Service Abbreviations.txt"))


	#Improper use of payment commands
	@pay_now.error
	async def pay_now_error(self, ctx, error):

		if isinstance(error, commands.UserInputError):

			paynow_usage_message = str("""```diff\n- $paynow [Account/Service Abbreviation]```""")
			emoji = "<a:jj:997043065095192603>"

			embed = discord.Embed(
				title = "**Improper usage of ${} command**".format(ctx.command),
				description = "**Please use this command properly as follows:**\n\n**{}** \n{}(**Abbreviations** can be **FOUND** using the **$payhelp** command or by visiting our **payment channel** in the **lfnm_modz server**.)".format(paynow_usage_message, emoji),
				colour = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			)


			embed.set_thumbnail(url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")
			embed.set_author(name = "Darth Vader", icon_url = "https://cdn.discordapp.com/avatars/995921314512638022/60275f59e5a1794d7d020e4c00e4051c.webp?size=1024")
			embed.set_footer(text = "Sincerly, the lfnm team", icon_url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")

			await ctx.message.add_reaction(emoji)

			await ctx.send(embed = embed)

	@paid.error
	async def paid_error(self, ctx, error):


		if isinstance(error, commands.UserInputError):

			paynow_usage_message = str("""```diff\n- $paid [Paypal Transaction id] [First Name] [Last Name] [Account/Service Abbreviation] [PSN Email(OPTIONAL)] [PSN Password(OPTIONAL)] [2FA Backup Code(OPTIONAL)]```""")
			emoji = "<a:jj:997043065095192603>"

			embed = discord.Embed(
				title = "**Improper usage of ${} command**".format(ctx.command),
				description = "**Please use this command properly as follows:**\n\n**{}** \n{}(**Abbreviations** can be **FOUND** using the **$payhelp** command or by visiting our **payment channel** in the **lfnm_modz server**.)".format(paynow_usage_message, emoji),
				colour = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			)


			embed.set_thumbnail(url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")
			embed.set_author(name = "Darth Vader", icon_url = "https://cdn.discordapp.com/avatars/995921314512638022/60275f59e5a1794d7d020e4c00e4051c.webp?size=1024")
			embed.set_footer(text = "Sincerly, the lfnm team", icon_url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")

			await ctx.message.add_reaction(emoji)

			await ctx.send(embed = embed)



def setup(client):
	client.add_cog(Payment_tools(client))
