import requests
import json
import re
import time
import tkinter as tk
from tkinter import ttk


dcServerDict = {
    "Aether" : ["Adamantoise", "Cactuar", "Faerie", "Gilgamesh", "Jenova", "Midgardsormr", "Sargantanas", "Siren"],
    "Crystal" : ["Balmung", "Brynhildr", "Coeurl", "Diabolos", "Goblin", "Malboro", "Mateus", "Zalera"],
    "Dynamis": ["Cuchulainn", "Golem", "Halicarnassus", "Kraken", "Maduin", "Marilith", "Rafflesia", "Seraph"],
    "Primal" : ["Behemoth", "Excalibur", "Exodus", "Famfrit", "Hyperion", "Lamia", "Leviathan", "Ultros"],
    "Chaos" : ["Cerberus", "Louisoix", "Moogle", "Omega", "Phantom", "Ragnarok", "Sagittarius", "Spriggan"],
    "Light" : ["Alpha", "Lich", "Odin", "Phoenix", "Raiden", "Shiva", "Twintania", "Zodiark"],
    "Shadow" : ["Innocence", "Pixie", "Titania", "Tycoon"],
    "Materia" : ["Bismarck", "Ravana", "Sephirot", "Sophia", "Zurvan"],
    "Elemental" : ["Aegis", "Atomos", "Carbuncle", "Garuda","Gungnir","Kujata","Tonberry","Typhon"],
    "Gaia" : ["Aexander", "Bahamut", "Durandal","Fenrir","Ifrit","Ridill","Tiamat","Ultima"],
    "Mana" : ["Anima","Asura","Chocobo","Hades","Ixion","Masamune","Pandaemonium","Titan"],
    "Meteor" : ["Belias", "Mandragora","Ramuh","Shinryu","Unicorn","Valefor","Yojimbo","Zeromus"]
}


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

previousSelection = -1





