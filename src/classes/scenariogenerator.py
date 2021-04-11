import random
from classes.npc import Npc
from classes.room import Room
from classes.time import Time

class ScenarioGenerator:
    def __init__(self,seed=None,difficulty=0):
        # Strings are accepted as a difficulty input just in case the user misunderstands the instructions
        if str(difficulty).lower() == "easy" or difficulty == "0": self.difficulty = 0
        elif str(difficulty).lower() == "medium" or difficulty == "1": self.difficulty = 1
        elif str(difficulty).lower() == "hard" or difficulty == "2": self.difficulty = 2
        else: self.difficulty = 0

        # If seed is not specified, set it as a random 32-bit signed integer
        if not seed:
            self.seed = random.randint(-2147483648,2147483647)
        else:
            self.seed = seed
        random.seed(a=self.seed)

        # A single scenario takes anywhere between 5 and 9 hours
        self.body_discovered_index = random.randint(30,54)
        # The murder is committed anywhere between 10 and 110 minutes before discovery
        self.murder_committed_index = self.body_discovered_index - random.randint(1,11)
        self.time = Time(self.body_discovered_index)

        # Split rooms by floor so they are easier to manage for difficulty settings
        rooms_G = {
                        "main_hall": Room("Main Hall", self.time),
                        "living_room": Room("Living Room", self.time),
                        "office": Room("Office", self.time),
                        "patio": Room("Patio", self.time),
                        "master_bedroom": Room("Master Bedroom", self.time),
                        "bathroom": Room("Bathroom", self.time),
                        "kitchen": Room("Kitchen", self.time),
                        "dining_room": Room("Dining Room", self.time)
        }
        rooms_LG = {
                         "basement_hall": Room("Basement Hall", self.time),
                         "wine_cellar": Room("Wine Cellar", self.time),
                         "laboratory": Room("Laboratory", self.time),
                         "archives": Room("Archives", self.time),
                         "storage": Room("Storage", self.time)
        }
        rooms_1F = {
                         "upstairs_hall": Room("Upstairs Hall", self.time),
                         "guest_room": Room("Guest Room", self.time),
                         "guest_bathroom": Room("Guest Bathroom", self.time),
                         "library": Room("Library", self.time),
                         "study": Room("Study", self.time),
                         "observatory": Room("Observatory", self.time),
                         "balcony": Room("Balcony", self.time),
                         "upstairs_hall": Room("Upstairs Hall", self.time)
        }
        # Set adjacent rooms for floor G
        for key in rooms_G:
            rooms_G["main_hall"].add_adjacent_room(rooms_G[key])
        rooms_G["kitchen"].add_adjacent_room(rooms_G["dining_room"])
        rooms_G["master_bedroom"].add_adjacent_room(rooms_G["bathroom"])
        rooms_G["master_bedroom"].add_adjacent_room(rooms_G["patio"])
        rooms_G["living_room"].add_adjacent_room(rooms_G["office"])

        # For now, easy will be the only difficulty to test the function of the game
        self.rooms = rooms_G

        with open("src/data/names.txt") as f:
            names = f.read().splitlines()
        self.npcs = []
        npc_names = random.sample(names, len(self.rooms)+1)
        for name in npc_names:
            self.npcs.append(Npc(name,self.rooms["main_hall"],"NORMAL"))
