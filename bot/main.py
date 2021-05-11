import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import func

load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")
MONGOURL = os.getenv("MONGO_URL")

cluster = MongoClient(MONGOURL)
db = cluster["DiscordData"]
collection = db["UserData"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild.me.permissions_in(message.channel).read_messages:
        return
    if not message.guild.me.permissions_in(message.channel).send_messages:
        return
    
    if message.content == '$roll_event':
        myquery = {"_id": message.author.id}
        if(collection.count_documents(myquery) == 0):
            post = {"_id": message.author.id, "name": message.author.name, "eventRoll": [{"r": 0, "rStar":"NA", "rName": "", "rUrl": ""}], "eiRoll": 0, "normalRoll": 0, "event4Pity": 0, "ei4Pity": 0, "normal4Pity": 0, "event5Pity": 0, "ei5Pity": 0, "normal5Pity": 0, "eventPromo": 0, }
            collection.insert_one(post)
        
        user = collection.find(myquery)
        tData = await func.rollEvent(user[0])
        collection.update_one({"_id": tData["_id"]}, {"$set": {"eventRoll": tData["eventRoll"], "event4Pity": tData["event4Pity"], "event5Pity":tData["event5Pity"]}})

        rTitle = "You rolled a " + tData["eventRoll"][-1]["rStar"] + " star"
        embed = discord.Embed(title=rTitle, color=discord.Color.purple())
        embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
        if tData["eventRoll"][-1]["rUrl"] != "":
            embed.set_image(url=tData["eventRoll"][-1]["rUrl"])
        embed.set_footer(text="Roll #" + str(tData["eventRoll"][-1]["r"]))
        await message.channel.send(embed=embed)

    if message.content == '$re10':
        myquery = {"_id": message.author.id}
        if(collection.count_documents(myquery) == 0):
            post = {"_id": message.author.id, "name": message.author.name, "eventRoll": [{"r": 0, "rStar":"NA", "rName": "", "rUrl": ""}], "eiRoll": 0, "normalRoll": 0, "event4Pity": 0, "ei4Pity": 0, "normal4Pity": 0, "event5Pity": 0, "ei5Pity": 0, "normal5Pity": 0, "eventPromo": 0, }
            collection.insert_one(post)
        
        user = collection.find(myquery)
        embed = discord.Embed(title="Making 10 wishes", color=discord.Color.orange())
        embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
        for i in range(0,10):
            tData = await func.rollEvent(user[0])
            collection.update_one({"_id": tData["_id"]}, {"$set": {"eventRoll": tData["eventRoll"], "event4Pity": tData["event4Pity"], "event5Pity":tData["event5Pity"]}})
            embed.add_field(name="Roll " + str(tData["eventRoll"][-1]["r"]) +": ", value= tData["eventRoll"][-1]["rName"], inline=False)
        await message.channel.send(embed=embed)

    if message.content == '$list_event':
        myquery = {"_id": message.author.id}
        if(collection.count_documents(myquery) == 0):
            await message.channel.send("You haven't rolled yet")
        else:
            user = collection.find(myquery)
            embed = discord.Embed(title="Listing 4 and 5 star event rolls", color=discord.Color.red())
            embed.set_author(name=message.author.name, icon_url = message.author.avatar_url)
            for roll in user[0]["eventRoll"]:
                if(roll["rStar"] == "four" or roll["rStar"] == "five"):
                    embed.add_field(name="Roll " + str(roll["r"]) +": ", value=roll["rName"], inline=False)
            await message.channel.send(embed=embed)
    
    if message.content == '$info':
        embed = discord.Embed(title="List of commands", color=discord.Color.green())
        embed.add_field(name="$roll_event", value="Roll once on the event banner", inline=False)
        embed.add_field(name="$list_event", value="List 4 and 5 star rolls from event banner", inline = False)
        await message.channel.send(embed = embed)
    
    
client.run(TOKEN)