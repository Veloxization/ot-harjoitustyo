# README
## What is this?
This is a project repository for a uni course. It has the main project as well as other small assignments.
## What's the main project about?
The main project is a small scale detective game developed with Python. A murder mystery scenario is generated at the start of each game and the player can interrogate the NPCs about their actions throughout the night to deduce who the murderer is and when the murder was committed. Further details in [Requirements](https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/requirements.md).
**Note: The project will very likely have major bugs at current time! The functionality is not complete yet.**
## Navigation
- [Installation](#installation)
- [Usage](#usage)
  - [Manual](#manual)
    - [Goal](#goal)
    - [NPCs](#npcs)
      - [Normal](#normal)
      - [Murderer](#murderer)
      - [Victim](#victim)
      - [Liar](#liar)
      - [Obsessive](#obsessive)
  - [Test](#test)
  - [Coverage Report](#coverage-report)
- [Links](#links)
## Installation
You are required to have Poetry installed to run this project. More instructions [here](https://python-poetry.org/docs/#installation).
1. Install dependencies using `poetry install`
2. Run the project using `poetry run invoke start`
## Usage
**Note: Currently the project works through terminal only. There will be a GUI in the future!**
### Manual
**Note: Some features mentioned in the manual may not be implemented yet!**
#### Goal
Interrogate NPCs and find out who the murderer is, and when they committed their crime!
#### NPCs
The game has five NPC types: Normal, Murderer, Victim, Liar and Obsessive. You won't be told the identities of these NPCs apart from the victim so pay close attention to what the NPCs tell you when you interrogate them! The patterns will reveal their type!
##### Normal
Normal NPCs show no special behaviours. They will visit random rooms during the night.
##### Murderer
Only one will be generated for each scenario. A murderer NPC will act a lot like a normal NPC but will lie about where they were at the time of the murder. Try to catch them in their lie by finding a discrepancy in their story compared to what other NPCs tell you!
##### Victim
Only one will be generated for each scenario. A victim NPC will act a lot like a normal NPC but will eventually end up in the same room with only the murderer NPC and be left there until discovered by another NPC. Note that the murderer themselves can also report the body!
##### Liar
Only one will be generated for each scenario. A liar NPC will never tell you the truth about where they were and who they were with. If you think you've found a discrepancy in someone's story, make sure you are not talking with a liar!
##### Obsessive
Only one will be generated for each scenario. An obsessive NPC will pick a random NPC to follow throughout the night. They will always be in an adjacent room and hence will always be able to tell where their obsession is, and with whom. They may have some really useful information if you get lucky...
### Test
To run currently implemented tests, use `poetry run invoke test`
### Coverage Report
To generate a coverage report, use `poetry run invoke coverage-report`
A coverage report will be generated in terminal but will also create a folder called *htmlcov*. Within it, you will find *index.html*. Opening it in browser will show a more visually pleasing coverage report.
## Links
* [Software Requirements Specification](https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/requirements.md)
* [Work hour sheet](https://github.com/Veloxization/ot-harjoitustyo/blob/master/documentation/workhours.md)
