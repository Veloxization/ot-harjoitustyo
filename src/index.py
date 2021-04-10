import random
from classes.npc import Npc
from classes.room import Room
from classes.time import Time

if __name__ == "__main__":
    seed = input("Enter seed (leave empty for random seed): ")
    if not seed:
        seed = random.randint(-2147483648,2147483647)
    random.seed(a=seed)
    body_discovered_index = random.randint(30,54)
    time = Time(body_discovered_index)
    rooms_G = {
                    "main_hall": Room("Main Hall", time),
                    "living_room": Room("Living Room", time),
                    "office": Room("Office", time),
                    "patio": Room("Patio", time),
                    "master_bedroom": Room("Master Bedroom", time),
                    "bathroom": Room("Bathroom", time),
                    "kitchen": Room("Kitchen", time),
                    "dining_room": Room("Dining Room", time)
    }
    npcs = []
