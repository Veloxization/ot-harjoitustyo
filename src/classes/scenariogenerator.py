import random
from classes.npc import Npc
from classes.room import Room
from classes.time import Time

class ScenarioGenerator:
    """The class that handles the generation of a scenario.

    Attributes:
        difficulty: The difficulty of the scenario, higher difficulty means more
                    rooms and NPCs.
        seed: The seed used by Python's random number generation, guarantees an
                identical scenario if the same seed is used.
        body_discovered_index: The time index at which an NPC discovers the
                                murder victim.
        murder_committed_index: The time at which the victim and the murderer
                                are in the same room and the murder is
                                committed.
        time: The Time object used by the scenario.
        rooms: A dictionary of rooms used in the scenario.
        crime_scene: The room in which the victim is killed and found.
        npcs: A list of NPCs involved in the scenario.
        murderer: The culprit NPC of the scenario.
        victim: The NPC who dies in this scenario.
        liar: The liar NPC of this scenario.
        obsessive: The obsessive NPC of this scenario.
        discoverer: The NPC who reports the body. Can be the murderer.
        whistle_blower: The NPC whose room the murderer claims to be in at
                        murder time.
    """
    def __init__(self,seed=None,difficulty=0):
        # Strings are accepted as a difficulty input
        if str(difficulty).lower() == "easy" or difficulty in ("0", 0):
            self.difficulty = 0
        elif str(difficulty).lower() == "medium" or difficulty in ("1", 1):
            self.difficulty = 1
        elif str(difficulty).lower() == "hard" or difficulty in ("2", 2):
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
        # The murder is committed anywhere between 10 and 200 minutes before
        # discovery (adjust this if too difficult?)
        self.murder_committed_index = self.body_discovered_index - random.randint(1,20)
        self.time = Time(self.body_discovered_index)

        # Split rooms by floor so they are easier to manage for difficulty settings
        rooms_g = {
                        "main_hall": Room("Main Hall", self.time),
                        "living_room": Room("Living Room", self.time),
                        "office": Room("Office", self.time),
                        "patio": Room("Patio", self.time),
                        "master_bedroom": Room("Master Bedroom", self.time),
                        "bathroom": Room("Bathroom", self.time),
                        "kitchen": Room("Kitchen", self.time),
                        "dining_room": Room("Dining Room", self.time)
        }
        rooms_lg = {
                         "basement_hall": Room("Basement Hall", self.time),
                         "wine_cellar": Room("Wine Cellar", self.time),
                         "laboratory": Room("Laboratory", self.time),
                         "archives": Room("Archives", self.time),
                         "storage": Room("Storage", self.time)
        }
        rooms_1f = {
                         "upstairs_hall": Room("Upstairs Hall", self.time),
                         "guest_room": Room("Guest Room", self.time),
                         "guest_bathroom": Room("Guest Bathroom", self.time),
                         "library": Room("Library", self.time),
                         "study": Room("Study", self.time),
                         "observatory": Room("Observatory", self.time),
                         "balcony": Room("Balcony", self.time)
        }
        # Set adjacent rooms for floor G
        for key in rooms_g:
            rooms_g["main_hall"].add_adjacent_room(rooms_g[key])
        rooms_g["kitchen"].add_adjacent_room(rooms_g["dining_room"])
        rooms_g["master_bedroom"].add_adjacent_room(rooms_g["bathroom"])
        rooms_g["master_bedroom"].add_adjacent_room(rooms_g["patio"])
        rooms_g["living_room"].add_adjacent_room(rooms_g["office"])

        # Set adjacent rooms for floor LG
        for key in rooms_lg:
            rooms_lg["basement_hall"].add_adjacent_room(rooms_lg[key])
        rooms_lg["laboratory"].add_adjacent_room(rooms_lg["archives"])
        rooms_lg["wine_cellar"].add_adjacent_room(rooms_lg["storage"])

        # Set adjacent rooms for floor 1F
        for key in rooms_1f:
            rooms_1f["upstairs_hall"].add_adjacent_room(rooms_1f[key])
        rooms_1f["guest_room"].add_adjacent_room(rooms_1f["guest_bathroom"])
        rooms_1f["guest_room"].add_adjacent_room(rooms_1f["balcony"])
        rooms_1f["study"].add_adjacent_room(rooms_1f["library"])
        rooms_1f["study"].add_adjacent_room(rooms_1f["observatory"])

        # Difficulty determines which floors are available
        if self.difficulty == 2:
            self.rooms = {**rooms_g, **rooms_lg, **rooms_1f}
        elif self.difficulty == 1:
            self.rooms = {**rooms_g, **rooms_lg}
        else:
            self.rooms = rooms_g

        # Select the room where the murder will be committed
        self.crime_scene = random.choice([room for room in list(self.rooms.values())
                                          if room not in (rooms_g["main_hall"],
                                          rooms_lg["basement_hall"], rooms_1f["upstairs_hall"])])

        # Get random names from the names.txt file
        with open("src/data/names.txt") as file:
            names = file.read().splitlines()
        self.npcs = []
        npc_names = random.sample(names, len(self.rooms)+1)
        for name in npc_names:
            self.npcs.append(Npc(name,self.rooms["main_hall"],"NORMAL"))

        # Set the special NPC traits
        # Murderer acts like a normal NPC, visiting random rooms, but will move
        # in a pre-selected room with the victim until the kill
        self.npcs[0].set_personality("MURDERER")
        self.murderer = self.npcs[0]
        # Victim acts like a normal NPC but will move to a pre-selected room
        # with the murderer
        self.npcs[1].set_personality("VICTIM")
        self.victim = self.npcs[1]
        # The liar will use separate fake routines for each NPC
        self.npcs[2].set_personality("LIAR")
        self.liar = self.npcs[2]
        # An obsessive person will stay in an adjacent room to their randomly
        # selected obsession at all times
        self.npcs[-1].set_personality("OBSESSIVE")
        self.npcs[-1].set_obsession(random.choice([npc for npc in self.npcs
                                                   if npc != self.npcs[-1]]))
        self.obsessive = self.npcs[-1]

        # Select the NPC (other than the victim or liar) who discovers the body.
        # Can be the murderer themselves!
        self.discoverer = random.choice([npc for npc in self.npcs
                                         if npc not in (self.victim, self.liar)])

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
                        npc.move_to_room(random.choice([room for room
                                                        in npc.obsession.get_room_at_time(i).adjacent_rooms
                                                        if room != self.crime_scene]))
                    else:
                        npc.move_to_room(random.choice(
                                                       npc.obsession.get_room_at_time(i).adjacent_rooms)
                                                      )
                # NPCs are more likely to stay in one room than to move to another room
                elif random.randint(0,9) < 7:
                    if npc.current_room != self.crime_scene and i >= self.murder_committed_index:
                        npc.stay_in_room()
                    # Even if the "dice roll" tells the NPC to stay at the crime scene... don't.
                    else:
                        npc.move_to_room(random.choice([room for room
                                                        in list(self.rooms.values())
                                                        if room != npc.current_room]))
                else:
                    if i >= self.murder_committed_index:
                        # No one goes to the crime scene before the scripted
                        # time when the body is discovered
                        npc.move_to_room(random.choice([room for room
                                                        in list(self.rooms.values())
                                                        if room not in
                                                        (npc.current_room, self.crime_scene)]))
                    else:
                        npc.move_to_room(random.choice([room for room
                                                        in list(self.rooms.values())
                                                        if room != npc.current_room]))
                # Same situation with the fake routines
                if random.randint(0,9) < 7:
                    npc.fake_stay_in_room()
                else:
                    npc.fake_move_to_room(random.choice(list(self.rooms.values())))

        # Set the fake room the murderer will tell about at murder time.
        # The room has to be occupied by someone else (other than the liar) so
        # they can be caught in the lie
        self.whistle_blower = random.choice([npc for npc
                                             in self.npcs
                                             if npc not in
                                             (self.victim, self.murderer, self.liar)])
        self.murderer.set_fake_room_at_murder_time(self.whistle_blower.get_room_at_time(self.murder_committed_index))

        # Shuffle the NPC list to avoid a pattern with most special NPCs
        # appearing at the start of the list
        random.shuffle(self.npcs)

    def accuse(self, npc, index):
        """The accusation function. Checks if the player's deduction on the
        culprit and murder time is correct.

        Args:
            npc: The NPC the player is accusing.
            index: The time index the player thinks the murder was committed at.
        """

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
