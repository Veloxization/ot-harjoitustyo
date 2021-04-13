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
        if action == "1":
            for npc in scen.npcs:
                if npc == scen.victim:
                    print(npc, "- The Victim")
                else:
                    print(npc)
        elif action == "2":
            num = 1
            for npc in scen.npcs:
                if npc == scen.victim:
                    print(num, npc, "- Dead. Can't be interrogated.")
                else:
                    print(num, npc)
                num += 1
            action = input("Interrogate (type a non-number to go back): ")
            try:
                npc = scen.npcs[int(action)-1]
            except:
                print("Going back...")
                continue
            print("1 Where were you at __:__?")
            action = input("Question (type a non-number to cancel): ")
            if action == "1":
                action = input("Type a 0-padded 24-hour time (e.g. 01:20): ")
                index = scen.time.string_to_index(action)
                if index == None:
                    print("Invalid time format. Use a 0-padded 24-hour format.")
                else:
                    inter.where_were_you_at(npc, index)
        elif action == "3":
            num = 1
            for npc in scen.npcs:
                if npc == scen.victim:
                    print(num, npc, "- It wasn't a suicide...")
                else:
                    print(num, npc)
                num += 1
            action = input("Accuse (type a non-number to go back): ")
        elif action == "4":
            action = input("Are you sure you want to exit? (y/n) ")
            if action.lower() == "y" or action.lower() == "yes":
                print("Exiting...")
                break
            else:
                print("Continuing...")
        else:
            print("Write number 1, 2, 3 or 4 to choose an action")
