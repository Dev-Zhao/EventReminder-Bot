import discord
from discord.ext import commands


class Settings(commands.Cog):
    """Bot settings"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = guild.text_channels[0]
        if general and general.permissions_for(guild.me).send_messages:
            msg = f"Hello {guild.name} ! \n I am your EventReminder! You could use -help for a list of my commands!"
            embed = discord.Embed(
                title = "Event Reminder",
                description= msg,
                color = discord.Color.purple()
            )
            await general.send("", embed = embed)

        print(f"Joined Guild {guild.name} - {guild.id}")


def setup(client):
    client.add_cog(Settings(client))