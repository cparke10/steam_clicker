# steam_clicker
script environment for educational reasoning of JaGex's OSRS anti-botting methods

run_steams.py is a self-contained, hard-coded screen clicker that simply clicks on a set series 
of bounding boxes of the users screen to carry out a set of actions within the game world.
NOTE: the user character must be placed at an exact angle prior to executing run_steams.py, which the author
will not document.

First, it identifies the bank object on the user's screen to deposit the steam runes.
Then, it teleports to the Duel Arena, identifies the altar object on the user's screen and interacts with the altar.
Finally, it crafts the runes, teleports back to the banking area to start over.
This agent will automatically keep up to date with replenishing the correct stats to maintain the crafting process.
