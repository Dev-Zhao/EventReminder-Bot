import discord
from discord.ext import commands
import os

if __name__ == '__main__':

    token = os.getenv("DISCORD_TOKEN")

    if token is None:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.environ.get("DISCORD_TOKEN")


    client = commands.Bot(command_prefix= "+")
    client.remove_command('help')

    @client.event
    async def on_ready():
        members = 0
        for guild in client.guilds:
            members += guild.member_count
        await client.change_presence(status=discord.Status.online,
                                     activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=f"{members} users!"))
        print("Event reminder is ready!")


    @client.command()
    async def load(ctx, extension):
        client.load_extension(f"cogs.{extension}")


    @client.command()
    async def unload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")

        #reload comamnd
    @client.command()
    @commands.is_owner()
    async def reload(ctx, cog):
        try:
            client.reload_extension(f"cogs.{cog}")
            await ctx.send(f"The extension cogs.{cog} was reloaded")
        except:
            await ctx.send(f"The extension cogs.{cog} could not be reloaded or does not exist")


    print("-------------------")
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                client.load_extension(f"cogs.{cog[:-3]}")
                print(f"{cog} Loaded!")
            except Exception as e:
                print(f"{cog} cannot be loaded:")
                raise e
    print("-------------------")

    client.run(token)

