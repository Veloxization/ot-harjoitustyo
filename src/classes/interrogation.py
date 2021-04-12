from classes.time import Time

class Interrogation:
    def __init__(self, time):
        self.time = time

    def where_were_you_at(self, npc, index):
        if index > self.time.final_index: index = self.time.final_index
        print(f"You: Where were you at {self.time.index_to_string(index)}?")
        if npc.personality == "LIAR":
            print(f"{npc}: I was in the {npc.get_fake_room_at_time(index)}.")
        elif npc.personality == "MURDERER" and index == self.time.final_index:
            print(f"{npc}: I was in the {npc.fake_room_at_murder_time}.")
        else:
            print(f"{npc}: I was in the {npc.get_room_at_time(index)}.")

    def who_were_you_with_at(self, npc, index):
        if index > self.time.final_index: index = self.time.final_index
        print(f"You: Who were you with at {self.time.index_to_string(index)}?")
        if npc.personality == "LIAR":
            room = npc.get_fake_room_at_time(index)
            if len(room.npcs) > 1:
                print(f"{npc}: I was with {str([nonPC for nonPC in room.npcs if nonPC != npc])}")
