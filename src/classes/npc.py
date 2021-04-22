class Npc:
    # Obsession only defined for the OBSESSIVE personality
    def __init__(self,name,start_room,personality,obsession=None):
        self.name = name
        self.current_room = start_room
        self.fake_current_room = start_room
        self.current_room.add_npc(0,self)
        self.fake_current_room.fake_add_npc(0,self)
        self.routine = [start_room]
        # Used by the murderer
        self.fake_room_at_murder_time = None
        # Used by the liar
        self.fake_routine = [start_room]
        # Personalities: NORMAL, MURDERER, VICTIM, LIAR, OBSESSIVE
        self.personality = personality
        self.obsession = obsession

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    # Can be used to change the NPCs personality, if needed.
    # Giving no arguments defaults to "NORMAL" personality
    def set_personality(self,personality=None):
        if not personality:
            self.personality = "NORMAL"
        else:
            self.personality = personality

    # Sets the obsession for the OBSESSIVE personality NPC
    # Can be set for other types but does nothing
    def set_obsession(self,npc):
        if npc:
            self.obsession = npc

    # The NPC does not move from the room they're currently in
    def stay_in_room(self):
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    # The NPC does not move from the supposed room they're currently in
    # Used by the LIAR personality
    def fake_stay_in_room(self):
        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    # The NPC moves to the specified room.
    def move_to_room(self,room):
        self.current_room = room
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    # The NPC supposedly moves to another, specified room
    # Used by the LIAR personality
    def fake_move_to_room(self,room):
        self.fake_current_room = room
        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    # Sets a fake room the MURDERER will tell they were in at the time of the
    # murder to try and give themselves an alibi.
    # Can also be set for other personalities but does nothing
    def set_fake_room_at_murder_time(self,room):
        self.fake_room_at_murder_time = room

    # Returns the room the NPC was in at the specified time
    def get_room_at_time(self,index):
        return self.routine[index]

    # Returns the supposed room the NPC was in at the specified time
    # Used by the LIAR personality
    def get_fake_room_at_time(self,index):
        return self.fake_routine[index]
