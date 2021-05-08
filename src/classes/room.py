class Room:
    """Class that defines the attributes of a room.

    Attributes:
        name: The name of the room.
        npcs: The list of lists of NPCs who visited the room during the night.
        fake_npcs: The list of lists of NPCs who supposedly visited the room
                    during the night, as told by the liar.
        adjacent_rooms: The rooms to which the NPCs in the current room can
                        "see".
    """

    def __init__(self,name,time_object):
        """Constructor that creates a new Room object.

        Args:
            name: The name of the room.
            time_object: The time object used in the scenario, for defining
                            the index range.
        """

        # Name of the room
        self.name = name
        # List of the NPCs in the room at a given time, takes sets
        self.npcs = [[] for i in range(time_object.final_index+1)]
        # A fake list used by the liar
        self.fake_npcs = [[] for i in range(time_object.final_index+1)]
        # List of adjacent rooms
        self.adjacent_rooms = []

    def __eq__(self, other):
        """Referred to when comparing another object to the Room.

        Args:
            other: The object to which the Room is compared to.
        """

        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

    def __str__(self):
        """Referred to when there's a need for a string display of the Room.
        """

        return self.name

    def add_npc(self,index,npc):
        """Adds an NPC to the room at a specified time.

        Args:
            index: The time index.
            npc: The NPC to add to the room at the specifed time.
        """

        if npc and npc not in self.npcs[index]:
            self.npcs[index].append(npc)

    def fake_add_npc(self,index,npc):
        """Adds an NPC to the fake list referred to by the liar.

        Args:
            index: The time index.
            npc: The NPC to add to the fake list at the specified time.
        """

        if npc and npc not in self.fake_npcs[index]:
            self.fake_npcs[index].append(npc)

    def add_adjacent_room(self,room):
        """Adds a room as an adjacent room, i.e. a room that is connected by a
        door.

        Args:
            room: The room this room connects to.
        """

        if room and room != self:
            if room not in self.adjacent_rooms:
                self.adjacent_rooms.append(room)
            if self not in room.adjacent_rooms:
                room.adjacent_rooms.append(self)
