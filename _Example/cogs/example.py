import discord
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands.core import command

# This class passes the variable 'bot' in japetus.py to this file
class Example(commands.Cog):

    def __init__(self, bot):
        # This allows the passing the 'bot' within the cog
        self.bot = bot

    # Examples on using events and commands in cogs.

    # Events on cogs
    # You have to have this '@commands.Cog.listener()' decorator, just like you have to have @bot.event on the main file
    @commands.Cog.listener()
    async def on_ready(self):
        # Prints ready on the console when its ready
        print('Ready!')
        #await bot.loop.create_task(status())


    # Commands on cogs. You have to have this '@commands.command()' decorator, just like you have to have @bot.command on the main file
    # Command to check the latency of the bot
    @commands.command()
    async def ping(self, ctx):
        # Get the latency of the bot
        #latency = bot.latency  # Included in the Discord.py library
        # Send it to the user
        #await ctx.send(latency)
        await ctx.send('Pong!')


# This funcion allows to link this cog to the japetus.py
def setup(bot):
    # Gets the method .add_cog of the 'bot' from japetus.py 'bot' that was passed previously
    # It does what is on the class Example, meaning it inicializes the cog
    bot.add_cog(Example(bot))