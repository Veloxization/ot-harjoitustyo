from classes.time import Time

class Interrogation:
    def __init__(self, time, scenario):
        self.time = time
        self.scenario = scenario

    def where_were_you_at(self, npc, index):
        # Can't ask questions from the dead!
        if npc == self.scenario.victim:
            print("You: I'm a detective, not a psychic.")
            return
        # If the time goes over the discovery time, defaults to the discovery time
        if index > self.time.final_index:
            index = self.time.final_index
        print(f"You: Where were you at {self.time.index_to_string(index)}?")
        # The liar will always lie and uses the separate fake room list
        if npc.personality == "LIAR":
            print(f"{npc}: I was in the {npc.get_fake_room_at_time(index)}.")
            return npc.get_fake_room_at_time(index)
        # The murderer will only lie when it concerns the time of the murder
        elif npc.personality == "MURDERER" and index == self.scenario.murder_committed_index:
            print(f"{npc}: I was in the {npc.fake_room_at_murder_time}.")
            return npc.fake_room_at_murder_time
        print(f"{npc}: I was in the {npc.get_room_at_time(index)}.")
        return npc.get_room_at_time(index)

    def who_were_you_with_at(self, npc, index):
        if npc == self.scenario.victim:
            print("You: I'm a detective, not a psychic.")
            return
        if index > self.time.final_index:
            index = self.time.final_index
        print(f"You: Who were you with at {self.time.index_to_string(index)}?")
        if npc.personality == "LIAR":
            room = npc.get_fake_room_at_time(index)
            if len(room.fake_npcs[index]) > 1:
                # Create a coherent string that lists NPCs, separated by commas
                npc_list = ', '.join([nonPC.name for nonPC in room.fake_npcs[index] if nonPC != npc])
                print(f"{npc}: I was with the following people: {npc_list}.")
            else:
                print(f"{npc}: I was alone.")
        elif npc.personality == "MURDERER" and index == self.scenario.murder_committed_index:
            print(f"{npc}: I was alone.")
        else:
            room = npc.get_room_at_time(index)
            if len(room.npcs[index]) > 1:
                npc_list = ', '.join([nonPC.name for nonPC in room.npcs[index] if nonPC != npc])
                print(f"{npc}: I was with the following people: {npc_list}.")
            else:
                print(f"{npc}: I was alone.")

    def where_were_they_at(self, asked_npc, answer_npc, index):
        if asked_npc == self.scenario.victim:
            print("You: I'm a detective, not a psychic.")
            return
        if index > self.time.final_index:
            index = self.time.final_index
        print(f"You: Where was {answer_npc} at {self.time.index_to_string(index)}?")
        if asked_npc.personality == "LIAR":
            room = answer_npc.get_fake_room_at_time(index)
            if (room in asked_npc.get_fake_room_at_time(index).adjacent_rooms
            or room == asked_npc.get_fake_room_at_time(index)):
                print(f"{asked_npc}: I think {answer_npc} was in the {room}.")
            else:
                print(f"{asked_npc}: I don't know.")
        # The murderer only lies here if it concerns the victim at the time of the murder.
        elif (asked_npc.personality == "MURDERER"
             and index == self.scenario.murder_committed_index
             and asked_npc == self.scenario.victim):
            print(f"{asked_npc}: I don't know.")
        else:
            room = answer_npc.get_room_at_time(index)
            if (room in asked_npc.get_room_at_time(index).adjacent_rooms
            or room == asked_npc.get_room_at_time(index)):
                print(f"{asked_npc}: I think {answer_npc} was in the {room}.")
            else:
                print(f"{asked_npc}: I don't know.")
