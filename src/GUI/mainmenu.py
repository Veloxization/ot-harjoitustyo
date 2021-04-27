import pygame
import pygame_menu

from classes.save import Save
from classes.scenariogenerator import ScenarioGenerator
from GUI.intro import Intro

class MainMenu:
    def __init__(self,surface,clock):
        self.surface = surface
        self.clock = clock

        self.difficulty = 0
        self.loaded_save = None
        self.seed = None
        self.save = Save()

        self.menu = pygame_menu.Menu("Main Menu", 400, 300)
        self.menu.add.button("New Game", self.open_new_game_menu)
        self.menu.add.button("Load Game", self.open_load_game_menu)
        self.menu.add.button("Quit Game", pygame_menu.events.EXIT)

        self.new_game_menu = pygame_menu.Menu("New Game", 400, 300)
        self.new_game_menu.add.text_input("Seed: ", maxchar=10, onchange=self.set_seed)
        self.new_game_menu.add.selector("Difficulty: ", [("Easy", 0), ("Medium", 1), ("Hard", 2)], onchange=self.set_difficulty)
        self.new_game_menu.add.button("Start", self.start_game)
        self.new_game_menu.add.button("Back", self.return_to_main_menu)

        self.load_game_menu = pygame_menu.Menu("Load Game", 400, 300)
        save_list = [("New Game",1)]
        index = 1
        for save in self.save.list_saves():
            save_list.append((save, index))
            index += 1
        self.load_game_menu.add.dropselect("Save: ", save_list, placeholder="Select a save", placeholder_add_to_selection_box=True, onchange=self.set_save)
        self.load_game_menu.add.button("Load", self.load_game)
        self.load_game_menu.add.button("Back", self.return_to_main_menu)

    def start(self):
        self.menu.mainloop(self.surface)

    def open_new_game_menu(self):
        self.menu.close()
        self.new_game_menu.mainloop(self.surface)

    def open_load_game_menu(self):
        self.menu.close()
        self.load_game_menu.mainloop(self.surface)

    def start_game(self):
        self.menu.toggle()
        self.new_game_menu.toggle()
        self.surface.fill((0,0,0))
        scenario = ScenarioGenerator(self.seed, self.difficulty)
        intro = Intro(scenario, self.surface, self.clock)
        intro.start()

    def load_game(self):
        print("Loading a game")

    def return_to_main_menu(self):
        self.new_game_menu.close()
        self.load_game_menu.close()
        self.menu.mainloop(self.surface)

    def set_difficulty(self,difficulty,index):
        self.difficulty = index

    def set_save(self,save,index):
        self.save = save

    def set_seed(self,seed,**kwargs):
        self.seed = seed
