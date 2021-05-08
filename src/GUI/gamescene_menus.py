import pygame
import pygame_menu

from classes.save import Save

class SaveMenu:
    def __init__(self, surface, scenario, notes):
        self.surface = surface
        self.scenario = scenario
        self.notes = notes
        self.save_name = ""
        self.menu = pygame_menu.Menu("Save", 400, 300)
        self.menu.add.text_input("Name: ", maxchar=10, onchange=self.set_save_name)
        self.menu.add.button("Save", self.save_game)
        self.menu.add.button("Back", self.return_to_game)

    def launch(self):
        self.menu.enable()
        self.menu.mainloop(self.surface)

    def save_game(self):
        if self.save_name:
            save = Save()
            save.write_to_file(self.save_name, self.scenario.seed, self.scenario.difficulty, self.notes)
            self.surface.fill((0,0,0))
            self.menu.disable()

    def return_to_game(self):
        self.surface.fill((0,0,0))
        self.menu.disable()

    def set_save_name(self,name,**kwargs):
        self.save_name = name

class NotesMenu:
    def __init__(self, surface, scenario, notes):
        self.surface = surface
        self.notes = notes
        width, height = surface.get_width() * 0.7, surface.get_height() * 0.7
        self.menu = pygame_menu.Menu("Notes", width, height)
        npcs = []
        index = 0
        for npc in scenario.npcs:
            npcs.append((npc.name, index))
            index += 1
        self.suspect = npcs[0][0]
        self.menu.add.dropselect("Suspect: ", npcs, default=0, onchange=self.change_suspect)
        self.menu.add.button("Personal routine", self.open_personal_routine_menu)
        self.menu.add.button("Company", self.open_company_menu)
        self.menu.add.button("Routine of another person", self.open_3rd_person_routine_menu)
        self.menu.add.button("Back", self.return_to_game)

    def launch(self):
        self.menu.mainloop(self.surface)

    def return_to_game(self):
        self.surface.fill((0,0,0))
        self.menu.disable()

    def change_suspect(self,npc,index):
        self.suspect = npc[0][0]

    def open_personal_routine_menu(self):
        self.surface.fill((0,0,0))
        note_entry = self.notes[self.suspect].get_personal_routine()
        personal_routine_menu = PersonalRoutineMenu(self.surface, note_entry)
        draw_object = pygame.sprite.RenderPlain()
        draw_object.add(personal_routine_menu)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        running = False
            draw_object.draw(self.surface)
            pygame.display.update()

    def open_company_menu(self):
        note_entry = self.notes[self.suspect].get_company_routine()

    def open_3rd_person_routine_menu(self):
        note_entry = self.notes[self.suspect].get_routine_of_npc(self.suspect)

class PersonalRoutineMenu(pygame.sprite.Sprite):
    def __init__(self, surface, note_entry):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.image = surface.copy()
        font = pygame.font.SysFont("monospace", 16)
        max_width = 0
        buffer = font.size("X")[0]
        for entry in note_entry:
            width, height = font.size(entry)
            if self.rect.y + height > surface.get_height():
                self.rect.y = 0
                self.rect = self.rect.move(max_width + buffer, 0)
                max_width = 0
            max_width = max(width, max_width)
            text = font.render(entry, 1, (255,255,255))
            surface.blit(text, self.rect)
            self.rect = self.rect.move(0, height)
