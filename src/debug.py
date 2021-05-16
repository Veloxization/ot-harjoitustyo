import sys

from classes.save import Save

if __name__ == "__main__":
    files = []
    save = Save()
    files.extend(save.list_saves())
    options = {}
    INDEX = 0
    for file in files:
        options[str(INDEX)] = file
        print(INDEX, file)
        INDEX += 1
    action = input("Select a save by typing a number (enter anything else to exit): ")
    if action in options:
        option = options[action]
    else:
        sys.exit()
    scen, notes = save.load_from_file(option)
    print("Here is the information for the save:")
    print(f"\tMurderer: {scen.murderer}")
    print(f"\tVictim: {scen.victim}")
    print(f"\tWhistle blower: {scen.whistle_blower}")
    print(f"\tLiar: {scen.liar}")
    print(f"\tObsessive: {scen.obsessive}")
    print(f"\tObsession: {scen.obsessive.obsession}")
    print(f"\tMurder time: {scen.time.index_to_string(scen.murder_committed_index)}")
