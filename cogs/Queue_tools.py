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


class Queue_tools(commands.Cog):

	def __init__(self, client):

		self.client = client

	def cog_check(self, ctx):

		return ctx.channel.id == 994442251092627467


	#Notify customer if we are logging into their personal account
	@commands.command()
	@commands.has_permissions(administrator = True)
	async def notify(self, ctx, member: discord.Member):

		await member.send(f'**Hello {member.mention}, we are now logging into your personal account and need you to log out if you are currently using your account. If any questions or concerns arise, please contact the Server Owners and do not reply to this message. Thank you:)**')
		await ctx.send(f'{member.mention} has been successfully notified.')


	#Command to display one of or all the current queues(ONLY FOR USE BY ADMINS)
	@commands.command(name = "displayqueue", aliases = ["display", "show"])
	@commands.has_permissions(administrator = True)
	async def display_queue(self, ctx, queue: str):

		if queue == "acc":

			acc_q = databaseFunc.display_queue_from_db(queue)

			await ctx.send("The Current Base Account Queue: {}".format(acc_q))

		elif queue == "div":

			div_q = databaseFunc.display_queue_from_db(queue)

			await ctx.send("The Current Liquid Divinium Queue: {}".format(div_q))

		elif queue == "acc_div":

			acc_div_q = databaseFunc.display_queue_from_db(queue)

			await ctx.send("The Current Accounts With Liquid Divinium Queue: {}".format(acc_div_q))


		elif queue == "all":

			all_q = databaseFunc.display_queue_from_db(queue)

			await ctx.send("The Current Base Account Queue is: {}\nThe Current Liquid Divinium Queue is: {}\nThe Current Accounts With Liquid Divinium Queue: {}".format(all_q[0], all_q[1], all_q[2]))


		else:
			raise commands.UserInputError



	@commands.command(name = "reset_set", aliases = ["set", "reset", "clear"])
	async def reset_set(self, ctx, account: str):

		result = databaseFunc.clear_db(account)

		if account == "all":
			await ctx.send("The following queues are now empty/reset:\nAccount Queue: {}\nDivinium Queue: {}\nAccount with Divinium Queue: {}".format(result[0], result[1], result[2]))

		elif account == "acc":
			await ctx.send("The Account Queue is empty/reset: {}".format(result))

		elif account == "div":
			await ctx.send("The Divinium Queue is empty/reset: {}".format(result))

		elif account == "acc_div":
			await ctx.send("The Accounts with Divinium Queue is empty/reset: {}".format(result))


		else:
			raise commands.UserInputError



	@commands.command(name = "sendout", aliases = ["send", "sendto"])
	async def send_out(self, ctx, member : discord.Member, search_for: str, service: str, psn_email = None, psn_pass = None):

		raise_error = False
		success = True

		if search_for.lower() == "yes":

			if service.lower() == "acc":

				operation = databaseFunc.look_and_remove_from_queue_at_db(1, str(member))

			elif service.lower() == "div":

				operation = databaseFunc.look_and_remove_from_queue_at_db(2, str(member))

			elif service.lower() == "acc_div":

				operation = databaseFunc.look_and_remove_from_queue_at_db(3, str(member))

			else:

				raise_error = True

			if operation[0] is None:

				success = False

				await ctx.send(f'The member {member} could not be found within the {service.lower()} queue. Please mention a valid member within the server or make sure the member has entered the queue. Come on you 🥩 heads!')


		elif search_for.lower() == "no":

			if service.lower() == "acc":

				operation = databaseFunc.dequeue_from_queue_at_db(1)


			elif service.lower() == "div":

				operation = databaseFunc.dequeue_from_queue_at_db(2)

			elif service.lower() == "acc_div":

				operation = databaseFunc.dequeue_from_queue_at_db(3)


			else:

				success = False
				raise_error = True

			if operation[0] is None:
				success = False

				await ctx.send(f'The {service} queue is empty.')

		else:
			raise_error = True

		if success:

			if psn_email is None and psn_pass is None:
				message = f'Hello,\nThank you for your purchase. Your order has been fulfilled!\n⭐️⭐️⭐️⭐️⭐️\nIf you’re satisfied with your experience shopping with us, it’ll be greatly appreciated if a review would be left as it helps us out tremendously so we can keep serving customers as yourself.\nThank you for your support,\nWe hope to serve you again soon.\nHave a good one ;)'

			else:
				message = f'Hello,\nThank you for your purchase. Your order has been fulfilled. The account details are below:\n{psn_email}\n{psn_pass}\n❗️In regards to the email, if you want to change it, we recommend you to do so as it’s not an accessible domain. So changing your password will have to be done after you change the email to one that you can access.\n ‼️ DO NOT LOG INTO THE ACCOUNT IMMEDIATELY (wait 30mins+). There may be a issue where a notification pops up asking for a code of some sort logging into the account immediately. Wait 1-2 hours if you are affected by it and try logging into it after the wait we recommend. (This typically happens bc we were just on the account in Canada and within 5-10 mins you have logged into it from USA, Australia, Germany, UK etc. WAIT BEFORE YOU LOG IN).\n⭐️⭐️⭐️⭐️⭐️\nIf you’re satisfied with your experience shopping with us, it’ll be greatly appreciated if a review would be left as it helps us out tremendously so we can keep serving customers as yourself.\nThank you for your support\nWe hope to serve you again soon.\nHave a good one ;)'

			await member.send(message)
			await ctx.send(f'The order has been successfully sent out to {member.mention} and the following order has been removed from {service} queue:\n{operation[0]}\n The updated {service} queue is now:\n{operation[1]}.')



		if raise_error:

			raise commands.UserInputError




	@commands.command(name = "search&delete", aliases = ["s&d"])
	async def search_delete(self, ctx, service: str, lookup_member: discord.Member):

		if service == "acc":

			operation = databaseFunc.look_and_remove_from_queue_at_db(1, str(lookup_member))

		elif service == "div":

			operation = databaseFunc.look_and_remove_from_queue_at_db(2, str(lookup_member))

		elif service == "acc_div":

			operation = databaseFunc.look_and_remove_from_queue_at_db(3, str(lookup_member))

		else:

			raise commands.UserInputError

		await ctx.send(f'{lookup_member.mention} order which was {operation[0]} has been successfully removed from the {service} queue.\nThe updated {service} queue is {operation[1]}.')


	#notify error
	@notify.error
	async def notify_error(self, ctx, error):

		await ctx.send(f'Please use the **${ctx.command}** command properly: **${ctx.command} [mention member in server]**')

	#reset command error
	@reset_set.error
	async def reset_set_eror(self, ctx, error):

		await ctx.send("Reset command error has occurred.")

	#send_out error
	@send_out.error
	async def send_out_error(self, ctx, error):

		await ctx.send("Please use the $sendout command properly as follows:\n$sendout [mention discord member] [search_for(yes/no)] [designated service queue to look in(options: accounts/div/acc_div)] [psn email(optional)], [psn password(optional)]")

	#search & delete error
	@search_delete.error
	async def search_delete_error(self, ctx, error):

		await ctx.send(f'Please use the {ctx.command} as follows:\n${ctx.command} [service queue] [mention discord member to look for].\nAlso, make sure the member you are mentioning is correct and/or in the server. Cheers!')



def setup(client):
	client.add_cog(Queue_tools(client))
