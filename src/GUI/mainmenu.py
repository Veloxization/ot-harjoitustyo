import pygame
import pygame_menu

from classes.save import Save
from classes.scenariogenerator import ScenarioGenerator
from classes.notes import Notes
from GUI.intro import Intro
from GUI.gamescene import GameScene

class MainMenu:
    def __init__(self,surface,clock):
        self.surface = surface
        self.clock = clock

        self.difficulty = 0
        self.loaded_save = None
        self.seed = None
        self.save_list = [("New Game",0)]

        self.menu = pygame_menu.Menu("Main Menu", 400, 300)
        self.menu.add.button("New Game", self.open_new_game_menu)
        self.menu.add.button("Load Game", self.open_load_game_menu)
        self.menu.add.button("Quit Game", pygame_menu.events.EXIT)

        self.new_game_menu = pygame_menu.Menu("New Game", 400, 300)
        self.new_game_menu.add.text_input("Seed: ", maxchar=10, onchange=self.set_seed)
        self.new_game_menu.add.selector("Difficulty: ", [("Easy", 0), ("Medium", 1), ("Hard", 2)], onchange=self.set_difficulty)
        self.new_game_menu.add.button("Start", self.start_game)
        self.new_game_menu.add.button("Back", self.return_to_main_menu)

        self.update_load_game_menu()

    def start(self):
        self.menu.mainloop(self.surface)

    def open_new_game_menu(self):
        if not self.new_game_menu.is_enabled():
            self.new_game_menu.enable()
        self.new_game_menu.mainloop(self.surface)

    def open_load_game_menu(self):
        if not self.load_game_menu.is_enabled():
            self.load_game_menu.enable()
        self.update_load_game_menu()
        self.load_game_menu.mainloop(self.surface)

    def update_load_game_menu(self):
        save = Save()
        self.save_list = [("New Game",0)]
        self.load_game_menu = pygame_menu.Menu("Load Game", 400, 300)
        index = 1
        for savedata in save.list_saves():
            self.save_list.append((savedata, index))
            index += 1
        self.load_game_menu.add.dropselect("Save: ", self.save_list, placeholder="Select a save", placeholder_add_to_selection_box=True, onchange=self.set_save)
        self.load_game_menu.add.button("Load", self.load_game)
        self.load_game_menu.add.button("Back", self.return_to_main_menu)

    def start_game(self):
        self.new_game_menu.disable()
        self.load_game_menu.disable()
        self.menu.disable()
        self.surface.fill((0,0,0))
        scenario = ScenarioGenerator(self.seed, self.difficulty)
        notes = {}
        for npc in scenario.npcs:
            notes[npc.name] = Notes(npc,scenario)
        intro = Intro(scenario, notes, self.surface, self.clock)
        intro.start()
        # This is run if the player returns from the game without terminating the process
        self.new_game_menu.enable()
        self.load_game_menu.enable()
        self.return_to_main_menu()

    def load_game(self):
        self.new_game_menu.disable()
        self.load_game_menu.disable()
        self.menu.disable()
        self.surface.fill((0,0,0))
        if self.loaded_save == "New Game":
            self.open_new_game_menu()
        saveloader = Save()
        scenario, notes = saveloader.load_from_file(self.loaded_save)
        scene = GameScene(self.surface,self.clock,scenario,notes)
        scene.start()
        self.new_game_menu.enable()
        self.load_game_menu.enable()
        self.return_to_main_menu()

    def return_to_main_menu(self):
        self.menu.enable()
        self.menu.mainloop(self.surface)

    def set_difficulty(self,difficulty,index):
        self.difficulty = index

    def set_save(self,save,index):
        self.loaded_save = save[0][0]

    def set_seed(self,seed,**kwargs):
        self.seed = seed
