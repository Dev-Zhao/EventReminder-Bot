import discord
from discord.ext import commands
import random
import pymongo
from pymongo import MongoClient
import os


# from replit import db

class Settings(commands.Cog):
    """ Bot Settings, including prefix changing"""

    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://scanbot:OSoKwu36c8x452bY@ruhacks.a7jye.mongodb.net/test")
        self.db = self.cluster["ruhacks"]
        self.prefixes = self.db["prefix"]

    # gets the prefix from database
    def get_prefix(self, client, message):
        post = self.prefixes.find_one({"_id": str(message.guild.id)})
        return post["prefix"]

    # events
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        post = {"_id": str(guild.id), "prefix": "."}
        self.prefixes.insert_one(post)

        general = guild.text_channels[0]
        if general and general.permissions_for(guild.me).send_messages:
            await general.send(
                f"``` Hello {guild.name}! \n I am your Event Reminder and you could use .help for a list of my commands! ```")

        print(f"Joined Guild {guild.name} - {guild.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.prefixes.delete_one({"_id": str(guild.id)})

    # commands

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix='-'):
        self.prefixes.update_one({"_id": str(ctx.message.guild.id)}, {"$set": {"prefix": prefix}})

        message = f"Prefix changed to {prefix}"
        print(message)
        await ctx.send(message)


def setup(client):
    client.add_cog(Settings(client))