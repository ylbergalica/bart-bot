import discord
import os
import requests
import google.generativeai as genai

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="bart ", intents=intents, case_insensitive=True)

api_url = 'https://api.api-ninjas.com/v1/facts'

@bot.command()
async def fact(ctx):
	response = requests.get(api_url, headers={'X-Api-Key': os.getenv('NINJA_API_KEY')})

	if response.status_code == requests.codes.ok:
		await ctx.reply(f"Did you know, {response.json()[0].get('fact')}")
	else:
		await ctx.reply("I am having a bit of a headache from your brainrot, please ask me again later..")
		print("Error:", response.status_code, response.text)

@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	await bot.process_commands(message)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
