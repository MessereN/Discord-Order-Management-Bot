import discord
import random
import sys
sys.path.append("..")
import admin_data


def payhelp():


	embed = discord.Embed(
		title = "Payment Assistance and Guidance",
		description = "**Please go through the following commands thoroughly and make sure you are using them correctly. Account/Service Abbreviations are also provided below\n\nIn addition, please use the *$paynow* command first then after paying via the prompted link, proceed to use the *$paid* command to confirm your order with us. It is essential to follow these steps exactly or else failure to comply will result in your order not being completed. __ABSOLUTELY NO EXCEPTIONS__\n**",
		colour = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
	)

	arrow = "<a:arrow1:997022886806159390>"

	descriptions = str("""```fix\n$paynow [Account/Service Abbreviation]\n\n```""") + str("""```fix\n$paid [Paypal Transaction id] [First Name] [Last Name] [Account/Service Abbreviation] [PSN Email(OPTIONAL)] [PSN Password(OPTIONAL)] [2FA Backup Code(OPTIONAL)]```""")

	embed.add_field(name = "**Command**", value = str("""```diff\n- $paynow\n\n```""") + "\n" + str("""```diff\n- $paid```"""))
	embed.add_field(name = "**Usage**", value = descriptions, inline = True)

	embed.add_field(name = "**__Account/Service Abbreviations__**", value = "\u200b", inline = False)

	embed.add_field(name = "**To view associated account/service abbreviations, please scroll down to the next message or visit the *#payment* channel in the LFNM server. Thank you!**", value = "\u200b", inline = False)

	embed.set_thumbnail(url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")
	embed.set_author(name = "Darth Vader", icon_url = "https://cdn.discordapp.com/avatars/995921314512638022/60275f59e5a1794d7d020e4c00e4051c.webp?size=1024")
	embed.set_footer(text = "Sincerly, the lfnm team", icon_url = "https://i.ebayimg.com/00/s/OTAwWDE2MDA=/z/E9sAAOSwivNiHpvU/$_7.JPG")

	return embed
