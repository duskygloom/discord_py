import discord
from discord.ext import commands

context_type = commands.Context

def get_member_name(member: discord.Member) -> str:
    name = member.nick
    if name is None:
        name = member.display_name
    return name

class RolesManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="add_roles", 
             parent="Roles",
             description="Assign roles to others... if you are permitted to.",
             usage="$add_roles <member> <role> <role> ...",
             brief="Assign roles to others.",
             help="Assign roles to others, if only you are permitted to modify roles yourself.")
    async def add_roles(
            ctx: context_type, 
            member: discord.Member, 
            *roles: discord.Role
    ):
        if ctx.author.guild_permissions.manage_roles:
            for role in roles:
                await member.add_roles(role)
            await ctx.send(f"Successfully assigned role(s) to {get_member_name(member)}.")
        else:
            await ctx.send(f"You don't have the permission to manage roles, {get_member_name(ctx.author)}.")

    @add_roles.error
    async def add_roles_error(ctx: context_type, error: discord.DiscordException):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Invalid member.")
        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.send("Invalid role.")
        else:
            await ctx.send("Some error occurred.")

    @commands.command(name="remove_roles", 
                parent="Roles",
                description="Removes roles from others... if you are permitted to.",
                usage="$remove_roles <member> <role> <role> ...",
                brief="Removes roles from others.",
                help="Removes roles from others, if only you are permitted to modify roles yourself.")
    async def remove_roles(
            ctx: context_type, 
            member: discord.Member, 
            *roles: discord.Role
    ):
        if ctx.author.guild_permissions.manage_roles:
            for role in roles:
                await member.remove_roles(role)
            await ctx.send(f"Successfully removed role(s) from {get_member_name(member)}.")
        else:
            await ctx.send(f"You don't have the permission to manage roles, {get_member_name(ctx.author)}.")

    @remove_roles.error
    async def remove_roles_error(ctx: context_type, error: discord.DiscordException):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Invalid member.")
        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.send("Invalid role.")
        else:
            await ctx.send("Some error occurred.")

def setup(bot: commands.Bot):
    bot.add_cog(RolesManagement(bot))
