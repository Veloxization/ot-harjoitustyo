from classes.scenariogenerator import ScenarioGenerator
from classes.interrogation import Interrogation

if __name__ == "__main__":
    seed = input("Enter seed (leave empty for random seed): ")
    difficulty = input("0 - Easy (default)\n1 - Medium\n2 - Hard\nEnter difficulty (leave empty for default): ")
    scen = ScenarioGenerator(seed, difficulty)
    inter = Interrogation(scen.time, scen)
    # Before GUI, this will do
    print("You are a detective called to a mansion to solve a murder committed during a party.")
    print(f"The party started at 18:00.\n\n{scen.victim} was found dead in the {scen.crime_scene} at {scen.time.index_to_string(scen.time.final_index)} by {scen.discoverer}.\n\nNo one has seen or heard anything.")
    print("It's up to you to solve this mystery.")
    while(1):
        action = input("1 - List NPCs\n2 - Interrogate\n3 - Accuse\n4 - Exit\n\nChoose your action: ")
        # List NPCs
        if action == "1":
            for npc in scen.npcs:
                if npc == scen.victim:
                    print(npc, "- The Victim")
                else:
                    print(npc)
        # Interrogate
        elif action == "2":
            num = 1
            interrogation_list = {}
            for npc in scen.npcs:
                if npc != scen.victim:
                    interrogation_list[num] = npc
                    print(num, npc)
                    num += 1
            action = input("Interrogate (type a non-number to go back): ")
            try:
                npc = interrogation_list[int(action)]
            except:
                print("Going back...")
                continue
            print("1 Where were you at __:__?\n2 Who were you with at __:__?\n3 Where was __ at __:__?")
            action = input("Question (type a non-number to cancel): ")
            # Where were you at __:__?
            if action == "1":
                action = input("Type a 0-padded 24-hour time (e.g. 01:20): ")
                index = scen.time.string_to_index(action)
                if index == None:
                    print("Invalid time format. Use a 0-padded 24-hour format.")
                else:
                    inter.where_were_you_at(npc, index)
            # Who were you with at __:__?
            elif action == "2":
                action = input("Type a 0-padded 24-hour time (e.g. 01:20): ")
                index = scen.time.string_to_index(action)
                if index == None:
                    print("Invalid time format. Use a 0-padded 24-hour format.")
                else:
                    inter.who_were_you_with_at(npc, index)
            # Where was __ at __:__?
            elif action == "3":
                answer_npcs = {}
                num = 1
                for answer_npc in scen.npcs:
                    if answer_npc != npc:
                        answer_npcs[num] = answer_npc
                        if answer_npc == scen.victim:
                            print(num, answer_npc, "- The Victim")
                        else:
                            print(num, answer_npc)
                        num += 1
                action = input("Type a number corresponding to an NPC: ")
                try:
                    answer_npc = answer_npcs[int(action)]
                except:
                    print("Going back...")
                action = input("Type a 0-padded 24-hour time (e.g. 01:20): ")
                index = scen.time.string_to_index(action)
                if index == None:
                    print("Invalid time format. Use a 0-padded 24-hour format.")
                else:
                    inter.where_were_they_at(answer_npc, npc, index)
        # Accuse
        elif action == "3":
            num = 1
            accuse_npcs = {}
            for npc in scen.npcs:
                if npc != scen.victim:
                    accuse_npcs[num] = npc
                    print(num, npc)
                    num += 1
            action = input("Accuse (type a non-number to go back): ")
            try:
                npc = accuse_npcs[int(action)]
            except:
                print("Going back...")
            action = input("Type a 0-padded 24-hour time (e.g. 01:20): ")
            index = scen.time.string_to_index(action)
            if index == None:
                print("Invalid time format. Use a 0-padded 24-hour format.")
            else:
                if not scen.accuse(npc,index):
                    print("Try again!")
                else:
                    break
        # Exit
        elif action == "4":
            action = input("Are you sure you want to exit? (y/n) ")
            if action.lower() == "y" or action.lower() == "yes":
                print("Exiting...")
                break
            else:
                print("Continuing...")
        # Just something for development... Don't cheat with this, though
        elif action == "debug":
            print(f"Murderer: {scen.murderer}")
            print(f"Liar: {scen.liar}")
            print(f"Obsessive: {scen.obsessive}")
            print(f"Obsession: {scen.obsessive.obsession}")
            print(f"Murder time: {scen.time.index_to_string(scen.murder_committed_index)}")
        else:
            print("Write number 1, 2, 3 or 4 to choose an action")
