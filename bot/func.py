import random
import json
with open("./bot/bannerData.json") as f:
    data = json.load(f)
ebanner = data["eventBanner"]

def get4(data):
    temp = []
    for item in data:
        if(item["star"] == 4):
            temp.append(item)
    return temp

def get5(data):
    temp = []
    for item in data:
        if(item["star"] == 5):
            temp.append(item)
    return temp

def getC(data):
    temp = []
    for item in data:
        if(item["type"] == 'character'):
            temp.append(item)
    return temp

def getW(data):
    temp = []
    for item in data:
        if(item["type"] == 'weapon'):
            temp.append(item)
    return temp

def choose5(data):
    items = get5(data)
    if random.random() < 0.5:
        for item in items:
            if item["up"]:
                return item
    else:
        return random.choice(items)

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
    item = {}

    if(e5Pity == 90):
        item = choose5(ebanner)
        e5Pity = 0
        e4Pity = 0
    elif(e4Pity == 10):
        x = random.choices([4,5], weights=[994, 6])
        if x[0] == 4:
            if random.random() < 0.5:
                item = getC(ebanner)
            else:
                item = getW(ebanner)
            item = choose4(item)
        else:
            item = choose5(ebanner)
        e4Pity = 0
    else:
        x = random.choices([3, 4, 5], weights=[943, 51, 6])
        if x[0] == 5:
            item = choose5(ebanner)
            e5Pity = 0
            e4Pity = 0
        elif x[0] == 4:
            if random.random() < 0.5:
                item = getC(ebanner)
            else:
                item = getW(ebanner)
            item = choose4(item)
            e4Pity = 0
            
    tData["event5Pity"] = e5Pity
    tData["event4Pity"] = e4Pity
    if(item):
        tData["eventRoll"].append({"r": eRoll, "star": item["star"], "name": item["name"], "imgUrl": item["imgUrl"], "type": item["type"]})
    else:
        tData["eventRoll"].append({"r": eRoll, "star": 3, "name": "3 star", "imgUrl": "", "type": "weapon"})

    return tData
