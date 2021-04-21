class Notes:
    def __init__(self,npc,scenario):
        self.npc = npc
        self.scenario = scenario
        unknowns = ["UNKNOWN" for i in range(scenario.body_discovered_index)]
        self.routine = unknowns.copy()
        self.company = unknowns.copy()
        self.npc_location_at_time = [unknowns.copy() for i in range(len(scenario.npcs))]

    def add_routine_to_notes(self,index,room):
        self.routine[index] = room

    def add_company_to_notes(self,index,npcs):
        self.company[index] = npcs

    def add_npc_location_to_notes(self,index,npc,room):
        self.npc_location_at_time[self.scenario.npcs.index(npc)][index] = room
