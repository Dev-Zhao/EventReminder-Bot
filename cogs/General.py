import discord
from discord.ext import commands


class General(commands.Cog):
    """General commands that respond with a message"""
    def __init__(self, client):
        self.client = client

    #commands
    @commands.command(aliases = ['hi'])
    async def hello(self, ctx):
        await ctx.send("Hello, I am your Event Reminder!")


def setup(client):
    client.add_cog(General(client))

