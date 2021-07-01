import discord
from discord.ext import commands
import json
import random
import os
import keep_alive

#mode = 'r' 命名jfile
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="^",intents=intents)


@bot.event
async def on_ready():
    print("~~ BOT IS ONLINE ~~")


#load & unload & reload
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'c6mds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')

#
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')



if __name__ == "__main__":
    #TOKEN
    keep_alive.keep_alive()
    bot.run(os.environ['TOKEN'])