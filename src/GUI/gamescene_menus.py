import pygame
import pygame_menu

from classes.save import Save
from classes.interrogation import Interrogation

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
        self.scenario = scenario
        self.width, self.height = surface.get_width() * 0.7, surface.get_height() * 0.7
        self.menu = pygame_menu.Menu("Notes", self.width, self.height)
        npcs = []
        index = 0
        for npc in scenario.npcs:
            if npc != scenario.victim:
                npcs.append((npc.name, index))
                index += 1
        self.suspect = npcs[0][0]
        self.third_suspect = npcs[0][0]
        self.menu.add.dropselect("Suspect: ", npcs, default=0, onchange=self.change_suspect)
        self.menu.add.button("Personal routine", self.open_personal_routine_menu)
        self.menu.add.button("Company", self.open_company_menu)
        self.menu.add.button("Routine of another person", self.open_3rd_person_selection_menu)
        self.menu.add.button("Back", self.return_to_game)

        self.selection_menu = pygame_menu.Menu(self.suspect, self.width, self.height)

    def launch(self):
        self.menu.enable()
        self.menu.mainloop(self.surface)

    def return_to_game(self):
        self.surface.fill((0,0,0))
        self.selection_menu.disable()
        self.menu.disable()

    def return_to_notes_menu(self):
        self.surface.fill((0,0,0))
        self.selection_menu.disable()
        self.menu.enable()

    def change_suspect(self,npc,index):
        self.suspect = npc[0][0]

    def change_third_suspect(self,npc,index):
        if "(dead)" in npc[0][0]:
            self.third_suspect = npc[0][0].split()[0]
        else:
            self.third_suspect = npc[0][0]

    def open_personal_routine_menu(self):
        self.surface.fill((0,0,0))
        note_entry = self.notes[self.suspect].get_personal_routine()
        personal_routine_menu = RoutineMenu(self.surface, note_entry)
        self.note_loop(personal_routine_menu)

    def open_company_menu(self):
        self.surface.fill((0,0,0))
        note_entry = self.notes[self.suspect].get_company_routine()
        company_routine_menu = RoutineMenu(self.surface, note_entry)
        self.note_loop(company_routine_menu)

    def open_3rd_person_selection_menu(self):
        self.selection_menu = pygame_menu.Menu(self.suspect, self.width, self.height)
        npcs = []
        index = 0
        for npc in self.scenario.npcs:
            if npc == self.scenario.victim:
                npcs.append((f"{npc.name} (dead)", index))
                index += 1
            elif npc != self.suspect:
                npcs.append((npc.name, index))
                index += 1
        self.third_suspect = npcs[0][0]
        self.selection_menu.add.dropselect("Suspect: ", npcs, default=0, onchange=self.change_third_suspect)
        self.selection_menu.add.button("Reported routine", self.open_3rd_person_routine_menu)
        self.selection_menu.add.button("Back", self.return_to_notes_menu)
        self.selection_menu.mainloop(self.surface)

    def open_3rd_person_routine_menu(self):
        self.surface.fill((0,0,0))
        note_entry = self.notes[self.suspect].get_routine_of_npc(self.third_suspect)
        third_person_routine_menu = RoutineMenu(self.surface, note_entry)
        self.note_loop(third_person_routine_menu)

    def note_loop(self, routine_menu):
        routine_menu.render_instructive_text(self.surface)
        draw_object = pygame.sprite.RenderPlain()
        draw_object.add(routine_menu)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        running = False
            draw_object.draw(self.surface)
            pygame.display.update()

