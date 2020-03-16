import discord
from discord.ext import commands


from utils.prices import PricesTable



class JerryBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        
        self.currentPT = PricesTable()
        super().__init__(command_prefix, **options)

client = JerryBot(command_prefix='!')
cog_list = ['cogs.scammer']
for i in cog_list:
    client.load_extension(i)    
    
@client.event
async def on_ready():
	print('running')

client.run('Njg4NzUxMzQ5MTg5NzA1NzY1.Xm43tQ.NmtAkLxMHN3qYG87FaO1jOn_CxY')
