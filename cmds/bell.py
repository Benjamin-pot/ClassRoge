import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, queue
import datetime
from datetime import timezone, timedelta


class Bell(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("setting.json", 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)

        #設定時區
        tz = timezone(timedelta(hours=+8))

        #設定迴圈
        async def bell_start():
            await self.bot.wait_until_ready()

            #channel
            self.channel = self.bot.get_channel(int(jdata['channel']))

            await self.channel.send("bell_start success!")

            #現在時間
            now_time = datetime.datetime.now(tz).strftime("%H%M")
            #是否上課中
            self.Class = 0

            self.time_list = queue.Queue(maxsize=15)

            for i in jdata['bell']:
                if now_time < i['start']:
                    #未開始上課
                    self.time_list.put(i)
                elif now_time < i['end']:
                    #上課中
                    self.time_list.put(i)
                    self.Class = 1

        #偵測時間做反應

        async def bell_run():
            await self.bot.loop.create_task(bell_start())

            await self.channel.send('bell_run success')

            #判斷有沒有bell
            if self.time_list.empty():
                self.bell_on = 0  #是否還有bell
            else:
                self.now_Class = self.time_list.get()  #上課時間
                self.bell_on = 1

            # print(type(self.now_Class))
            # print(self.now_Class)
            # self.now_Class.clear()
            # print(self.now_Class)
            # print(len(self.now_Class))

            while self.bell_on:
                now_time = datetime.datetime.now(tz).strftime("%H%M")

                #await self.channel.send(now_time)

                if now_time == self.now_Class['start'] and self.Class == 0:
                    self.Class = 1
                    await self.time_for_class()
                    #await self.channel.send(self.now_Class['start_text'])

                elif now_time == self.now_Class['end']:
                    self.Class = 0

                    #await self.channel.send(self.now_Class['end_text'])
                    if self.time_list.empty():
                        self.bell_on = 0
                        # print(self.now_Class)

                    await self.after_class()
                    # print("AC")

                await asyncio.sleep(1)

            await self.channel.send("All bells have done.")

        self.bg_task = self.bot.loop.create_task(bell_run())

    #上課
    async def time_for_class(self):

        with open("setting.json", 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)

        #訊息
        embed = discord.Embed(
            title=self.now_Class['start_text'],
            description=":bell: :bell: :bell: :bell: :bell: ",
            color=0xffae00)
        embed.set_author(name="ClassRoge")
        embed.add_field(
            name="這一節課",
            value=f"{self.now_Class['start']}~{self.now_Class['end']}")
        embed.set_footer(text="𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡")
        await self.channel.send(embed=embed)

        #移動
        self.AllWantClass = self.channel.guild.get_role(int(jdata['AllWantClass_role']))
        #await self.channel.send(self.AllWantClass)

        self.Class_vc = self.bot.get_channel(int(jdata['Class_vc']))
        #await self.channel.send(self.Class_vc)

        for WantClass in self.AllWantClass.members:
           # await self.channel.send(WantClass.name)
            #檢查有沒有連接語音
            if WantClass.voice is None:
              await self.channel.send(f'{WantClass.mention}沒有進語音頻道喔')
            else:
              await WantClass.move_to(self.Class_vc)

    # 下課
    async def after_class(self):

        with open("setting.json", 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)

        embed = discord.Embed(
            title=self.now_Class['end_text'],
            description=":bell: :bell: :bell: :bell: :bell: ",
            color=0x916800)
        embed.set_author(name="ClassRoge")

        ####
        if self.bell_on != 0:
            self.now_Class = self.time_list.get()

        if self.bell_on == 0:
            print('sdfsdfsdf')
            embed.add_field(name="YAAAAAA~~~", value="沒有下一節")
        else:
            embed.add_field(
                name="下一節課",
                value=f"{self.now_Class['start']}~{self.now_Class['end']}")
        embed.set_footer(text="𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡𝓒𝓵𝓪𝓼𝓼𝓡")
        await self.channel.send(embed=embed)

        #移動
        self.AllWantClass = self.channel.guild.get_role(int(jdata['AllWantClass_role']))
        #await self.channel.send(self.AllWantClass)

        self.AfterClass_vc = self.bot.get_channel(int(jdata['AfterClass_vc']))

        #await self.channel.send(self.AfterClass_vc)

        for WantClass in self.AllWantClass.members:
            if WantClass.voice is None:
              await self.channel.send(f'{WantClass.mention}沒有進語音頻道喔')
            else:
              await WantClass.move_to(self.AfterClass_vc)

    #設定頻道
    # @commands.command()
    # async def set_channel(self, ctx, ch: int):
    #     self.channel = self.bot.get_channel(ch)
    #     await ctx.send(f'Set channel:{self.channel.mention}')


    #查詢Class 是否上課中
    @commands.command()
    async def now(self, ctx):
        if self.Class:
            await ctx.send('現在是上課ㄟ')
        else:
            await ctx.send('下課TIME')


    #設定時間
    # @commands.command()
    # async def set_time(self, ctx, time):

    #     self.counter = 0

    #     with open("setting.json", 'r', encoding='utf8') as jfile:
    #         jdata = json.load(jfile)
    #     jdata['time'] = time

    #     with open("setting.json", 'w', encoding='utf8') as jfile:
    #         json.dump(jdata, jfile, indent=4)

    #     await ctx.send(f'Set time:{time}')


def setup(bot):
    bot.add_cog(Bell(bot))