class RoutineMenu(pygame.sprite.Sprite):
    def __init__(self, surface, note_entry):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.image = pygame.Surface((1,1))
        font = pygame.font.SysFont("monospace", 16)
        max_width = 0
        buffer = font.size("X")[0]
        for entry in note_entry:
            if font.size(entry)[0] > surface.get_width() // 3:
                words = entry.split()
                while words:
                    line = ""
                    while font.size(line)[0] < surface.get_width() // 3 and words:
                        word = words.pop(0)
                        width = font.size(word)[0]
                        line += word + " "
                    max_width = max(font.size(line)[0], max_width)
                    width = 0
                    height = font.size(line)[1]
                    text = font.render(line, 1, (255,255,255))
                    surface.blit(text, self.rect)
                    self.rect.y += height
            else:
                width, height = font.size(entry)
                if self.rect.y + height > surface.get_height():
                    self.rect.y = 0
                    self.rect = self.rect.move(max_width + buffer, 0)
                    max_width = 0
                text = font.render(entry, 1, (255,255,255))
                surface.blit(text, self.rect)
                self.rect = self.rect.move(0, height)
            max_width = max(width, max_width)

    def render_instructive_text(self, surface):
        font = pygame.font.SysFont("arial", 16)
        string = "Backspace to return"
        width, height = font.size(string)
        self.rect.x = surface.get_width() - width
        self.rect.y = surface.get_height() - height
        text = font.render(string, 1, (255,255,255))
        surface.blit(text, self.rect)

class InterrogationMenu:
    def __init__(self, surface, scenario):
        self.interrogation = Interrogation(scenario.time, scenario)
        self.dialogue = (None, [])
        self.surface = surface
        self.scenario = scenario
        width, height = surface.get_width() * 0.7, surface.get_height() * 0.7
        self.menu = pygame_menu.Menu("Interrogate", width, height)
        self.other_npcs = ["EMPTY"]
        npcs = []
        index = 0
        for npc in scenario.npcs:
            if npc != scenario.victim:
                npcs.append((npc.name, index))
                index += 1
        self.suspect = None
        questions = [("Where were you at __:__?", 0),
                     ("Who were you with at __:__?", 1),
                     ("Where was __ at __:__?", 2)]
        times = []
        for index in range(scenario.body_discovered_index + 1):
            time = scenario.time.index_to_string(index)
            times.append((time, index))
        self.suspect_selector = self.menu.add.dropselect("Suspect: ", npcs, default=0, onchange=self.change_suspect)
        self.question_selector = self.menu.add.dropselect("Question: ", questions, default=0, onchange=self.change_question)
        self.other_person_selector = self.menu.add.dropselect("Person: ", self.other_npcs, default=0)
        self.other_person_selector.hide()
        self.change_suspect(npcs, 0)
        self.time_selector = self.menu.add.dropselect("Time: ", times, default=0)
        self.interrogate_button = self.menu.add.button("Interrogate", self.interrogate)
        self.back_button = self.menu.add.button("Back", self.return_to_game)

    def launch(self):
        self.menu.enable()
        self.surface.fill((0,0,0))
        self.menu.mainloop(self.surface)

    def return_to_game(self):
        self.surface.fill((0,0,0))
        self.menu.disable()

    def interrogate(self):
        suspect = self.suspect_selector.get_value()[0][0]
        other_person = self.other_person_selector.get_value()[0][0]
        if "(dead)" in other_person:
            other_person = other_person.split()[0]
        for npc in self.scenario.npcs:
            if npc.name == suspect:
                suspect = npc
            elif npc.name == other_person:
                other_person = npc
        question = self.question_selector.get_index()
        time = self.time_selector.get_index()
        if question == 0:
            self.dialogue = self.interrogation.where_were_you_at(suspect, time)
        elif question == 1:
            self.dialogue = self.interrogation.who_were_you_with_at(suspect, time)
        else:
            self.dialogue = self.interrogation.where_were_they_at(suspect, other_person, time)
        self.return_to_game()

    def change_question(self, question, index):
        if index == 2:
            self.other_person_selector.show()
        else:
            self.other_person_selector.hide()

    def change_suspect(self, npc, index):
        self.suspect = npc[0][0]
        self.other_npcs = []
        index = 0
        for npc in self.scenario.npcs:
            if npc == self.scenario.victim:
                self.other_npcs.append((f"{npc.name} (dead)", index))
                index += 1
            elif npc != self.suspect:
                self.other_npcs.append((npc.name, index))
                index += 1
        self.other_person_selector.update_items(self.other_npcs)
        self.other_person_selector.make_selection_drop()

