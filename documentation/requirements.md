# Software Requirements Specification
## Purpose
A simple detective game where at the start of each new game, a new murder mystery scenario is procedurally generated and the player has to deduce who the murderer is by interrogating NPC characters.
## UI Plan
The game will have two main UIs: The main menu and the game UI itself (detailed below). The game UI will also have a few submenus.
<img src="raw.githubusercontent.com/veloxization/ot-harjoitustyo/master/documentation/images/gameUI.png">
## Basic functionality
### Main Menu
* New Game
  * Creates a new scenario
* Load Game
  * The player can continue a previously started unfinished scenario
* High Scores (possibly)
  * Details the player's performance in previously completed games
* Quit Game
  * Exits the game
### Game Menu
* Map
  * Details the map to give the player a reference to the events
* Floor
  * The currently selected floor
  * Can be used to cycle between floors
* Interrogating
  * Has a small menu the player can use to select an NPC to interrogate
* Question
  * The player can select a question base and fill in the blanks to ask qustions from the NPC being interrogated
  * The NPC will answer based on their knowledge and traits, answers are saved to Notes
* Notes
  * Opens a submenu
  * Saves everything the player has asked the NPCs for later reference
* Accuse
  * Opens a submenu
  * Allows the player to suggest their main suspect and time of murder
  * If the player makes the correct accusation, points will possibly be awarded based on the amount of questions asked so far etc.
* Save Game
  * Saves the game in its current state
* Exit Game
  * Moves the player back to the main menu
