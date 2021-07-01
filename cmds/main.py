import discord
from discord.ext import commands

from core.classes import Cog_Extension

import datetime

class Main(Cog_Extension):

    #Ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)') # *1000轉成毫秒 round()四捨五入

    #嵌入訊息
    @commands.command()
    async def em(self, ctx):
        embed=discord.Embed(title="第一節課！", description=":bell: :bell: :bell: :bell: :bell: ", color=0xff9500)
        embed.set_author(name="ClassR")
        embed.add_field(name="這一節課", value="0810 ~ 0900", inline=True)
        embed.add_field(name="下一節課", value="0910 ~ 1000", inline=True)
        embed.set_footer(text="𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡")
        await ctx.send(embed=embed)

    #復誦 & 刪除訊息
    @commands.command()
    async def sayd(self, ctx, *,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)


    

def setup(bot):
    bot.add_cog(Main(bot))


