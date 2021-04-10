from collections import namedtuple
from classes.room import Room

class Npc:
    # Obsession only defined for the OBSESSIVE personality
    def __init__(self,name,start_room,personality,obsession=None):
        self.name = name
        self.current_room = start_room
        self.current_room.add_npc(0,self)
        self.routine = [start_room]
        # Personalities: NORMAL, MURDERER, VICTIM, LIAR, OBSESSIVE
        self.personality = personality
        self.obsession = obsession

    def stay_in_room(self):
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(routine),self)

    def move_to_room(self,room):
        self.current_room = room
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(routine),self)
