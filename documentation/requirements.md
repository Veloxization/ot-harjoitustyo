# Software Requirements Specification
## Purpose
A simple detective game where at the start of each new game, a new murder mystery scenario is procedurally generated and the player has to deduce who the murderer is by interrogating NPC characters.
## UI Plan
The game will have two main UIs: The main menu **(DONE!)** and the game UI itself (detailed below). The game UI will also have a few submenus. **(DONE!)**
<img src="https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/images/gameUI.png">
## Basic functionality
### Main Menu
* New Game
  * Creates a new scenario **(DONE!)**
* Load Game
  * The player can continue a previously started unfinished scenario **(DONE!)**
* Quit Game
  * Exits the game **(DONE!)**
### Game Menu
* Map
  * Details the map to give the player a reference to the events **(DONE!)**
* Floor
  * The currently selected floor **(DONE!)**
  * Can be used to cycle between floors **(DONE!)**
* Interrogating
  * Has a small menu the player can use to select an NPC to interrogate **(DONE!)**
* Question
  * The player can select a question base and fill in the blanks to ask questions from the NPC being interrogated **(DONE!)**
  * The NPC will answer based on their knowledge and traits **(DONE!)**, answers are saved to Notes **(DONE!)**
* Notes
  * Opens a submenu **(DONE!)**
  * Saves everything the player has asked the NPCs for later reference **(DONE!)**
* Accuse
  * Opens a submenu **(DONE!)**
  * Allows the player to suggest their main suspect and time of murder **(DONE!)**
  * If the player makes the correct accusation, the game will end with a win condition. **(DONE!)**
* Save Game
  * Saves the game in its current state **(DONE!)**
* Exit Game
  * Moves the player back to the main menu **(DONE!)**
