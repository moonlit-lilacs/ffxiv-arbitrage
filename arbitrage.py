import requests
import json
import re
import time


#priceBuilder takes in a jsonObject given to us by the Universalis API and turns it into a dictionary which gives us each item, its
#average price, its total cost, and its quantity. We may want to do more manipulation of the data in the future, in which case we can
#revisit this and add some more data in. Because each GET request to Universalis is limited to a maximum of one World (or datacenter,
#but we'll explore that later), we can let the main program handle adding this dictionary as the value to the key of the world name, letting
#us traverse a master dictionary to compare prices. If it's organized more easily to query a data-center, we'll consider that.
def priceBuilder(jsonObject, items):
    priceDict = {}
    keys = list(jsonObject.keys())
    if (keys[0] == "items"):
        for item in items:
            if not item in jsonObject['items']:
                priceDict[item] = {"quantity" : 0, "cost" : 0, "avgCost" : 0}
        for item_id, item in jsonObject['items'].items():
            units = 0
            cost = 0
            if(len(item['listings']) == 0):
                priceDict[item_id] = {"quantity" : 0, "cost" : 0, "avgCost" : 0}
            for listing in item['listings']:
                units += listing['quantity']
                cost += listing['quantity']*listing['pricePerUnit']+listing['tax']
            if (units > 0):
                priceDict[item_id] = {"quantity" : units, "cost" : cost, "avgCost" : cost/units}
            else:
                priceDict[item_id] = {"quantity" : 0, "cost" : 0, "avgCost" : 0}
    else:
        units = 0
        cost = 0
        for listing in jsonObject['listings']:
            units += listing['quantity']
            cost += listing['quantity']*listing['pricePerUnit']+listing['tax']
        priceDict[item_id] = {"quantity" : units, "cost" : cost, "avgCost" : cost/units}
    return priceDict

def buildWorld(world, items):
    baseURL = "https://universalis.app/api/v2/"

    usrItems = ','.join(items)

    url = baseURL + world + "/" + usrItems + "?listings=5&entries=0&fields=items.listings.pricePerUnit,items.listings.quantity,items.listings.tax,items.listings.total"

    try:
        response = requests.get(url = url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error {e}")
    except json.JSONDecodeError as e:
        print(f"Request error {e}")

    return priceBuilder(data, items)

def get_user_int(prompt, default_value=-1):
    while True:
        inp = input(prompt)
    
        if (inp == '') and (default_value != -1):
            return default_value
        try:
            value = int(inp)
            return value
        except ValueError:
            print("Not an integer")

def arbitrage(dict, items, homeWorld):
    arbit = {}
    for item in items:
        data = []
        homeItemCost = float(dict[homeWorld][item]['avgCost'])
        if homeItemCost == 0:
            pass
        for world in dict:
            if world == homeWorld:
                pass
            else:
                worldItemCost = float(dict[world][item]['avgCost'])
                if (worldItemCost) == 0:
                    continue
                if worldItemCost < homeItemCost:
                    profit = homeItemCost-worldItemCost
                    #print(f"Found {item} in {world} where {item} costs {dict[world][item]['avgCost']} on {world} and {str(homeItemCost)} on {homeWorld}, for an arbitrage of {str(profit)}")
                    data.append((world, worldItemCost, profit))
        arbit[item] = sorted(data, key=lambda x : x[2])
    return arbit


def main():
    masterDict = {}
    worlds = ["Seraph","Kraken","Cuchulainn","Halicarnassus", "Maduin"]
    items = ["5367", "5368", "5373", "5380", "5381", "5383", "5384", "5385", "5386", "5387", "5388", "5389", "5390", "5391", "5392", "5393", "5394"]
    homeWorld = "Seraph"


    for world in worlds:
        time.sleep(1)
        masterDict[world] = buildWorld(world, items)
        time.sleep(1)
    
    with open("test.json", 'w') as file:
        json.dump(masterDict, file, indent=4)

    # with open("test.json", 'r') as file:
    #     masterDict = json.load(file)



    arbit = arbitrage(masterDict, items, homeWorld)

    for key in arbit:
        print(f"{key} was found on following worlds for cheaper prices than on {homeWorld}: \n", end='')
        for instance in arbit[key]:
            world = instance[0]
            cost = instance[1]
            profit = instance[2]
            print(f"\t{world}: {cost}, profit +{profit}")
        print("---------------------------------------------\n", end='')

    return

if __name__ == "__main__":
    main()