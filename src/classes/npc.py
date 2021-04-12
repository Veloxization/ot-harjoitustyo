from classes.room import Room

class Npc:
    # Obsession only defined for the OBSESSIVE personality
    def __init__(self,name,start_room,personality,obsession=None):
        self.name = name
        self.current_room = start_room
        self.fake_current_room = start_room
        self.current_room.add_npc(0,self)
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

    def set_personality(self,personality):
        if not personality:
            self.personality = "NORMAL"
        else:
            self.personality = personality

    def set_obsession(self,npc):
        if npc:
            self.obsession = npc

    def stay_in_room(self):
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    def fake_stay_in_room(self):
        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    def move_to_room(self,room):
        self.current_room = room
        self.routine.append(self.current_room)
        self.current_room.add_npc(len(self.routine)-1,self)

    def fake_move_to_room(self,room):
        self.fake_current_room = room
        self.fake_routine.append(self.fake_current_room)
        self.fake_current_room.fake_add_npc(len(self.fake_routine)-1,self)

    def set_fake_room_at_murder_time(self,room):
        self.fake_room_at_murder_time = room

    def get_room_at_time(self,index):
        return self.routine[index]

    def get_fake_room_at_time(self,index):
        return self.fake_routine[index]
