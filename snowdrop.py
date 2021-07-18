import discord
import json
import os
import pathlib
from discord import Embed
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType


# Gets the file directory
path = pathlib.Path(__file__).parent.resolve()
pathGuildConfig = str(path) + r'\guildConfig'
def get_prefix(bot, message):
    with open(pathGuildConfig + r'\prefixes.json', 'r') as f:
      prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


# Funcion to get the config values
def get_guild(int):
  with open('config.json', 'r') as f:
    guild_id = json.load(f)
  if int == 1:
    return guild_id[str('GuildID')]
  elif int == 2:
    return guild_id[str('ModID')]
  elif int == 3:
    return guild_id[str('MemberID')]
  elif int == 0:
    return guild_id[str('Token')]
guild_id = {int(get_guild(1))}
guild_id_int = int(get_guild(1))
mod_id = int(get_guild(2))
Token = str(get_guild(0))

cogs_choices = [
  create_choice(
    name="Admin",
    value="admin"
  ),
  create_choice(
    name="Main",
    value="main"
  ),
  create_choice(
    name="Fun",
    value="fun"
  ),
  create_choice(
    name="Test",
    value="test"
  ),
  create_choice(
    name="Token",
    value="token"
  )
]


intents = discord.Intents().all()
intents.members = True
# To get the command prefix, run the funcion get_prefix
bot = commands.Bot(command_prefix = get_prefix, intents = intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload = True)
bot.remove_command("help")



# Commands to be called when its needed to load, unload or reload the cogs
@slash.slash(name="z-load", guild_ids = guild_id,
            description="Admin Only. Load a given cog.",
            options=[
               create_option(
                 name="load",
                 description="Set a cog to load.",
                 option_type=3,
                 required=True,
                 choices = cogs_choices
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
async def load(ctx, load: str):
  try:
    bot.load_extension(f'cogs.{load}')

    embed = Embed(description=f'The extension {load.title()} was loaded')
    print(embed.to_dict())
    await ctx.send(embed=embed)
  except discord.ext.commands.errors.ExtensionAlreadyLoaded:
    embed = Embed(description=f'The extension {load.title()} is already loaded')
    print(embed.to_dict())
    await ctx.send(embed=embed)


@slash.slash(name="z-unload", guild_ids = guild_id,
            description="Admin Only. Unload a given cog.",
            options=[
               create_option(
                 name="unload",
                 description="Set a cog to unload.",
                 option_type=3,
                 required=True,
                 choices = cogs_choices
               )
              ],
            default_permission=False,
            permissions={
              guild_id_int: [
                create_permission(mod_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
async def unload(ctx, unload: str):
  try:
    bot.unload_extension(f'cogs.{unload}')

    embed = Embed(description=f'The extension {unload.title()} was unloaded')
    print(embed.to_dict())
    await ctx.send(embed=embed)
  except discord.ext.commands.errors.ExtensionNotLoaded:
    embed = Embed(description=f'The extension {unload.title()} is already unloaded')
    print(embed.to_dict())
    await ctx.send(embed=embed)


@slash.slash(name="z-reload", guild_ids = guild_id,
            description="Admin Only. Reload a given cog.",
            options=[
               create_option(
                 name="reload",
                 description="Set a cog to reload.",
                 option_type=3,
                 required=True,
                 choices = cogs_choices
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
async def reload(ctx, reload: str):
  try:
    bot.unload_extension(f'cogs.{reload}')
  except discord.ext.commands.errors.ExtensionNotLoaded:
    bot.load_extension(f'cogs.{reload}')
    embed = Embed(description=f'The extension {reload.title()} is unloaded. Loading it.')
    print(embed.to_dict())
    msg = await ctx.send(embed=embed)

  try:
    bot.load_extension(f'cogs.{reload}')
  except discord.ext.commands.errors.ExtensionAlreadyLoaded:
    pass

  embed = Embed(description=f'The extension {reload.title()} was reloaded')
  try:
    await msg.edit(embed=embed)
  except:
    await ctx.send(embed=embed)



# Looks for the current directory the cogs folder, and outputs them to the filename str var.
pathCogs = str(path) + r'\cogs'

for filename in os.listdir(pathCogs):
    if filename.endswith('.py'):         # Loads the files. The [:3] splits the last 3 characters to load only the name, not the extension.
        bot.load_extension(f'cogs.{filename[:-3]}')
# Gets and executes the bot with its token

bot.run(Token)