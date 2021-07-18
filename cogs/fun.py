import discord, json, pathlib
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

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



class FunCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # A command that echos the argument
    @commands.command()
    async def echo(self, ctx, *,argument):
        embed = Embed(description=argument)
        await ctx.message.delete()
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(FunCog(bot))