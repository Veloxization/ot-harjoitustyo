class Npc:
    """The class that specifies the attributes of an NPC.

    Attributes:
        name: The name of the NPC.
        current_room: The room in which the NPC is currently (only used during
                        scenario generation)
        fake_current_room: The room in which the liar NPC will claim the NPC is
                            currently (only used during scenario generation)
        routine: A list of rooms the NPC visited during the night, in order.
        fake_routine: A list of rooms the NPC visited during the night, as told
                        by the liar
        fake_room_at_murder_time: The room the murderer will tell they were in
                                    at murder time.
        personality: The personality of the NPC (Normal, Murderer, Victim, Liar,
                        Obsessive)
        obsession: The NPC the obsessive NPC will follow around.
    """
    # Obsession only defined for the OBSESSIVE personality
    def __init__(self,name,start_room,personality,obsession=None):
        """Constructor that creates a new Npc object.

        Args:
            name: The name of the NPC.
            start_room: The room the NPC starts the night in.
            personality: The personality of the NPC.
            obsession: The NPC the obsessive NPC will follow around.
        """

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
        """Used to define equality between two objects, one of which is this
        NPC.

        Args:
            other: The object to which this NPC is compared.
        """

        if type(other) == str:
            return self.name == other
        else:
            return self.name == other.name

    def __str__(self):
        """What is displayed when the NPC is referred to in a string."""

        return self.name

    # Giving no arguments defaults to "NORMAL" personality
    def set_personality(self,personality=None):
        """Used to change the NPC's personality.

        Args:
            personality: The personality to which the NPC will be changed.
        """

        if not personality:
            self.personality = "NORMAL"
        else:
            self.personality = personality

    # Can be set for other types but does nothing
    def set_obsession(self,npc):
        """Used to change the NPC the obsessive NPC will follow around.

        Args:
            npc: The NPC the obsessive NPC will follow around.
        """

        if npc:
            self.obsession = npc

    def stay_in_room(self):
        """The NPC's room will stay the same for the next time index."""

        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    def fake_stay_in_room(self):
        """The NPC's room will stay the same for the next time index, as told
        by the liar.
        """

        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    def move_to_room(self,room):
        """The NPC's room changes to the specified room for the next time index.

        Args:
            room: The room to which the NPC will move.
        """

        self.current_room = room
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    def fake_move_to_room(self,room):
        """The NPC's room changes to the specified room for the next time index,
        as told by the liar.

        Args:
            room: The room the NPC supposedly moves to.
        """

        self.fake_current_room = room
        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    # Can also be set for other personalities but does nothing
    def set_fake_room_at_murder_time(self,room):
        """Sets the room the murderer will tell they were in at murder time to
        give themselves an alibi.

        Args:
            room: The room the murderer will claim they were in.
        """

        self.fake_room_at_murder_time = room

    def get_room_at_time(self,index):
        """Returns the room the NPC was in at the specifed time.

        Args:
            index: The time index.
        """

        return self.routine[index]

    def get_fake_room_at_time(self,index):
        """Returns the supposed room the NPC was in at the specified time, as told
        by the liar.

        Args:
            index: The time index.
        """

        return self.fake_routine[index]
