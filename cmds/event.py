import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

#mode = 'r' 命名jfile
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
    pass
    # @commands.Cog.listener()
    # async def on_message(self,msg):

        #if msg.content == 'apple':
        #    await msg.channel.send('hi')

        # if msg.content.endswith('apple'):
        #     await msg.channel.send('hi')

        #避免被自己觸發
        # if msg.content == 'apple' and msg.author != self.bot.user:
        #     await msg.channel.send('apple')

        # keyword = ['green','blue','red']
        # if msg.content in keyword:
        #      await msg.channel.send('color!')





def setup(bot):
    bot.add_cog(Event(bot))

