import discord
import os
import requests
import openai

from openai import AsyncOpenAI
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key = os.getenv('CHATGPT_API_KEY'))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="bart ", intents=intents, case_insensitive=True)

api_url = 'https://api.api-ninjas.com/v1/facts'

@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')

@bot.command()
async def fact(ctx):
	response = requests.get(api_url, headers={'X-Api-Key': os.getenv('NINJA_API_KEY')})

	if response.status_code == requests.codes.ok:
		await ctx.reply(f"Did you know, {response.json()[0].get('fact')}")
	else:
		await ctx.reply("I am having a bit of a headache from your brainrot, please ask me again later..")
		print("Error:", response.status_code, response.text)

@bot.command()
async def yo(ctx, *, message):
	if message:
		chat = await client.chat.completions.create(
			messages=[
				{
					"role": "system",
					"content": "You are a smart old man. You will find a counter argument for what the user says. Act like you DO NOT AGREE with the user, no matter how right the user is.",
				},
				{
					"role": "user",
					"content": message,
				}
			],
			model="gpt-3.5-turbo",
		)
	else:
		return await ctx.reply("The strongest argument is no argument, I accept defeat.")
    
	reply = chat.choices[0].message.content
	print(f"ChatGPT: {reply}")

	await ctx.reply(reply)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	await bot.process_commands(message)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
