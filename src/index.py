from classes.scenariogenerator import ScenarioGenerator

if __name__ == "__main__":
    seed = input("Enter seed (leave empty for random seed): ")
    difficulty = input("0 - Easy (default)\n1 - Medium\n2 - Hard\nEnter difficulty (leave empty for default): ")
    scen = ScenarioGenerator(seed, difficulty)
    print(scen.npcs[0].get_room_at_time(0).name)
