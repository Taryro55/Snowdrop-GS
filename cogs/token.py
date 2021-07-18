import discord, json, pathlib

from asyncio import sleep
from discord.ext import commands
from discord import Embed
from discord.utils import get

from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext

# Gets some paths
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
    elif int == 4:
        return guild_id[str('Jail')][str('Jailer')]
    elif int == 5:
        return guild_id[str('JailRemoveRoles')]
    elif int == 6:
        return guild_id[str('Jail')][str('Prisioner')]
    elif int == 7:
        return guild_id[str('Jail')][str('JailVC')]
    elif int == 8:
        return guild_id[str('NickToken')][str('NickerRole')]
    elif int == 9:
        return guild_id[str('Jail')][str('TimeJailed')]
    elif int == 10:
        return guild_id[str('GodToken')]
guild_id = {int(get_guild(1))}
guild_id_int = int(get_guild(1))
mod_id = int(get_guild(2))
member_id = int(get_guild(3))
jail_id = int(get_guild(4))
jail_dict = dict(get_guild(5))
prisioner_id = get_guild(6)
JailVC_id = get_guild(7)
nicker_id = int(get_guild(8))
jail_time = int(get_guild(9))
god_id = int(get_guild(10))


class TokenCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @cog_ext.cog_slash(name="Jail-Token", guild_ids = guild_id,
            description="Sends a user to jail for 30min.",   
            options=[
               create_option(
                 name="user",
                 description="Ping a user.",
                 option_type=6,
                 required=True
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(jail_id, SlashCommandPermissionType.ROLE, True),
                create_permission(god_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def jailToken(self, ctx: SlashContext, user: discord.User):
        if ctx.author.voice and ctx.author.voice.channel: # Checks if connected to a voice channel\
            embed = Embed(description=f'Jailing {user}!')
            self.bot.jail_message = await ctx.send(embed=embed)
            self.bot.jailer_author = ctx.author
            
            try:
                self.bot.og_prisioner_vc = user.voice.channel
            except AttributeError:
                embed = Embed(description=f'{user.nick} is not connected to a vc.')
                await self.bot.jail_message.edit(embed=embed)
                return
            self.bot.jailed_user = user
            move_vc_channel = discord.utils.get(self.bot.get_all_channels(), id=JailVC_id)
            jailer_role = discord.utils.get(ctx.guild.roles, id=int(jail_id))
            await user.move_to(move_vc_channel)
            await ctx.author.remove_roles(jailer_role, reason=f'Used the token on {user}')

            for each_id in jail_dict:
                values = jail_dict[str(each_id)]

                member_role = discord.utils.get(ctx.guild.roles, id=int(values))
                prisioner_role = discord.utils.get(ctx.guild.roles, id=prisioner_id)

                await user.remove_roles(member_role, reason=f'Jailed by {ctx.author}')
            await user.add_roles(prisioner_role, reason=f'Jailed by {ctx.author}')
            buttons = [
                create_button(
                    style=ButtonStyle.green,
                    label=f"Click to free {user.nick} from jail",
                    custom_id='unJail'
                ),
            ]
            action_row = create_actionrow(*buttons)
            await self.bot.jail_message.edit(components=[action_row])
            await sleep(jail_time)
            

            prisioner_role = discord.utils.get(ctx.guild.roles, id=prisioner_id)
            if prisioner_role in user.roles:
                for each_id in jail_dict:
                    values = jail_dict[str(each_id)]
                
                    member_role = discord.utils.get(ctx.guild.roles, id=int(values))
                    prisioner_role = discord.utils.get(ctx.guild.roles, id=prisioner_id)

                    await user.add_roles(member_role, reason=f'Freed of the tirany of {ctx.author}')
                await user.remove_roles(prisioner_role, reason=f'Freed of the tirany of {ctx.author}')
                await user.move_to(self.bot.og_prisioner_vc)
            elif not prisioner_role in user.roles:
                print(f'{user} was freed by the button')

        else:
            embed = Embed(description='You are not connected to a voice channel')
            await ctx.send(embed=embed)
            return


    @cog_ext.cog_component(components='unJail')
    async def unJail(self, ctx: ComponentContext):
        user = self.bot.jailed_user
        jailer_author = self.bot.jailer_author

        if ctx.author == jailer_author:
            for each_id in jail_dict:
                values = jail_dict[str(each_id)]
            
                member_role = discord.utils.get(ctx.guild.roles, id=int(values))
                prisioner_role = discord.utils.get(ctx.guild.roles, id=prisioner_id)

                await user.add_roles(member_role, reason=f'Freed of the tirany of {ctx.author}')
            await user.remove_roles(prisioner_role, reason=f'Freed of the tirany of {ctx.author}')
            await user.move_to(self.bot.og_prisioner_vc)

            embed = Embed(description="Freed! Epic!")
            await ctx.origin_message.edit(embed=embed)
            await ctx.edit_origin(content=None)
            await self.bot.jail_message.edit(components=None)
        elif not ctx.author == jailer_author:
            embed = Embed(description=f'Only {jailer_author} can free him.')
            await ctx.origin_message.edit(embed=embed)
            await ctx.edit_origin(content=None)
            

    @cog_ext.cog_slash(name="Nick-Token", guild_ids = guild_id,
            description="Change the nick of a user.",   
            options=[
               create_option(
                 name="user1",
                 description="Ping a user.",
                 option_type=6,
                 required=True
               ),
               create_option(
                 name="new_nick",
                 description="Set a nick.",
                 option_type=3,
                 required=True
               )
            ],
            default_permission=False,
            # Change to allow a per-guild config with the on_ready event on main.py
            permissions={
              guild_id_int: [
                create_permission(nicker_id, SlashCommandPermissionType.ROLE, True),
                create_permission(god_id, SlashCommandPermissionType.ROLE, True)
                ]
              }
            )
    async def nickToken(self, ctx: SlashContext, user1: discord.User, new_nick: str):
        oldnick = user1.nick
        await user1.edit(nick = new_nick, reason = f'NickToken used by {ctx.author}')
        embed = Embed(description=f'The user {oldnick} has been nicked! The new nick is {user1.nick}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TokenCog(bot))