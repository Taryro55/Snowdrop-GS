import discord, json, pathlib, os
from discord import Embed
from discord.ext import commands

from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow


path = pathlib.Path(__file__).parent.parent.resolve()

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



class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Command to check if the bot is alive
    @commands.command()
    async def test(self, ctx):
        await ctx.send('Test')


    @cog_ext.cog_slash(name="test", guild_ids = guild_id,
            description="Test the bot.",
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(member_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def _test(self, ctx: SlashContext):
        os.system('cls')
        embed = Embed(description="Hey, Im alive!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Test(bot))