import discord, logging, secret, asyncio
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

async def load_extensions():
    extensions = ["pinkbot/commands/general", "pinkbot/commands/roles"]
    for extension in extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    try:
        asyncio.run(load_extensions())
        bot.run(secret.bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
