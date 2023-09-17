import discord
from discord.ext import commands

context_type = commands.Context

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="echo", 
             parent="Dumb",
             description="Make me say anything.",
             usage="$echo what to repeat ...",
             brief="Repeat before me.",
             help="The bot repeats what you say.")
    async def echo(ctx: context_type, *, text: str):
        await ctx.send(text)

    @commands.command(name="ask_feature", 
                parent="Feedback",
                description="Need something else? Ask it, maybe I can help.",
                usage="$ask_feature feature continues onward ...",
                brief="Request for a new feature.",
                help="Ask the developers for a new feature.")
    async def ask_feature(ctx: context_type, *, text: str):
        with open("feature_requests.txt", "a") as f:
            f.write(f"{text}\n")

def setup(bot: commands.Bot):
    bot.add_cog(General(bot))
