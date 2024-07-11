# FFXIV Arbitrage

This is a simple project based off of a proof of concept that I had developed a couple years ago having to do with automatically calculating arbitrage opportunities between different servers by querying the API of a popular price aggregator for FFXIV for a user-defined selection of items. The script would query and compare the prices across different servers to the designated "home" server and determine if an arbitrage opportunity was possible. If so, it would display the results as well as how much could be made

Note: Because this is utilizing a third party website whose server hosting costs I am *not* paying for, and because this is explicitly used for the purpose of educating myself, there is built-in inefficiency to target a "one request per second" goal (far below the 25req/s limit on their website) for the express purpose of causing as little load as possible.


## Update (7/10/24)

The bulk of the functionality is now complete. There are a few things that I might want to tune up in the future (sorting by columns, refactoring code to be less spaghettified, adding in a debugger using that debug flag, more input validation, replacing the comboboxes with a more appropriate widget, etc.), but as the main purpose of this was educating myself and personal curiosity, I find that I may want to dedicate my time elsewhere in the pursuit of learning other things. For now I'll leave it be, though I don't rule out coming back to it another day.