def main():
    masterDict = {}
    worlds = ["Seraph","Kraken","Cuchulainn","Halicarnassus", "Maduin"]
    items = ["5367", "5368", "5373", "5380", "5381", "5383", "5384", "5385", "5386", "5387", "5388", "5389", "5390", "5391", "5392", "5393", "5394"]
    homeWorld = "Seraph"


    # for world in worlds:
    #     time.sleep(1)
    #     masterDict[world] = buildWorld(world, items)
    #     time.sleep(1)
    
    # with open("test.json", 'w') as file:
    #     json.dump(masterDict, file, indent=4)

    with open("test.json", 'r') as file:
        masterDict = json.load(file)



    arbit = arbitrage(masterDict, items, homeWorld)

    # for key in arbit:
    #     print(f"{key} was found on following worlds for cheaper prices than on {homeWorld}: \n", end='')
    #     for instance in arbit[key]:
    #         world = instance[0]
    #         cost = instance[1]
    #         profit = instance[2]
    #         print(f"\t{world}: {cost}, profit +{profit}")
    #     print("---------------------------------------------\n", end='')


    root = tk.Tk()

    root.title("FFXIV Arbitrage Tool")
    root.geometry("800x800")


    root.style = ttk.Style()
    root.style.theme_use('clam')

    root.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
    root.style.configure("TButton", background="#444444", foreground="#ffffff")
    root.style.configure("TEntry", fieldbackground="#2e2e2e", foreground="#ffffff")
    root.style.configure("TFrame", background="#2e2e2e")
    root.style.map("TButton",
          background=[("active", "#666666"), ("pressed", "#444444")])

    root.frame = ttk.Frame(root,padding="10")
    root.frame.pack(fill=tk.BOTH,expand=True)

    label = ttk.Label(root.frame, text="Select Data Center")
    label.pack(pady=2)
    dataCenter = tk.StringVar()
    root.dataCenters = ttk.Combobox(root.frame, width=27, textvariable=dataCenter)
    root.dataCenters['values'] = ("Aether", "Crystal", "Dynamis", "Primal", "Chaos", "Light","Shadow","Materia","Elemental","Gaia","Mana","Meteor")
    root.dataCenters.pack(pady=10)
    root.dataCenters.current()

    server = tk.StringVar()
    root.servers = ttk.Combobox(root.frame, width=27, textvariable=server)
    root.servers.pack(pady=10)

    def updateServers(event):
            global previousSelection

            selectedValue = root.dataCenters.current()
            values = []

            if selectedValue != previousSelection:
                match selectedValue:
                    case 0:
                        values = ["Adamantoise", "Cactuar", "Faerie", "Gilgamesh", "Jenova", "Midgardsormr", "Sargantanas", "Siren"]
                    case 1:
                        values = ["Balmung", "Brynhildr", "Coeurl", "Diabolos", "Goblin", "Malboro", "Mateus", "Zalera"]
                    case 2:
                        values = ["Cuchulainn", "Golem", "Halicarnassus", "Kraken", "Maduin", "Marilith", "Rafflesia", "Seraph"]
                    case 3:
                        values = ["Behemoth", "Excalibur", "Exodus", "Famfrit", "Hyperion", "Lamia", "Leviathan", "Ultros"]
                    case 4:
                        values = ["Cerberus", "Louisoix", "Moogle", "Omega", "Phantom", "Ragnarok", "Sagittarius", "Spriggan"]
                    case 5:
                        values = ["Alpha", "Lich", "Odin", "Phoenix", "Raiden", "Shiva", "Twintania", "Zodiark"]
                    case 6:
                        values = ["Innocence", "Pixie", "Titania", "Tycoon"]
                    case 7:
                        values = ["Bismarck", "Ravana", "Sephirot", "Sophia", "Zurvan"]
                    case 8:
                        values = ["Aegis", "Atomos", "Carbuncle", "Garuda","Gungnir","Kujata","Tonberry","Typhon"]
                    case 9:
                        values = ["Aexander", "Bahamut", "Durandal","Fenrir","Ifrit","Ridill","Tiamat","Ultima"]
                    case 10:
                        values = ["Anima","Asura","Chocobo","Hades","Ixion","Masamune","Pandaemonium","Titan"]
                    case 11:
                        values = ["Belias", "Mandragora","Ramuh","Shinryu","Unicorn","Valefor","Yojimbo","Zeromus"]

                root.servers['values'] = values
                root.servers.set('')
                previousSelection = selectedValue

    root.dataCenters.bind("<<ComboboxSelected>>", updateServers)

    def closeComboboxDropdown(event):
        if (root.focus_get() != root.dataCenters) and (root.focus_get() != root.servers):    
            print("closing combobox dropdowns...")
            root.dataCenters.event_generate('<Escape>')
            root.servers.event_generate('<Escape>')

    root.bind("<FocusOut>", closeComboboxDropdown)
    #root.bind("<Alt-Tab>", closeComboboxDropdown)


    items = tk.StringVar()
    itemBox = ttk.Entry(root.frame, textvariable=items)
    itemBox.pack(pady=10)

    arbitButton = ttk.Button(root.frame, text="Execute")
    arbitButton.pack(pady=10)

    def on_button_click():
        if((not root.dataCenters.get()) or (not server.get()) or (not itemBox.get())):
            return
        worlds = dcServerDict[root.dataCenters.get()]
        homeWorld = server.get()
        selectedItems = itemBox.get()
        print(f"Worlds: {worlds}")
        url = "https://universalis.app/api/v2/" + "/" + selectedItems + "?listings=5&entries=0&fields=items.listings.pricePerUnit,items.listings.quantity,items.listings.tax,items.listings.total"
        print(url)
        print(f"Selected homeworld: {homeWorld}")
        return


    
    arbitButton.config(command=on_button_click)



    
    root.mainloop()
    





    return

if __name__ == "__main__":
    main()