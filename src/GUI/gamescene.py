import pygame

from GUI.gamescene_menus import SaveMenu
from GUI.gamescene_menus import NotesMenu
from GUI.gamescene_menus import InterrogationMenu
from GUI.gamescene_menus import AccusationMenu

class RoomGraphic(pygame.sprite.Sprite):
    def __init__(self, surface, scenario, name, x=0, y=0, width=5, height=5):
        super().__init__()
        self.surface = surface
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.crime_scene = False
        if scenario.crime_scene == name:
            self.crime_scene = True
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        # Yellow is used as a highlight
        self.yellow = pygame.Surface((width, height))
        pygame.draw.rect(surface, (255,255,255), self.rect, 4)
        self.highlighted = False
        self.name = name
        self.namegraphic = pygame.font.SysFont("arial", 14)
        self.render_room_name(width, height)
        if self.crime_scene:
            self.render_body_text()

    def toggle_highlight(self):
        self.highlighted = not self.highlighted
        if self.highlighted:
            self.yellow.fill((255,255,0))
            self.yellow.set_alpha(40)
            self.image.blit(self.yellow, (0,0))
        else:
            self.yellow.fill((0,0,0))
            self.yellow.set_alpha(255)
            self.image.blit(self.yellow, (0,0))
            self.render_room_name(self.width, self.height)
            if self.crime_scene:
                self.render_body_text()

    def rerender(self):
        pygame.draw.rect(self.surface, (255,255,255), self.rect, 4)

    def render_body_text(self):
        text = pygame.font.SysFont("arial", 12)
        sizing = text.size("Body")
        x_coord = self.width - sizing[0]
        y_coord = 0
        s = text.render("Body", 1, (255,0,0))
        self.image.blit(s, (x_coord, y_coord))

    def render_room_name(self, width, height):
        # Room name should appear in the middle of the rectangle representing the room
        sizing = self.namegraphic.size(self.name)
        # If the text would be wider then the rectange, split it on two lines
        if sizing[0] > width and len(self.name.split()) > 1:
            # Has to be done this way because Pygame's text render does not support line breaks
            name = self.name.split()
            sizing = self.namegraphic.size(name[0])
            text_x = (width - sizing[0]) // 2
            text_y = (height - sizing[1]) // 2 - (sizing[1] // 2)
            s = self.namegraphic.render(name[0], 1, (255,255,255))
            self.image.blit(s, (text_x, text_y))
            sizing = self.namegraphic.size(name[1])
            text_x = (width - sizing[0]) // 2
            text_y = (height - sizing[1]) // 2 + (sizing[1] // 2)
            s = self.namegraphic.render(name[1], 1, (255,255,255))
            self.image.blit(s, (text_x, text_y))
        else:
            text_x = (width - sizing[0]) // 2
            text_y = (height - sizing[1]) // 2
            s = self.namegraphic.render(self.name, 1, (255,255,255))
            self.image.blit(s, (text_x, text_y))

class SceneText(pygame.sprite.Sprite):
    def __init__(self, text, size, pos):
        super().__init__()
        self.text = text
        font = pygame.font.SysFont("arial", size)
        width, height = font.size(text)
        self.image = pygame.Surface(font.size(text))
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        s = font.render(text, 1, (255,255,255))
        self.image.blit(s, (0,0))

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, function):
        super().__init__()
        self.text = text
        self.function = function
        self.active = False
        font = pygame.font.SysFont("arial", 16)
        font.underline = True
        width, height = font.size(text)
        self.image = pygame.Surface(font.size(text))
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        s = font.render(text, 1, (255,255,255))
        self.image.blit(s, (0,0))

    def activate(self):
        return self.function

