import aiohttp
import random
import discord
from discord.ext import commands


class Scammer(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.group(name='scammer', hidden=True, aliases=['s'], invoke_without_command=True)
    async def scammer(self, ctx):
        await ctx.send(f'Why are you here? You shall use my subcommands instead!: ``!scammer check <ign>``')

    @scammer.command(name='check', usage='scammer check <IGNorUUID>',
                     description='`<IGNorUUID>` ~ The IGN or the UUID of the player you want to check\nChecks player <IGNorUUID> and see if he is a scammer or not',
                     aliases=['c'])
    async def check(self, ctx, IGNorUUID):
        ret = await self.client.currentPT.queryScammer(username=IGNorUUID)
        if ret == 'INVPLY':
            embed = discord.Embed(title=f'Invalid Player Specified',
                                  colour=discord.Colour.gold())
            embed.add_field(name='We can\'t get the data from Mojang API', value='This username / UUID is INVALID')
            await ctx.send(embed=embed)
            return
        if ret == 'NOTSCM':
            embed = discord.Embed(title=f'User is innocent', colour=discord.Colour.green())
            embed.add_field(name='This user is not a scammer',
                            value='But you still have to be careful while trading with anyone!')
            
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=f'USER IS A SCAMMER', colour=discord.Colour.red())
        embed.add_field(name='THIS USER IS A SCAMMER',
                        value='DO NOT TRADE WITH THIS USER!!!', inline=False)
        embed.add_field(name='SCAMMER DETAILS', value=f'IGN: {ret[3]}\nReason: {ret[1]}', inline=False)
        await ctx.send(embed=embed)

    @commands.has_any_role(688745505701888018)
    @scammer.command(name='add',
                     description='<ign> ~ Scammer\'s IGN, obviously\n<discordID> ~ ID of the user discord, can be either a ping to them (@someone#1234) or their ID (466769036122783744) or N/A if they dont have one\n<reason> ~ The reason of why you want to add this user to scammer list\nAdds user <ign> into scammer list with reason <reason>',
                     usage='scammer add <ign> <discordID> <reason>')
    async def add(self, ctx, ign, discordID, *, reason):        
        if '<' in discordID:
            discordID = discordID.replace('<', '').replace('>', '').replace('@', '')
        if '#' in discordID:
            await ctx.send(
                content='Please either mention the user (@someone#1234) or enter the user \'s ID (614505992964800552)')
            return
        discordID = f'<@{discordID}>'
        if isinstance(await self.client.currentPT.queryScammer(ign), list):
            await ctx.send(content='User already in scammer database, how much do you hate him to add him twice')
            return
        await self.client.currentPT.addScammer(username=ign, reason=reason, responsible_staff=str(ctx.message.author))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        url = f'https://namemc.com/profile/{ign}'
        async with aiohttp.ClientSession(headers=headers) as cs:
            async with cs.get(url) as r:
                url = r.url
        embed = discord.Embed(title=ign, colour=discord.Colour.from_rgb(random.randint(1, 255), random.randint(1, 255),
                                                                        random.randint(1, 255)))
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Discord', value=discordID)
        embed.add_field(name='NameMC', value=str(url))
        embed.set_thumbnail(url=f'https://minotar.net/helm/{ign}/69420.png')
        cc = self.client.get_channel(617952920046010375)
        
        try:
            msgctx2 = await cc.send(embed=embed)
            await ctx.send(
                content=f'Completed! Check `$s check {ign}` for command result')
        except discord.Forbidden:
            await ctx.send('meh')
        

    @commands.has_any_role(688745505701888018)
    @scammer.command(name='remove', usage='scammer remove <ign>',
                     description='<ign> ~ IGN of scammer you wish to remove\nRemove a possible innocent from the scammer database')
    async def remove(self, ctx, ign):
        
        if not isinstance(await self.client.currentPT.queryScammer(ign), list):
            await ctx.send(f'This user isn\'t even a scammer what you wish will happen???')
            return
        ret = await self.client.currentPT.removeScammer(username=ign)
        if ret is None:
            await ctx.send(
                f'This user doesn\' even exist in Minecraft world why would you want to do that???')
            return
        
        await ctx.send('Removal Succeeded')


def setup(bot):
    bot.add_cog(Scammer(bot))
