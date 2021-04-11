class Room:
    def __init__(self,name,time_object):
        # Name of the room
        self.name = name
        # List of the NPCs in the room at a given time, takes sets
        self.npcs = [set() for i in range(time_object.final_index+1)]
        # List of adjacent rooms
        self.adjacent_rooms = set()

    # Adds an NPC to the room at a given time
    def add_npc(self,index,npc):
        if npc:
            self.npcs[index].add(npc)

    def add_adjacent_room(self,room):
        if room and room != self:
            self.adjacent_rooms.add(room)
            room.adjacent_rooms.add(self)
