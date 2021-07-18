import discord
import pathlib
import json
from asyncio import sleep
from discord.ext import commands
from discord import Embed

from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

# Gets some paths
path = pathlib.Path(__file__).parent.parent.resolve()
pathGuildConfig = str(path) + r'\guildConfig'

def get_guild(int):
    with open(str(path) + r'\config.json', 'r') as f:
        guild_id = json.load(f)
    if int == 1:
        return guild_id[str('GuildID')]
    elif int == 2:
        return guild_id[str('ModID')]
    elif int == 3:
        return guild_id[str('MemberID')]

guild_id = {int(get_guild(1))}
guild_id_int = int(get_guild(1))
member_id = int(get_guild(3))



# This class passes the variable 'bot' in bot.py to this file
class MainCog(commands.Cog):

    def __init__(self, bot):
        # This allows the passing the 'bot' within the cog
        self.bot = bot
    # Events/Commands on cogs. You have to have this '@commands.Cog.listener()'/'@commands.command()' decorator, just like you have to have @bot.event on the main file


    # Event to do something when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"The bot is ready!")


    # Command to check the latency of the bot
    @cog_ext.cog_slash(name="Ping", guild_ids = guild_id,
            description="Returns the ping in ms of the bot.",
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(member_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def ping(self, ctx):
        # Included in the Discord.py library, also its multiplied to be on ms
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'The ping is {latency}ms')


    # Event to trigger when a message is sent, if the messsage is tagging the bot, it reacts
    @commands.Cog.listener()
    async def on_message(self, ctx):
        mention = f'<@!{self.bot.user.id}>'
        if mention in ctx.content:
            with open (pathGuildConfig + r'\prefixes.json', 'r') as f:
                prefix = json.load(f)
            prefix = prefix[str(ctx.guild.id)]
            await ctx.channel.send(f"My prefix is {prefix}")


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # On join, adds the guild.id and its value to the database
        # Opens a file, a variable is set, the variable is dumped into the open file
        with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
            prefixes = json.load(f)
        # Add a new value to the key guild.id, in this case, a dot. Now the default prefix is a dot.
        prefixes[str(guild.id)] = '.'

        with open(pathGuildConfig + r'\prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
    

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # On leave, removes the guild.id and its value from the database
        # Opens a file, a key is poped out, the updated key is dumped into the open file
        with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
            prefixes = json.load(f)
        # Remvoes out the string guild id.
        prefixes.pop(str(guild.id))

        with open(pathGuildConfig + r'\prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        with open(pathGuildConfig + r'\admins.json', 'r') as f:
            admins = json.load(f) 
        admins.pop[str(guild.id)]
        with open(pathGuildConfig + r'\admins.json', 'w') as f:
            json.dump(admins, f, indent=4)



# This funcion allows to link this cog to the bot.py
def setup(bot):
    # Adds the cog into the main bot file
    # Gets the method .add_cog of the 'bot' from bot.py 'bot' that was passed previously. It inicializes the cog MainCog
    bot.add_cog(MainCog(bot))