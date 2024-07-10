import requests
import json
import re
import time
import tkinter as tk
from tkinter import ttk

#A simply dictionary caching which servers are in which data center for use later.

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

    root.mainFrame = ttk.Frame(root,padding="10")
    root.mainFrame.grid(row=0,column=0,sticky="nsew")

    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)

    root.leftFrame = ttk.Frame(root.mainFrame,padding="10")
    root.leftFrame.grid(row=0,column=0,sticky="n")

    root.rightFrame = ttk.Frame(root.mainFrame,padding="10")
    root.rightFrame.grid(row=0,column=1,sticky="nsew")

    root.mainFrame.grid_rowconfigure(0,weight=1)
    root.mainFrame.grid_columnconfigure(1,weight=1)

        

    label = ttk.Label(root.leftFrame, text="Select Data Center")
    label.grid(row=0,column=0,pady=10,sticky="ew")
    dataCenter = tk.StringVar()
    root.dataCenters = ttk.Combobox(root.leftFrame, textvariable=dataCenter)
    root.dataCenters['values'] = ("Aether", "Crystal", "Dynamis", "Primal", "Chaos", "Light","Shadow","Materia","Elemental","Gaia","Mana","Meteor")
    root.dataCenters.grid(row=1,column=0,pady=10,sticky="ew")
    root.dataCenters.current()

    server = tk.StringVar()
    root.servers = ttk.Combobox(root.leftFrame, textvariable=server)
    root.servers.grid(row=2,column=0,pady=10,sticky="ew")

    def updateServers(event):
            global previousSelection
            selectedValue = root.dataCenters.current()
            values = []

            #To prevent de-selecting homeworld when you switch from a data center to the same
            #data center, we check if our results actually differ before we do any work.
            if selectedValue != previousSelection:
                match selectedValue:
                    case 0:
                        values = dcServerDict['Aether']
                    case 1:
                        values = dcServerDict['Crystal']
                    case 2:
                        values = dcServerDict['Dynamis']
                    case 3:
                        values = dcServerDict['Primal']
                    case 4:
                        values = dcServerDict['Chaos']
                    case 5:
                        values = dcServerDict['Light']
                    case 6:
                        values = dcServerDict['Shadow']
                    case 7:
                        values = dcServerDict['Materia']
                    case 8:
                        values = dcServerDict['Elemental']
                    case 9:
                        values = dcServerDict['Gaia']
                    case 10:
                        values = dcServerDict['Mana']
                    case 11:
                        values = dcServerDict['Meteor']

                #Sets the servers available from the data center, clears the homeworld, and sets
                #our selection as the previous selection so we don't clear if we select the same
                #thing again.
                root.servers['values'] = values
                root.servers.set('')
                previousSelection = selectedValue

    #When we select an option, update the servers available.
    root.dataCenters.bind("<<ComboboxSelected>>", updateServers)

    def closeComboboxDropdown(event):
        #On focus loss, we check if our focus is on our two comboboxes. If it is, we
        #ignore it and return without doing anything. If it isn't, we generate an escape event
        #to close the dropdown menus. This is buggy on windows and in some ways on Unix systems,
        #but I'll come back to polish it later.
        try:
            if (root.focus_get() != root.dataCenters) and (root.focus_get() != root.servers):    
                root.dataCenters.event_generate('<Escape>')
                root.servers.event_generate('<Escape>')
        
        #We have to ignore keyerrors here because the comboboxes' popdown arrow throws errors for 
        #the focus_get() function. However, this only happens for those popdown arrows and in that
        #case, we don't want anything to happen anyway, so we can safely ignore it.
        except KeyError:
            return


    #Close the dropdown when we're not focusing on the application, getting rid of the annoying
    #menu artefacts.
    root.bind("<FocusOut>", closeComboboxDropdown)


    items = tk.StringVar()
    itemBox = ttk.Entry(root.leftFrame, textvariable=items)
    itemBox.grid(row=3,column=0,pady=10,sticky="ew")

    arbitButton = ttk.Button(root.leftFrame, text="Execute")
    arbitButton.grid(row=4,column=0,pady=10,sticky="ew")

    def on_button_click():
        if((not root.dataCenters.get()) or (not server.get()) or (not itemBox.get())):
            return
        worlds = dcServerDict[root.dataCenters.get()]
        homeWorld = server.get()
        selectedItems = itemBox.get()
        print(f"Worlds to query: {worlds}")
        url = "https://universalis.app/api/v2/" + homeWorld + "/" + selectedItems + "?listings=5&entries=0&fields=items.listings.pricePerUnit,items.listings.quantity,items.listings.tax,items.listings.total"
        print(url)
        print(f"Selected homeworld: {homeWorld}")
        return

    arbitButton.config(command=on_button_click)

    placeHolder = ttk.Label(root.rightFrame, text="Test")
    placeHolder.grid(row=0,column=0,sticky="nsew")

    root.rightFrame.grid_rowconfigure(0, weight=1)
    root.rightFrame.grid_columnconfigure(0,weight=1)


    
    root.mainloop()
    return

if __name__ == "__main__":
    main()