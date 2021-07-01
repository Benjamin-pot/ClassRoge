import discord
from discord.ext import commands
import json
import random


#mode = 'r' 命名jfile
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

from core.classes import Cog_Extension

class React(Cog_Extension):

    #圖片
    @commands.command()
    async def cat(self, ctx):
        random_pic = random.choice(jdata['pic_cat'])
        pic = discord.File(f'{jdata["pic"]}{random_pic}')
        await ctx.send(file= pic)

    @commands.command()
    async def dog(self, ctx):
        pic = jdata["url_dog"]
        await ctx.send(pic)



def setup(bot):
    bot.add_cog(React(bot))