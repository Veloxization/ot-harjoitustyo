class Room:
    def __init__(self,name,time_object):
        # Name of the room
        self.name = name
        # List of the NPCs in the room at a given time, takes sets
        self.npcs = [[] for i in range(time_object.final_index+1)]
        # A fake list used by the liar
        self.fake_npcs = [[] for i in range(time_object.final_index+1)]
        # List of adjacent rooms
        self.adjacent_rooms = []

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    # Adds an NPC to the room at a given time
    def add_npc(self,index,npc):
        if npc and npc not in self.npcs[index]:
            self.npcs[index].append(npc)

    # Adds an NPC to the fake list
    def fake_add_npc(self,index,npc):
        if npc and npc not in self.fake_npcs[index]:
            self.fake_npcs[index].append(npc)

    # Adds a room as an adjacent room, i.e. a room that is connected by a door
    def add_adjacent_room(self,room):
        if room and room != self:
            if room not in self.adjacent_rooms:
                self.adjacent_rooms.append(room)
            if self not in room.adjacent_rooms:
                room.adjacent_rooms.append(self)
