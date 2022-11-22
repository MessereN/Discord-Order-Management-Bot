import discord
from discord.ext import commands
import logs_func

class Log_tools(commands.Cog):

	def __init__(self, client):

		self.client = client

	@commands.command(name = "viewlog")
	@commands.has_any_role("Server Owner(s)", "Modz")
	async def view_log(self, ctx):


		await ctx.send("The contents of the payment log file are:", file = discord.File(fp = "./logs/payment_log.txt"))



	@commands.command(name = "clearlog", aliases = ["clog", "resetlog"])
	@commands.has_any_role("Server Owner(s)", "Modz")
	async def clear_log(self, ctx):

		logs_func.clear_log_file()

		await ctx.send("The log file has been successfully cleared.")

def setup(client):
	client.add_cog(Log_tools(client))
