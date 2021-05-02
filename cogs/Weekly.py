import discord
from discord.ext import commands
from discord.ext import tasks
import os
from dotenv import load_dotenv
import pymongo
import re
import time

class Weekly(commands.Cog):
    '''Weekly Event Scheduler!  '''

    def __init__(self, bot):
        self.bot = bot  

        #load database
        load_dotenv()
        self.DBCRED = os.environ.get("DBCRED")
        self.database = pymongo.MongoClient(self.DBCRED)["ruhacks"]
        self.userweeklyevents = self.database["userweeklyevents"]


    @commands.command()
    async def addweekly(self, ctx, day, time,  *,info = None):
        '''
        new_weekly_event = {
                    "userID" : ctx.message.author.id,
                    "event_time" : arg1.upper(),
                    "event_day" : arg2,
                    "event_details" : args
                }
        '''
        embed=discord.Embed(color=0xf3c4ea)
        embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")

        dates = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        #CHECK VALID DATE AND TIME
        if (day.lower().capitalize() in dates) and bool(re.match("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", time)):

            #CHECK TIME FORMAT
            new_weekly_event = {
                    "userID" : ctx.message.author.id,
                    "event_day" : day.lower().capitalize(),
                    "event_time" : time,
                    "event_details" : info if info is not None else "n/a"
            }
            self.userweeklyevents.insert_one(new_weekly_event)
            embed.add_field(name=f"New event on {day.lower().capitalize()} @ {time}", value=f"```{info} ```")
              
        else:
            embed.add_field(name = "Invalid Format", value = "```The input should be <DAY OF WEEK> <HH:MM> <EVENT DETAILS> \n ie. -addweeklyevent Tuesday 20:20 Math Lecture```")
        
        await ctx.send(embed = embed)


    @commands.command()
    async def listweekly(self, ctx):
        user_events = list(self.userweeklyevents.find({"userID" : ctx.message.author.id}, { "_id": 0 , "userID" : 0}))

        embed=discord.Embed(title = "Your Weekly Schedule!", color=0xf3c4ea)
        embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")

        dates = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        for day in dates:
            embed_field = ""
            for event in user_events:

                if (event["event_day"] == day):
                    details = event["event_details"]
                    time = event["event_time"]

                    embed_field += (f"\n -------| {time} |------- \n {details}")
            
            if (embed_field != ""):
                embed.add_field(name = day, value= f"```{embed_field}```", inline= False)
        
        await ctx.send(f"<@{ctx.message.author.id}>")
        await ctx.send(embed = embed)

    @commands.command()
    async def deleteweekly(self, ctx, date, time):
        #arg 1 is date arg 2 is time
        dates = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        embed=discord.Embed(color=0xf3c4ea)
        embed.set_author(name="Scheduler Bot | Created for RUHacks 2021", icon_url="https://shotatlife.org/wp-content/uploads/2018/07/google-calendar-icon-png.png")


        #CHECK VALID DATE AND TIME
        if (date.lower().capitalize() in dates) and bool(re.match("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]", time)):

            weekly_event_search = {
                    "userID" : ctx.message.author.id ,
                    "event_day" : date.lower().capitalize(),
                    "event_time" : time
                    }

            if (self.userweeklyevents.count_documents(weekly_event_search, limit = 1)) != 0:
                self.userweeklyevents.delete_one(weekly_event_search)
                embed.add_field(name = "Event was Removed", value = f"```{date.lower().capitalize()} @ {time}```")

            else:
                 embed.add_field(name = "Event could not be found", value = f"```{date.lower().capitalize()} @ {time}```")

        else:
            embed.add_field(name = "Invalid Format", value = "```The input should be <DAY OF WEEK> <HH:MM> \n ie. -deleteweeklyevent Tuesday 20:20 ```")

        await ctx.send(embed=embed)

    @commands.command()
    async def removeallweekly(self, ctx):
        if (self.userweeklyevents.count_documents({"userID": ctx.message.author.id})) != 0:
            self.userweeklyevents.delete_many({"userID" : ctx.message.author.id})
            await ctx.send("All of your events have been deleted!")
        else:
            await ctx.send("You don't have any events to be deleted!")




def setup(bot):
    bot.add_cog(Weekly(bot))

