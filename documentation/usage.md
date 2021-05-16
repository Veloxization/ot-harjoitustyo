# Usage
## Manual
### How to Play
#### Main Menu
The _Main Menu_ gives you the following options: new game, load game, quit game
##### New Game
Selecting _New Game_ takes you to a new menu where you are given an option to enter a seed, and difficulty. _The seed_ is used for the generation logic of a new scenario. You can leave it empty for a random 32-bit signed integer to be used as the seed. You can read more about _the difficulty option_ in its own [section](#difficulties).
##### Load Game
Selecting _Load Game_ takes you to a new menu where you are given the option to continue a previously saved scenario. The dropdown menu will reveal any previously saved games, if any are available.
##### Quit Game
Selecting _Quit Game_ immediately closes the game.
### Goal
Interrogate NPCs and find out who the murderer is, and when they committed their crime!
### NPCs
The game has five NPC types: Normal, Murderer, Victim, Liar and Obsessive. You won't be told the identities of these NPCs apart from the victim so pay close attention to what the NPCs tell you when you interrogate them! The patterns will reveal their type!
#### Normal
Normal NPCs show no special behaviours. They will visit random rooms during the night.
#### Murderer
Only one will be generated for each scenario. A murderer NPC will act a lot like a normal NPC but will lie about where they were at the time of the murder. Try to catch them in their lie by finding a discrepancy in their story compared to what other NPCs tell you!
#### Victim
Only one will be generated for each scenario. A victim NPC will act a lot like a normal NPC but will eventually end up in the same room with only the murderer NPC and be left there until discovered by another NPC. Note that the murderer themselves can also report the body!
#### Liar
Only one will be generated for each scenario. A liar NPC will never tell you the truth about where they were and who they were with (with the exception of when they are accused of a crime they didn't commit). If you think you've found a discrepancy in someone's story, make sure you are not talking with a liar!
#### Obsessive
Only one will be generated for each scenario. An obsessive NPC will pick a random NPC to follow throughout the night. They will always be in an adjacent room and hence will always be able to tell where their obsession is, and with whom. They may have some really useful information if you get lucky...
### Difficulties
There are three difficulties: Easy, Normal and Hard.

A higher difficulty level means you will have more NPCs to interrogate and more floors unlocked, giving you a lot of information to shift through.
### Rooms
Rooms are accessed by NPCs throughout the night. You can ask an NPC about which room they were with the *"Where were you at \_\_:\_\_?"* question and they will answer based on their personality.

Each room has **adjacent rooms**, i.e. other rooms that can be directly accessed from that room. You can ask an NPC about where other NPCs were with the *"Where were they at \_\_:\_\_?"* question. If that other NPC was in the same or an adjacent room to the asked NPC, they will be able to tell (unless they're lying, of course).

Note that even though two rooms may share a wall, it doesn't necessarily mean they are adjacent rooms. The *Wine Cellar* in the basement is not connected to the *Laboratory*, and the *Kitchen* and the *Dining Room* on the ground floor are not connected to the *Office* and the *Bathroom* respectively despite being connected by a wall.
### Saving
You can save your progress at any time during gameplay by selecting the option. Saves are put in the `/src/data/saves` folder in base64 encoded JSON format. Saved files can be loaded to continue a previous investigation.
## Test
To run currently implemented tests, use `poetry run invoke test`
## Coverage Report
To generate a coverage report, use `poetry run invoke coverage-report`
A coverage report will be generated in terminal but a folder called *htmlcov* will also be created in the root directory. Within it, you will find *index.html*. Opening it in browser will show a more visually pleasing coverage report.
## Pylint
To run Pylint, use `poetry run invoke lint`
## Debug
Come across a scenario that seems impossible to solve? Save your game and use `poetry run invoke debug` to see information about the save, including the scenario's solution.
