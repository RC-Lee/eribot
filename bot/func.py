import random
import json
with open("./bot/bannerData.json") as f:
    data = json.load(f)
ebanner = data["eventBanner"]

def get4(data):
    char = []
    for item in data:
        if(item["star"] == "four"):
            char.append(item)
    return char


def get5(data):
    char = []
    for item in data:
        if(item["star"] == "five"):
            char.append(item)
    return char


def choose5(data):
    char = get5(data)
    if random.random() < 0.5:
        for item in char:
            if item["up"]:
                return item
    else:
        return random.choice(char)


def choose4(data):
    items = get4(data)
    if random.random() < 0.5:
        upItems = []
        for item in items:
            if item["up"]:
                upItems.append(item)
        return random.choice(upItems)
    else:
        return random.choice(items)

async def rollEvent(userData):
    tData = userData
    eRoll = tData["eventRoll"][-1]["r"] + 1
    e5Pity = tData["event5Pity"] + 1
    e4Pity = tData["event4Pity"] + 1
    eventPromo = tData["eventPromo"]
    item = {}

    if(e5Pity == 90):
        rTitle = 'Roll: '+ str(eRoll) + ' Congrats you rolled a 5 star'
        item = choose5(ebanner)
        e5Pity = 0
        e4Pity = 0
        # collection.update_one({"_id": userData["_id"]}, {"$set": {"event5Pity": 0, "event4Pity": 0, "eventRoll": eRoll}})
    elif(e4Pity == 10):
        rTitle = 'Roll: '+ str(eRoll) + ' Congrats you rolled a 4 star'
        item = choose4(ebanner)
        e4Pity = 0
        # collection.update_one({"_id": message.author.id}, {"$set": {"event4Pity": 0, "eventRoll": eRoll}})
    else:
        from random import randint
        value = randint(1, 1000)
        if value <= 6:
            rTitle = 'Roll: '+ str(eRoll) + ' Congrats you rolled a 5 star'
            item = choose5(ebanner)
            e5Pity = 0
            e4Pity = 0
            # collection.update_one({"_id": message.author.id}, {"$set": {"event5Pity": 0, "event4Pity": 0, "eventRoll": eRoll}})
        elif value <= 57:
            item = choose4(ebanner)
            rTitle = 'Roll: '+ str(eRoll) + ' Congrats you rolled a 4 star'
            e4Pity = 0
            # collection.update_one({"_id": message.author.id}, {"$set": {"event4Pity": 0, "eventRoll": eRoll}})
        else:
            rTitle = 'Roll: '+ str(eRoll) + ' Boo you rolled a 3 star'
            # collection.update_one({"_id": message.author.id}, {"$set": {"event5Pity": e5Pity, "event4Pity": e4Pity, "eventRoll": eRoll}})
    tData["event5Pity"] = e5Pity
    tData["event4Pity"] = e4Pity
    if(item):
        tData["eventRoll"].append({"r": eRoll, "rStar": item["star"], "rName": item["name"], "rUrl": item["imgUrl"]})
    else:
        tData["eventRoll"].append({"r": eRoll, "rStar": "three", "rName": "3 star", "rUrl": ""})

    return tData
