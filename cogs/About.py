import discord
from discord.ext import commands


class About(commands.Cog):
    """Bot Information"""

    def __init__(self, client):
        self.client = client

    # commands
    @commands.command()
    async def info(self, ctx):
        command_prefix = "-"
        await ctx.send(f"``` I'm a bot created for RUHacks2021 by xxsuka#7765, 100bandz#6828, aco#1225, charr#2956 !\n Server count: {len(self.client.guilds)}\n use {command_prefix}help to get help on the different bot categories and commands! ```")

    @commands.command(aliases = ['chad'])
    @commands.has_permissions(embed_links=True)
    async def help(self, ctx, query=None):
        command_prefix = "-"
        cogs_list = [c.capitalize() for c in self.client.cogs]
        cogs_desc = ""
        commands_desc = ""
        private_cogs = []
        embed = ""
        if query is None:
            for cog in self.client.cogs:
                if cog not in private_cogs:
                    cogs_desc += f"`{cog}` - {self.client.cogs[cog].__doc__}\n"

            embed = discord.Embed(
                title="EventReminder Help",
                description=f"These are all the command categories!\n Type {command_prefix}help [category] to get the list of commands from each category",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="categories",
                value=cogs_desc,
                inline=False
            )
        else:
            if query.capitalize() in cogs_list:
                cog_commands = self.client.get_cog(query.capitalize()).get_commands()
                for com in cog_commands:
                  aliases_desc = ""
                  com_desc = com.name
                  for param in com.clean_params:
                    com_desc += f" <{param}>"
                  for alias in com.aliases:
                    aliases_desc += alias
                  if aliases_desc == "":
                    commands_desc += f"{command_prefix}{com_desc}\n"
                  else:
                    commands_desc += f"{command_prefix}{com_desc} - Aliases: {aliases_desc}\n"
                embed = discord.Embed(
                    title="EventReminder Help",
                    description=f"These are all the commands for category {query}!\n",
                    color=discord.Color.blue()
                )

                embed.add_field(
                    name="Commands",
                    value=commands_desc,
                    inline=False
                )
            else:
                await ctx.send("Category not available!")
        await ctx.send("", embed=embed)


def setup(client):
    client.add_cog(About(client))
