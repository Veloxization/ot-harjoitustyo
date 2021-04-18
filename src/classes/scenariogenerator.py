import random
from classes.npc import Npc
from classes.room import Room
from classes.time import Time

class ScenarioGenerator:
    def __init__(self,seed=None,difficulty=0):
        # Strings are accepted as a difficulty input just in case the user misunderstands the instructions
        if str(difficulty).lower() == "easy" or difficulty == "0":
            self.difficulty = 0
        elif str(difficulty).lower() == "medium" or difficulty == "1":
            self.difficulty = 1
        elif str(difficulty).lower() == "hard" or difficulty == "2":
            self.difficulty = 2
        else:
            self.difficulty = 0

        # If seed is not specified, set it as a random 32-bit signed integer
        if not seed:
            self.seed = random.randint(-2147483648,2147483647)
        else:
            self.seed = seed
        random.seed(a=self.seed)

        # A single scenario takes anywhere between 5 and 9 hours
        self.body_discovered_index = random.randint(30,54)
        # The murder is committed anywhere between 10 and 200 minutes before discovery (adjust this if too difficult?)
        self.murder_committed_index = self.body_discovered_index - random.randint(1,20)
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
                         "balcony": Room("Balcony", self.time)
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

        # Select the room where the murder will be committed
        self.crime_scene = random.choice([room for room in list(self.rooms.values()) if room != rooms_G["main_hall"] and room != rooms_LG["basement_hall"] and room != rooms_1F["upstairs_hall"]])

        # Get random names from the names.txt file
        with open("src/data/names.txt") as f:
            names = f.read().splitlines()
        self.npcs = []
        npc_names = random.sample(names, len(self.rooms)+1)
        for name in npc_names:
            self.npcs.append(Npc(name,self.rooms["main_hall"],"NORMAL"))

        # Set the special NPC traits
        # Murderer acts like a normal NPC, visiting random rooms, but will move in a pre-selected room with the victim until the kill
        self.npcs[0].set_personality("MURDERER")
        self.murderer = self.npcs[0]
        # Victim acts like a normal NPC but will move to a pre-selected room with the murderer
        self.npcs[1].set_personality("VICTIM")
        self.victim = self.npcs[1]
        # The liar will use separate fake routines for each NPC
        self.npcs[2].set_personality("LIAR")
        self.liar = self.npcs[2]
        # An obsessive person will stay in an adjacent room to their randomly selected obsession at all times
        self.npcs[-1].set_personality("OBSESSIVE")
        self.npcs[-1].set_obsession(random.choice([npc for npc in self.npcs if npc != self.npcs[-1]]))
        self.obsessive = self.npcs[-1]

        # Select the NPC (other than the victim or liar) who discovers the body. Can be the murderer themselves!
        self.discoverer = random.choice([npc for npc in self.npcs if npc not in (self.victim, self.liar)])

        # Generate a routine for each NPC
        for npc in self.npcs:
            for i in range(1, self.body_discovered_index+1):
                if npc == self.discoverer and i == self.body_discovered_index:
                    npc.move_to_room(self.crime_scene)
                elif npc in (self.murderer, self.victim) and i == self.murder_committed_index:
                    npc.move_to_room(self.crime_scene)
                elif npc == self.victim and i > self.murder_committed_index:
                    # Don't want the dead to be walking...
                    npc.stay_in_room()
                elif npc == self.obsessive:
                    # Don't move the obsessive NPC to the room where the murder is being committed
                    if i >= self.murder_committed_index:
                        npc.move_to_room(random.choice([room for room in npc.obsession.get_room_at_time(i).adjacent_rooms if room != self.crime_scene]))
                    else:
                        npc.move_to_room(random.choice(npc.obsession.get_room_at_time(i).adjacent_rooms))
                # NPCs are more likely to stay in one room than to move to another room
                elif random.randint(0,9) < 7:
                    if npc.current_room != self.crime_scene and i >= self.murder_committed_index:
                        npc.stay_in_room()
                    # Even if the "dice roll" tells the NPC to stay at the crime scene... don't.
                    else:
                        npc.move_to_room(random.choice([room for room in list(self.rooms.values()) if room != npc.current_room]))
                else:
                    if i >= self.murder_committed_index:
                        # No one goes to the crime scene before the scripted time when the body is discovered
                        npc.move_to_room(random.choice([room for room in list(self.rooms.values()) if room not in (npc.current_room, self.crime_scene)]))
                    else:
                        npc.move_to_room(random.choice([room for room in list(self.rooms.values()) if room != npc.current_room]))
                # Same situation with the fake routines
                if random.randint(0,9) < 7:
                    npc.fake_stay_in_room()
                else:
                    npc.fake_move_to_room(random.choice(list(self.rooms.values())))

        # Set the fake room the murderer will tell about at murder time.
        # The room has to be occupied by someone else (other than the liar) so they can be caught in the lie
        self.whistle_blower = random.choice([npc for npc in self.npcs if npc not in (self.victim, self.murderer, self.liar)])
        self.murderer.set_fake_room_at_murder_time(self.whistle_blower.get_room_at_time(self.murder_committed_index))

        # Shuffle the NPC list to avoid a pattern with most special NPCs appearing at the start of the list
        random.shuffle(self.npcs)

    def accuse(self, npc, index):
        solved = False
        print(f"You: I think the murderer is {npc} and they committed their crime at {self.time.index_to_string(index)}!")
        if npc == self.murderer and index == self.murder_committed_index:
            print(f"{npc}: Not possible. I am sure I was in the {npc.fake_room_at_murder_time} at that time. There were no bodies.")
            print(f"{self.whistle_blower}: You're lying! I was in the {self.whistle_blower.get_room_at_time(self.murder_committed_index)} at {self.time.index_to_string(index)}! You weren't there!")
            print(f"YOU ARE CORRECT! {npc} is the murderer and the crime was committed at {self.time.index_to_string(index)}!")
            solved = True
        else:
            print(f"{npc}: Not possible. I am sure I was in the {npc.get_room_at_time(index)} at that time. There were no bodies.")
        return solved
