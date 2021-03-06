class Interrogation:
    """A class that handles the logic behind question the player can ask NPCs.

    Attributes:
        time: The Time object used in the scenario.
        scenario: The scenario to which the interrogation is linked.
    """

    def __init__(self, time, scenario):
        """Constructor creates a new interrogation object.

        Args:
            time: The Time object used in the scenario.
            scenario: The current scenario.
        """

        self.time = time
        self.scenario = scenario

    def where_were_you_at(self, npc, index):
        """The NPC tells their location at a specific time or lies about it
        depending on personality

        Args:
            npc: The NPC to whom the question is posed.
            index: The time that is asked, index 0 is 18:00 and each following
                    index adds 10 minutes.
        """
        # Can't ask questions from the dead!
        dialogue = []
        if npc == self.scenario.victim:
            dialogue.append("You: I'm a detective, not a psychic.")
            return "No answer", dialogue
        # If the time goes over the discovery time, defaults to the discovery time
        if index > self.time.final_index:
            index = self.time.final_index
        dialogue.append(f"You: Where were you at {self.time.index_to_string(index)}?")
        # The liar will always lie and uses the separate fake room list
        if npc.personality == "LIAR":
            dialogue.append(f"{npc}: I was in the {npc.get_fake_room_at_time(index)}.")
            return npc.get_fake_room_at_time(index).name, dialogue
        # The murderer will only lie when it concerns the time of the murder
        if npc.personality == "MURDERER" and index == self.scenario.murder_committed_index:
            dialogue.append(f"{npc}: I was in the {npc.fake_room_at_murder_time}.")
            return npc.fake_room_at_murder_time.name, dialogue
        dialogue.append(f"{npc}: I was in the {npc.get_room_at_time(index)}.")
        return npc.get_room_at_time(index).name, dialogue

    def who_were_you_with_at(self, npc, index):
        """The NPC lists the people they were with at the specified time, or lies about it.

        Args:
            npc: The NPC to whom the question is posed.
            index: The time the NPC will recall, each number adding 10 minutes to 18:00.
        """

        dialogue = []
        if npc == self.scenario.victim:
            dialogue.append("You: I'm a detective, not a psychic.")
            return "No answer", dialogue
        if index > self.time.final_index:
            index = self.time.final_index
        dialogue.append(f"You: Who were you with at {self.time.index_to_string(index)}?")
        if npc.personality == "LIAR":
            room = npc.get_fake_room_at_time(index)
            if len(room.fake_npcs[index]) > 1:
                # Create a coherent string that lists NPCs, separated by commas
                npc_list = ', '.join([nonPC.name for nonPC in room.fake_npcs[index]
                                      if nonPC != npc])
                dialogue.append(f"{npc}: I was with the following people: {npc_list}.")
                return npc_list, dialogue
            dialogue.append(f"{npc}: I was alone.")
            return "Alone", dialogue
        if npc.personality == "MURDERER" and index == self.scenario.murder_committed_index:
            dialogue.append(f"{npc}: I was alone.")
            return "Alone", dialogue
        room = npc.get_room_at_time(index)
        if len(room.npcs[index]) > 1:
            npc_list = ', '.join([nonPC.name for nonPC in room.npcs[index] if nonPC != npc])
            dialogue.append(f"{npc}: I was with the following people: {npc_list}.")
            return npc_list, dialogue
        dialogue.append(f"{npc}: I was alone.")
        return "Alone", dialogue

    def where_were_they_at(self, asked_npc, answer_npc, index):
        """The NPC tells where another NPC was, or replies with I don't know if
        they weren't in the same or adjacent room.

        Args:
            asked_npc: The NPC to whom the question is posed.
            answer_npc: The NPC whose location the player wants to know.
            index: The time when the NPC's location is wanted.
        """
        dialogue = []
        if asked_npc == self.scenario.victim:
            dialogue.append("You: I'm a detective, not a psychic.")
            return "No answer", dialogue
        if index > self.time.final_index:
            index = self.time.final_index
        dialogue.append(f"You: Where was {answer_npc} at {self.time.index_to_string(index)}?")
        if asked_npc.personality == "LIAR":
            room = answer_npc.get_fake_room_at_time(index)
            if (room in asked_npc.get_fake_room_at_time(index).adjacent_rooms
            or room == asked_npc.get_fake_room_at_time(index)):
                dialogue.append(f"{asked_npc}: I think {answer_npc} was in the {room}.")
                return room.name, dialogue
            dialogue.append(f"{asked_npc}: I don't know.")
            return "Didn't know", dialogue
        # The murderer only lies here if it concerns the victim at the time of the murder.
        if (asked_npc.personality == "MURDERER"
             and index == self.scenario.murder_committed_index
             and asked_npc == self.scenario.victim):
            dialogue.append(f"{asked_npc}: I don't know.")
            return "Didn't know", dialogue
        room = answer_npc.get_room_at_time(index)
        if (room in asked_npc.get_room_at_time(index).adjacent_rooms
        or room == asked_npc.get_room_at_time(index)):
            dialogue.append(f"{asked_npc}: I think {answer_npc} was in the {room}.")
            return room.name, dialogue
        dialogue.append(f"{asked_npc}: I don't know.")
        return "Didn't know", dialogue
