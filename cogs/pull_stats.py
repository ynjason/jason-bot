import aiohttp
import discord
import json
import os
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Context

class Pulls(commands.Cog, name="pulls"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="getpullhistory", description="Get pull history from wuthering waves. Need banner type: limited_char, limited_weapon, standard_char, standard_weapon, beginner, beginner_choice")
    async def getpullhistory(self, context: Context, banner: str) -> None:
        config = await self.bot.database.get_configs(context.author.id)
        if config is None:
            embed = discord.Embed(
                title="Error!",
                description="There is no config for {context.author}",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            config = next(iter((await self.bot.database.get_configs(context.author.id))), None)
            if config is None:
                embed = discord.Embed(
                    title="Error!",
                    description="There is no config for {context.author}",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
        
        banner_dict = {
            "limited_char": 1,
            "limited_weapon": 2,
            "standard_char": 3,
            "standard_weapon": 4,
            "beginner": 5,
            "beginner_choice": 6
        }
        card_pool_type = banner_dict.get(banner, None)
        if card_pool_type is None:
            embed = discord.Embed(
                title="Error!",
                description="Invalid banner. pick one of these limited_char, limited_weapon, standard_char, standard_weapon, beginner, beginner_choice",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://gmserver-api.aki-game2.net/gacha/record/query",
                headers={
                    "authority": "gmserver-api.aki-game2.net",
                    "method":"POST",
                    "path":"/gacha/record/query",
                    "scheme":"https",
                    "accept":"application/json, text/plain, */*",
                    "accept-encoding":"gzip, deflate, br, zstd",
                    "accept-language":"en",
                    "origin":"https://aki-gm-resources-oversea.aki-game.net",
                    "priority":"u=1, i",
                    "referer":"https://aki-gm-resources-oversea.aki-game.net/",
                    "sec-ch-ua":"`'Google Chrome`';v=`'125`', `'Chromium`';v=`'125`', `'Not.A/Brand`';v=`'24`'",
                    "sec-ch-ua-mobile":"?0",
                    "sec-ch-ua-platform":"`'Windows`'",
                    "sec-fetch-dest":"empty",
                    "sec-fetch-mode":"cors",
                    "sec-fetch-site":"cross-site"
                },
                json={
                    "playerId": config[2],
                    "cardPoolId":config[1],
                    "cardPoolType":card_pool_type,
                    "serverId":config[4],
                    "languageCode":"en",
                    "recordId":config[3]
                },
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    path = "temp_data/" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + context.author.name + "wuthering_waves_pull_history.json"
                    with open(path, 'w+') as f:
                        json.dump(data['data'], f)
                    embed = discord.Embed(description="Sucess", color=0xD75BF4)
                    await context.send(embed=embed, file=discord.File(path))
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                    await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Pulls(bot))
