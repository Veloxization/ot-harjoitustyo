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

    def get_personal_routine(self):
        personal_routine = []
        index = 0
        for room in self.routine:
            personal_routine.append(f"{self.scenario.time.index_to_string(index)} {room}")
            index += 1
        return personal_routine

    def get_routine_of_npc(self,npc):
        other_routine = []
        index = 0
        npc_index = self.scenario.npcs.index(npc)
        for room in self.npc_location_at_time[npc_index]:
            other_routine.append(f"{self.scenario.time.index_to_string(index)} {room}")
            index += 1
        return other_routine

    def get_company_routine(self):
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
