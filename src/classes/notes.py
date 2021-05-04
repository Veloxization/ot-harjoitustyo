class Notes:
    """The class that saves all the notes the player has collected during
    interrogation.

    Attributes:
        npc: The NPC to whom the notes are linked.
        scenario: The scenario to which the notes are linked.
    """

    def __init__(self,npc,scenario):
        """The constructor that creates a new Notes object.

        Args:
            npc: The NPC to whom the notes are linked.
            scenario: The scenario to which the notes are linked.
        """

        self.npc = npc
        self.scenario = scenario
        unknowns = ["UNKNOWN" for i in range(scenario.body_discovered_index)]
        self.routine = unknowns.copy()
        self.company = unknowns.copy()
        self.npc_location_at_time = [unknowns.copy() for i in range(len(scenario.npcs))]

    def add_routine_to_notes(self,index,room):
        """Adds the room the NPC tells they were in at a specified time.

        Args:
            index: The specified time.
            room: The room at that specified time.
        """

        self.routine[index] = room

    def add_company_to_notes(self,index,npcs):
        """Adds the NPCs the NPC told they were with at the specified time.

        Args:
            index: The specified time.
            npcs: The NPCs the NPC was with at the specified time.
        """

        self.company[index] = npcs

    def add_npc_location_to_notes(self,index,npc,room):
        """Adds the location of another NPC to the notes, as told by the NPC
        linked to the notes.

        Args:
            index: The specified time.
            npc: The NPC whose location was told.
            room: The location of that NPC.
        """

        self.npc_location_at_time[self.scenario.npcs.index(npc)][index] = room

    def get_personal_routine(self):
        """Returns the full notes regarding the NPC's movements during a
        scenario
        """

        personal_routine = []
        index = 0
        for room in self.routine:
            personal_routine.append(f"{self.scenario.time.index_to_string(index)} {room}")
            index += 1
        return personal_routine

    def get_routine_of_npc(self,npc):
        """Returns the full notes regarding the movements of another NPC as told
        by the NPC to whom the notes are linked.
        """

        other_routine = []
        index = 0
        npc_index = self.scenario.npcs.index(npc)
        for room in self.npc_location_at_time[npc_index]:
            other_routine.append(f"{self.scenario.time.index_to_string(index)} {room}")
            index += 1
        return other_routine

    def get_company_routine(self):
        """Returns the full list of NPCs with whom the NPC in question was with
        at different times.
        """
        
        companies = []
        index = 0
        for company in self.company:
            to_add = f"{self.scenario.time.index_to_string(index)} "
            if type(company) == list:
                to_add += ', '.join(company)
            else:
                to_add += company
            companies.append(to_add)
            index += 1
        return companies
