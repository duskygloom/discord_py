import discord, logging, secret
from discord.ext import commands

discord.utils.setup_logging()

context_type = commands.context.Context

activity = "Listening to you."

bot = commands.Bot(
    command_prefix="$",
    intents=discord.Intents.all(),
    case_insensitive=True,
    strip_after_prefix=True
)

bot.activity = discord.CustomActivity(activity)
bot.status = discord.Status.idle

def get_member_name(self, member: discord.Member) -> str:
    name = member.nick
    if name is None:
        name = member.display_name
    return name

# events

@bot.event
async def on_ready():
    logging.info(f"{bot.user} is online.")
    for guild in bot.guilds:
        await guild.system_channel.send("I am online now.")

@bot.event
async def on_member_join(member: discord.Member):
    await member.guild.system_channel.send(f"Welcome {bot.get_member_name(member)}!")

# commands

@bot.command(name="echo", 
             parent="Dumb",
             description="Make me say anything.",
             usage="$echo what to repeat ...",
             brief="Repeat before me.",
             help="The bot repeats what you say.")
async def echo(ctx: context_type, *, text: str):
    await ctx.send(text)

@bot.command(name="ask_feature", 
             parent="Feedback",
             description="Need something else? Ask it, maybe I can help.",
             usage="$ask_feature feature continues onward ...",
             brief="Request for a new feature.",
             help="Ask the developers for a new feature.")
async def ask_feature(ctx: context_type, *, text: str):
    with open("feature_requests.txt", "a") as f:
        f.write(f"{text}\n")

@bot.command(name="add_roles", 
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

@bot.command(name="remove_roles", 
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

if __name__ == "__main__":
    try:
        bot.run(secret.bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
