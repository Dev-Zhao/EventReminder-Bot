import discord
from discord.ext import commands


class GoogleAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

    #commands
    @commands.command(aliases = ['import'])
    async def importFromGoogle(self, ctx):
        await ctx.send("Hello, I am your Event Reminder!")


def setup(client):
    client.add_cog(GoogleAPI(client))