class Level:
    def __init__(self, surface, scenario):
        self.surface = surface
        self.scenario = scenario
        self.room_sprites_G = pygame.sprite.Group()
        self.room_sprites_LG = pygame.sprite.Group()
        self.room_sprites_1F = pygame.sprite.Group()
        self.all_room_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.floor_buttons = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.interrogating = None
        self.question = None
        self.floor = 0
        self._initialize_sprites(surface)

    def _initialize_sprites(self, surface):
        map_width, map_height = surface.get_width() // 2, surface.get_height() // 2
        corner_x, corner_y = (surface.get_width() - map_width) // 2, (surface.get_height() - map_height) // 2
        cell_x, cell_y = map_width // 4, map_height // 4
        # INITIALISE FLOOR G
        floor = self.room_sprites_G
        # Add kitchen
        x, y = corner_x, corner_y
        width, height = cell_x * 2, cell_y
        self.add_room("Kitchen", floor, x, y, width, height)
        # Add dining room
        x = corner_x + (cell_x * 2) + 1
        self.add_room("Dining Room", floor, x, y, width, height)
        # Add office
        x, y = corner_x, corner_y + cell_y + 1
        width = cell_x
        self.add_room("Office", floor, x, y, width, height)
        # Add main hall
        x = corner_x + cell_x + 1
        width, height = cell_x * 2, cell_y * 3
        self.add_room("Main Hall", floor, x, y, width, height)
        # Add bathroom
        x += cell_x * 2 + 1
        width, height = cell_x, cell_y
        self.add_room("Bathroom", floor, x, y, width, height)
        # Add living room
        x = corner_x
        y += cell_y + 1
        height = cell_y * 2
        self.add_room("Living Room", floor, x, y, width, height)
        # Add master bedroom
        x += cell_x * 3 + 2
        height = cell_y
        self.add_room("Master Bedroom", floor, x, y, width, height)
        # Add patio
        y += cell_y + 1
        self.add_room("Patio", floor, x, y, width, height)

        # INITIALISE FLOOR LG
        floor = self.room_sprites_LG
        # Add wine cellar
        x, y = corner_x, corner_y
        width, height = cell_x * 3, cell_y
        self.add_room("Wine Cellar", floor, x, y, width, height)
        # Add laboratory
        x += cell_x * 3 + 2
        width, height = cell_x, cell_y * 2
        self.add_room("Laboratory", floor, x, y, width, height)
        # Add storage
        x, y = corner_x, corner_y + cell_y + 1
        width, height = cell_x, cell_y * 3
        self.add_room("Storage", floor, x, y, width, height)
        # Add basement hall
        x += cell_x + 1
        width, height = cell_x * 2, cell_y * 3
        self.add_room("Basement Hall", floor, x, y, width, height)
        # Add archives
        x += cell_x * 2 + 1
        y += cell_y + 1
        width, height = cell_x, cell_y * 2
        self.add_room("Archives", floor, x, y, width, height)

        # INITIALISE FLOOR 1F
        floor = self.room_sprites_1F
        # Add observatory
        x, y = corner_x, corner_y
        width, height = cell_x, cell_y
        self.add_room("Observatory", floor, x, y, width, height)
        # Add upstairs hall
        x += cell_x + 1
        width, height = cell_x * 2, cell_y * 4
        self.add_room("Upstairs Hall", floor, x, y, width, height)
        # Add balcony
        x += cell_x * 2 + 1
        width, height = cell_x, cell_y
        self.add_room("Balcony", floor, x, y, width, height)
        # Add study
        x, y = corner_x, corner_y + cell_y + 1
        self.add_room("Study", floor, x, y, width, height)
        # Add guest bedroom
        x += cell_x * 3 + 2
        height = cell_y * 2
        self.add_room("Guest Room", floor, x, y, width, height)
        # Add library
        x, y = corner_x, corner_y + cell_y * 2 + 2
        self.add_room("Library", floor, x, y, width, height)
        # Add guest bathroom
        x += cell_x * 3 + 2
        y += cell_y
        width, height = cell_x, cell_y
        self.add_room("Guest Bathroom", floor, x, y, width, height)

        # INITIALISE FLOOR NAMES
        size = 20
        font = pygame.font.SysFont("arial", size)
        # Add first floor
        text = "First Floor"
        width, height = font.size(text)
        x = (corner_x + map_width // 2) - width // 2
        y = corner_y - height * 2
        text_object = self.add_text(text, size, x, y)
        self.room_sprites_1F.add(text_object)
        # Add ground floor
        text = "Ground Floor"
        width, height = font.size(text)
        x = (corner_x + map_width // 2) - width // 2
        text_object = self.add_text(text, size, x, y)
        self.room_sprites_G.add(text_object)
        # Add lower ground floor
        text = "Lower Ground"
        width, height = font.size(text)
        x = (corner_x + map_width // 2) - width // 2
        text_object = self.add_text(text, size, x, y)
        self.room_sprites_LG.add(text_object)

        # INITIALISE BUTTONS
        font = pygame.font.SysFont("arial", 16)
        # Add the exit game button
        text = "Exit Game"
        width, height = font.size(text)
        x, y = surface.get_width() - width, surface.get_height() - height
        self.add_button(text, x, y, "EXIT")
        # Add the save game button
        text = "Save Game"
        width, height = font.size(text)
        x, y = 0, surface.get_height() - height
        self.add_button(text, x, y, "SAVE")
        # Add the floor 1F button
        text = "1F"
        width, height = font.size(text)
        x, y = surface.get_width() - width * 2, height * 2
        if self.scenario.difficulty == 2:
            self.add_button(text, x, y, "1F")
        # Add the floor G button
        text = "G"
        width, height = font.size(text)
        y += height
        if self.scenario.difficulty > 0:
            self.add_button(text, x, y, "G")
        # Add the floor LG button
        text = "LG"
        width, height = font.size(text)
        y += height
        if self.scenario.difficulty > 0:
            self.add_button(text, x, y, "LG")
        # Add the interrogation menu button
        text = "Interrogate"
        self.add_button(text, 0, 0, "INTERROGATE")
        # Add the notes menu button
        text = "Notes"
        width, height = font.size(text)
        x, y = 0, (surface.get_height() // 2) - height // 2
        self.add_button(text, x, y, "NOTES")
        # Add accusation menu button
        text = "Accuse"
        width, height = font.size(text)
        x, y = 0, (surface.get_height() // 2) + height // 2
        self.add_button(text, x, y, "ACCUSE")

    def add_room(self, name, floor, x, y, width, height):
        room = RoomGraphic(self.surface, self.scenario, name, x, y, width, height)
        floor.add(room)
        self.all_room_sprites.add(room)

    def add_button(self, text, x, y, function):
        button = Button(text, (x, y), function)
        self.buttons.add(button)

    def add_text(self, text, size, x, y):
        text_object = SceneText(text, size, (x,y))
        self.texts.add(text_object)
        return text_object

class GameScene:
    def __init__(self,surface,clock,scenario,notes):
        self.surface = surface
        self.clock = clock
        self.level = Level(surface, scenario)
        self.scen = scenario
        self.notes = notes
        self.active_floor = self.level.room_sprites_G

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    for roomgraph in self.level.all_room_sprites:
                        if roomgraph.rect.collidepoint(x, y):
                            roomgraph.toggle_highlight()
                    for button in self.level.buttons:
                        if button.rect.collidepoint(x, y):
                            function = button.activate()
                            if function == "EXIT":
                                running = False
                            elif function == "SAVE":
                                save_menu = SaveMenu(self.surface, self.scen, self.notes)
                                save_menu.launch()
                            elif function == "INTERROGATE":
                                interrogation_menu = InterrogationMenu(self.surface, self.scen)
                                interrogation_menu.launch()
                            elif function == "NOTES":
                                notes_menu = NotesMenu(self.surface, self.scen, self.notes)
                                notes_menu.launch()
                            elif function == "ACCUSE":
                                accusation_menu = AccusationMenu(self.surface, self.scen)
                                accusation_menu.launch()
                            elif function == "1F":
                                self.surface.fill((0,0,0))
                                self.active_floor = self.level.room_sprites_1F
                            elif function == "G":
                                self.surface.fill((0,0,0))
                                self.active_floor = self.level.room_sprites_G
                            elif function == "LG":
                                self.surface.fill((0,0,0))
                                self.active_floor = self.level.room_sprites_LG
            self._render()
            pygame.display.update()
            self.clock.tick(60)

    def _render(self):
        for room in self.active_floor:
            if room not in self.level.texts:
                room.rerender()
        self.active_floor.draw(self.surface)
        self.level.buttons.draw(self.surface)
