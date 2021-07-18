import discord
import pathlib
import json
import os
from asyncio import sleep
from discord.channel import VoiceChannel
from discord.ext import commands
from discord import Embed
from discord.ext.commands.converter import VoiceChannelConverter

from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

path = pathlib.Path(__file__).parent.parent.resolve()
pathGuildConfig = str(path) + r'\guildConfig'
pathCogs = str(path) + r'\cogs'


buttons_ids = []
for cogFilename in os.listdir(pathCogs):
    if cogFilename.endswith('.py'):
        cogFilename = cogFilename[:-3]
        buttons_ids.append(cogFilename)


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
mod_id = int(get_guild(2))


class ManagerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Clears certain ammount of messages from a channel.
    @cog_ext.cog_slash(name="z-migrate", guild_ids = guild_id,
            description="Moves all of the vc users to another.",   
            options=[
               create_option(
                 name="vc_id",
                 description="Set a vc id to change the users.",
                 option_type=3,
                 required=True
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def vc_changer(self, ctx: SlashContext, vc_id: VoiceChannel):
        if ctx.author.voice and ctx.author.voice.channel:

            # Change this on the multi guild branch
            move_vc_input = int(vc_id)
            move_vc_channel = discord.utils.get(self.bot.get_all_channels(), id=move_vc_input)
            
            original_vc = ctx.author.voice.channel #The original vc
            original_vc_members = original_vc.members # All conected users

            if ctx.author.voice.channel.id != move_vc_channel.id:

                for eachmember in original_vc_members:
                    original_vc_members_count = len(original_vc_members)
                    await eachmember.move_to(move_vc_channel)
                
                embed = Embed(description=f"Success! Moved {original_vc_members_count} users from {original_vc} to {move_vc_channel}.")
                print(embed.to_dict())
                await ctx.send(embed=embed)

            else:
                embed = Embed(description=f"You already are on that vc!")
                print(embed.to_dict())
                await ctx.send(embed=embed)
                
        else:
            await ctx.send("You are not connected to a voice channel")
            return


    # Clears certain ammount of messages from a channel.
    @cog_ext.cog_slash(name="z-purge", guild_ids = guild_id,
            description="Purges a certain ammount of messages.",
            options=[
               create_option(
                 name="messages",
                 description="Ammount of messages to be deleted.",
                 option_type=4,
                 required=True
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def purge(self, ctx: SlashContext, messages: int):
        ammount = int(messages)
        await ctx.channel.purge(limit=ammount)
        embed = Embed(description=f"Purged {ammount} messages.")
        await ctx.send(embed=embed)


    # Allows to change the prefix
    @cog_ext.cog_slash(name="z-prefix", guild_ids = guild_id,
            description="Changes the prefix of the bot.",
            options=[
               create_option(
                 name="prefix",
                 description="Set a prefix. One character only.",
                 option_type=3,
                 required=False
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def prefix(self, ctx, prefix):
        if len(prefix) == 1:
            # Opens a file
            with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
                prefixes = json.load(f)

            # Checks the new and the stored (in the json) prefix
            if prefix != prefixes[str(ctx.guild.id)]:
                prefixes[str(ctx.guild.id)] = prefix
                with open(pathGuildConfig + r'\prefixes.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                await ctx.send(f'The prefix was set to {prefix}')
                f.close()

            elif prefix == prefixes[str(ctx.guild.id)]:
                await ctx.send(f'The prefix is already set to {prefix}')
            
        elif len(prefix) >= 2:
            await ctx.send('The prefix must be one character long.')
            print(len(prefix))
            print(prefix)
        
        elif prefix == None:
            with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
                prefixes = json.load(f)
            await ctx.send(f'The current prefix is: {prefixes[str(ctx.guild.id)]}')


    # Allows to change the time of jail on normal mode
    @cog_ext.cog_slash(name="z-jTime", guild_ids = guild_id,
            description="Changes the normal jail time.",
            options=[
               create_option(
                 name="time",
                 description="Set a new time.",
                 option_type=4,
                 required=True
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def j_time(self, ctx, time: int):
        
        with open(str(path) + r'\config.json', 'r') as f:
            config = json.load(f)

            # Checks the new and the stored (in the json) prefix
            if str(time) != config[str('Jail')][str('TimeJailed')]:
                config[str('Jail')][str('TimeJailed')] = time
                with open(str(path) + r'\config.json', 'w') as f:
                    json.dump(config, f, indent=4)
                await ctx.send(f'The time was set to {time}')

            elif time == config[str('Jail')][str('TimeJailed')]:
                await ctx.send(f'The time is already set to {time}')

    
    # Creates a message with buttons to reload cogs
    @cog_ext.cog_slash(name="z-cogButton", guild_ids = guild_id,
            description="Creates a message with components to reload cogs quicker.",
            default_permission=False,
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def cog_button(self, ctx: SlashContext):
        embed = Embed(description='Here are the buttons to manage Cogs')
        buttons = []
        global buttons_ids
        
        for cogFilename in os.listdir(pathCogs):
            if cogFilename.endswith('.py'):
                cogFilename = cogFilename[:-3]

                newButton = create_button(
                    style=ButtonStyle.red,
                    label=f"Restart {cogFilename.title()} Cog",
                    custom_id=f'{cogFilename}'
                )
                buttons.append(newButton)
                
        action_row = create_actionrow(*buttons)
        await ctx.send(embed=embed, components=[action_row])

    
    @cog_ext.cog_component(components=buttons_ids)
    async def hello(self, ctx: ComponentContext):
        await ctx.edit_origin(content=None)

        try:
            self.bot.unload_extension(f'cogs.{ctx.custom_id}')
        except discord.ext.commands.errors.ExtensionNotLoaded:
            self.bot.load_extension(f'cogs.{ctx.custom_id}')
            embed = Embed(description=f'The extension {ctx.custom_id.title()} is unloaded. Loading it.')
            print(embed.to_dict())
            msg = await ctx.send(embed=embed)

        try:
            self.bot.load_extension(f'cogs.{ctx.custom_id}')
        except discord.ext.commands.errors.ExtensionAlreadyLoaded:
            pass

        embed = Embed(description=f'The extension {ctx.custom_id.title()} was reloaded')
        try:
            await msg.edit(embed=embed)
        except:
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=10)
    


    # Kicks a user
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)


    # Bans a user
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason = reason)


    # Nicks a user
    @commands.command()
    async def nick(self, ctx, member: discord.Member, *, argument):
        await member.edit(nick=argument)


    # Outputs the saved prefix
    @commands.command()
    async def checkprefix(self, ctx):
        path = pathlib.Path(__file__).parent.parent.resolve()
        pathGuildConfig = str(path) + r'\guildConfig'
        def get_prefix():
            with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
                prefixes = json.load(f)

            return prefixes[str(ctx.guild.id)]

        prefixvalue = get_prefix()
        await ctx.send(f"The prefix for the server is {prefixvalue}")
        pass


def setup(bot):
    bot.add_cog(ManagerCog(bot))