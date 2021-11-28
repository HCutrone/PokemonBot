import discord
from discord.ext import commands
import requests
import json
import requestsHelper as helper

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
  print("We have logged in as bot")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  msg = message.content
  if (msg.startswith("hey")):
    await message.channel.send("wassup")

  await bot.process_commands(message)

@bot.command()
async def test(context, arg):
  await context.send(arg)

@bot.command() 
async def inspire(context):
  quote = helper.inspire()
  await context.send(quote)

@bot.command()
async def popular(context):
  popular_movies = helper.get_popular()
  await context.send(popular_movies)

@bot.command()
async def toprated(context):
  toprated_movies = helper.get_rated()
  await context.send(toprated_movies)

@bot.command()
async def pkmn(context, pokemon):
  await context.send("Command that will take a pokemon name/id and returns pokedex entry, type(s), and evolutions.\
                      \n Use !help to see other commands to see more information")

@bot.command()
async def abilities(context, pokemon):
  #/
  # input:
  #   pokemon name or id
  # output:
  #   the pokemon's abilities and descriptions
  # /#
  await context.send(helper.getAbilities(pokemon))

@bot.command()
async def type(context, pokemon):
  # input:
  #   pokemon name or id
  # output:
  #   the pokemon's type(s) and strengths and weaknesses


  #await context.send("Takes a Pokemon's names or id and returns the Pokemon's types and strengths and weaknesses."
  msg = ""
  msg += helper.getTypes(pokemon) + "\n"
  msg += "Strengths:\n"
  msg += helper.getStrengths(pokemon)
  msg += "Weaknesses:\n"
  msg += helper.getWeaknesses(pokemon)
  await context.send(msg)

@bot.command()
async def evol(context, *args):
  await context.send("Evolutions command")
  
bot.run("OTA5NTU0MjkzODAyMTM5Njc4.YZF-cg.h4h7ZL-KxvMG6XdJehkUltlbvBE")