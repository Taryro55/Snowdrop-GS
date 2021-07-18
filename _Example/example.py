import discord
import os
import pathlib
from asyncio import sleep
from discord.ext import commands

intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='_', intents=intents)
bot.remove_command("help")


# Command to be called when its needed to load the cogs
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} was loaded')

# Command to be called when its needed to unload the cogs
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} was unloaded')

# Gets the file directory
path = pathlib.Path(__file__).parent.absolute()
path = str(path) + r'\cogs'

# Looks for the current directory the cogs folder, and outputs them to the filename str var.
for filename in os.listdir(path):
    #Checks if the filename is a .py file
    if filename.endswith('.py'):
        # Loads the files. The [:-3] splits the last 3 characters to load only the name, not the .py extension.
        bot.load_extension(f'cogs.{filename[:-3]}')


# Gets and executes the bot with its token
TOKEN = 'ODMyNDAyMDg4NDExMzk4MTg2.YHjQ2w.1Sx4E_Q-NMhf_uuUcPyC4FKPT5Q'
bot.run(TOKEN)