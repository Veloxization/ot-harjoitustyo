# Relation of the core classes
<img src="https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/images/diagram.png">

# The core functionality
At the core of the game lies the ScenarioGenerator class. The scenario generator creates the details the player has to look through during gameplay. Utilising the _Time_, _Room_ and _NPC_ classes as well as Python's pseudorandom number generation, the scenario generator determines where rooms are located in relation to each other, how NPCs act throughout the night and how they will respond to the player's questions when interrogated. Below is the sequence diagram of the function of the ScenarioGenerator class when initialised.
<img src="https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/images/sequence.png">
The actual function is a lot more extensive than can be displayed in an image without making it look very confusing. It's also largely dependent on the seed and difficulty it's given.

# User interface
The user interface can be divided into three parts:
- The main menu
- The intro sequence
- The game scene

## Main menu
The main menu is created as its own class and has two submenus: New game and load game. There is also an option to shut down the process in the "Quit Game" option.

## Intro sequence
The intro sequence is only displayed when the player starts a new game. It details the scenario the player got from the specified seed and difficulty.

## Game scene
The game scene consists of the main scene as well as multiple submenus including the saving menu and the accusation menu. The actual gameplay happens inside this scene.

# Saving
The Save class handles saving the player's data, just in case they want to return to a scenario they started but were unable to finish. The Save class takes the scenario's seed and difficulty, as well as the notes the player has collected, and creates a base64 encoded JSON file that saves all this data.

All the Save class has to do to return the player to where they were is create a new scenario with the same seed and difficulty as specified in the save file, and return the notes to the state they were in at the time of saving. Due to the pseudorandom nature of Python's random library, giving it the same variables to work with will always produce the same results.
