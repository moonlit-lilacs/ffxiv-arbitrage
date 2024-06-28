import requests
import json
import re
import time


#priceBuilder takes in a jsonObject given to us by the Universalis API and turns it into a dictionary which gives us each item, its
#average price, its total cost, and its quantity. We may want to do more manipulation of the data in the future, in which case we can
#revisit this and add some more data in. Because each GET request to Universalis is limited to a maximum of one World (or datacenter,
#but we'll explore that later), we can let the main program handle adding this dictionary as the value to the key of the world name, letting
#us traverse a master dictionary to compare prices. If it's organized more easily to query a data-center, we'll consider that.
def priceBuilder(jsonObject):
    priceDict = {}
    keys = list(jsonObject.keys())
    if (keys[0] == "items"):
        for item_id, item in jsonObject['items'].items():
            units = 0
            cost = 0
            for listing in item['listings']:
                units += listing['quantity']
                cost += listing['quantity']*listing['pricePerUnit']+listing['tax']
            priceDict[item_id] = {"quantity" : units, "cost" : cost, "avgCost" : cost/units}
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

    return priceBuilder(data)

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


def main():

    masterDict = {}
    worlds = ["Faerie","Cactuar","Gilgamesh","Adamantoise"]
    items = ["5367", "5368", "5373"]
    for world in worlds:
        time.sleep(1)
        masterDict[world] = buildWorld(world, items)
        time.sleep(1)
    
    with open("test.json", 'w') as file:
        json.dump(masterDict, file, indent=4)



    return

if __name__ == "__main__":
    main()