class AccusationMenu:
    def __init__(self, surface, scenario, clock):
        self.surface = surface
        self.scenario = scenario
        self.clock = clock
        self.solved = False
        self.width, self.height = surface.get_width() * 0.7, surface.get_height() * 0.7
        self.menu = pygame_menu.Menu("Accuse", self.width, self.height)
        npcs = []
        index = 0
        for npc in scenario.npcs:
            if npc != self.scenario.victim:
                npcs.append((npc.name, index))
                index += 1
        self.suspect = npcs[0][0]

        times = []
        index = 0
        for time_index in range(self.scenario.body_discovered_index + 1):
            time = self.scenario.time.index_to_string(time_index)
            times.append((time, index))
            index += 1
        self.time = times[0][0]
        self.menu.add.label("Select your suspect and murder time")
        self.menu.add.dropselect("Suspect: ", npcs, default=0, onchange=self.change_suspect)
        self.menu.add.dropselect("Time: ", times, default=0, onchange=self.change_time)
        self.menu.add.button("Accuse", self.accusation)
        self.menu.add.button("Back", self.return_to_game)

    def launch(self):
        self.menu.enable()
        self.menu.mainloop(self.surface)

    def return_to_game(self):
        self.surface.fill((0,0,0))
        self.menu.disable()

    def accusation(self):
        for npc in self.scenario.npcs:
            if npc == self.suspect:
                accused_npc = npc
                break
        accused_time = self.scenario.time.string_to_index(self.time)
        solved, dialogue = self.scenario.accuse(accused_npc, accused_time)
        self.solved = solved
        accusation_scene = AccusationDialogue(self.surface, dialogue, solved)
        dialogue_graphic = pygame.sprite.RenderPlain()
        dialogue_graphic.add(accusation_scene)
        self.surface.fill((0,0,0))
        while accusation_scene.dialogue:
            accusation_scene.render_dialogue()
            dialogue_graphic.draw(self.surface)
            pygame.display.update()
            self.clock.tick(60)
        accusation_scene.render_results()
        dialogue_graphic.draw(self.surface)
        pygame.display.update()
        waiting_for_user_input = True
        while waiting_for_user_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_user_input = False
                if event.type == pygame.KEYDOWN:
                    waiting_for_user_input = False
        self.return_to_game()

    def change_suspect(self, npc, index):
        self.suspect = npc[0][0]

    def change_time(self, time, index):
        self.time = time[0][0]

class AccusationDialogue(pygame.sprite.Sprite):
    def __init__(self, surface, dialogue, solved):
        super().__init__()
        dialogue_text = '\n'.join(dialogue)
        self.words = dialogue_text.split()
        self.dialogue = [char for char in dialogue_text]
        self.solved = solved
        self.surface = surface
        self.width, self.height = surface.get_width() * 0.7, surface.get_height() * 0.7
        self.image = pygame.Surface((self.width, self.height))
        x, y = (surface.get_width() - self.width) // 2, (surface.get_height() - self.height) // 2
        self.rect = pygame.Rect(x, y, 1, 1)
        self.x, self.y = 0, 0

    def render_dialogue(self):
        letter = self.dialogue.pop(0)
        word = ""
        if letter == ' ':
            word = self.words.pop(0)
        font = pygame.font.SysFont("monospace", 16)
        width, height = font.size(letter)
        word_width = font.size(word)[0]
        letter_graphic = font.render(letter, 1, (255,255,255))
        if letter == '\n' or self.x + word_width > self.width-5:
            self.x = 0
            self.y += height
        else:
            self.image.blit(letter_graphic, (self.x, self.y))
            self.x += width

    def render_results(self):
        victory_text = "MYSTERY SOLVED!\nPress any key to return to menu"
        failure_text = "NOT QUITE!\nPress any key to return to the map"
        if self.solved:
            text_to_render = victory_text
        else:
            text_to_render = failure_text
        top_text = text_to_render.split('\n')[0]
        bottom_text = text_to_render.split('\n')[1]
        font = pygame.font.SysFont("arial", 16)
        self.x = (self.width - font.size(top_text)[0]) // 2
        self.y += font.size(top_text)[1] * 2
        text = font.render(top_text, 1, (255,255,255))
        self.image.blit(text, (self.x, self.y))
        self.x = (self.width - font.size(bottom_text)[0]) // 2
        self.y += font.size(top_text)[1]
        text = font.render(bottom_text, 1, (255,255,255))
        self.image.blit(text, (self.x, self.y))
