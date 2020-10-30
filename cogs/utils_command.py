from discord import Embed
from discord.ext import commands
from consts import *

class Utils(commands.Cog):
    """"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def sondage_multiple(self, ctx, *args):
        emoji_number = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣", "9️⃣"]
        args = list(args)
        try:
            number_ans = int(args[0])
        except ValueError:
            await ctx.send(
                "Trop peut d'arguments : \n"
                "    !sondage_multiple nombre_de_réponses question",delete_after=ERROR_DELAY*4)
            await ctx.message.delete(delay=ERROR_DELAY*4)
            return
        del args[0]

        msg=""
        for str in args:
            msg+=str+" "
        embed = Embed(title="Sondage",description=msg)

        embed = Embed(title="Sondage",description=msg)
        the_message = await ctx.send(embed=embed)
        await ctx.message.delete()
        for i in range(0, number_ans):
            await the_message.add_reaction(emoji_number[i])

    @commands.command()
    @commands.guild_only()
    async def sondage(self, ctx, *args):
        msg=""
        for str in args:
            msg+=str+" "
        embed = Embed(title="Sondage",description=msg)
        the_message = await ctx.send(embed=embed)
        await ctx.message.delete()

        await the_message.add_reaction("\U0001f7e2")
        await the_message.add_reaction("\U0001f534")

def setup(client):
    client.add_cog(Utils(client))
