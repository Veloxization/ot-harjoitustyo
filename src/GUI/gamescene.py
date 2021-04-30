import pygame

class RoomGraphic(pygame.sprite.Sprite):
    def __init__(self, surface, name, x=0, y=0, width=5, height=5):
        super().__init__()
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        # Yellow is used as a highlight. Its width is initialised as -1 so it would be invisible at start
        self.image = pygame.Surface((width, height))
        self.yellow = pygame.Surface((width, height))
        self.yellow.set_alpha(0)
        self.graphic = pygame.draw.rect(surface, (255,255,255), self.rect, 4)
        self.highlighted = False
        self.name = name
        self.namegraphic = pygame.font.SysFont("arial", 16)
        # Room name should appear in the middle of the rectangle representing the room
        sizing = self.namegraphic.size(name)
        text_x = (width - sizing[0]) // 2
        text_y = (height - sizing[1]) // 2
        s = self.namegraphic.render(name, 1, (255,255,255))
        self.image.blit(s, (text_x, text_y))

    def highlight(self):
        self.highlighted = not self.highlighted
        if self.highlighted:
            self.yellow.width = 0
        else:
            self.yellow.width = -1

class Level:
    def __init__(self, surface):
        self.surface = surface
        self.room_sprites_G = pygame.sprite.Group()
        self.room_sprites_LG = pygame.sprite.Group()
        self.room_sprites_1F = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.floor = 0
        self._initialize_sprites(surface)

    def _initialize_sprites(self, surface):
        map_width, map_height = surface.get_width() // 2, surface.get_height() // 2
        corner_x, corner_y = (surface.get_width() - map_width) // 2, (surface.get_height() - map_height) // 2
        cell_x, cell_y = map_width // 4, map_height // 4
        # Add kitchen
        x, y = corner_x, corner_y
        width, height = cell_x * 2, cell_y
        self.room_sprites_G.add(RoomGraphic(surface, "Kitchen", x, y, width, height))
        # Add dining room
        x = corner_x + (cell_x * 2) + 1
        self.room_sprites_G.add(RoomGraphic(surface, "Dining Room", x, y, width, height))
        # Add office
        x, y = corner_x, corner_y + cell_y + 1
        width = cell_x
        self.room_sprites_G.add(RoomGraphic(surface, "Office", x, y, width, height))
        # Add main hall
        x = corner_x + cell_x + 1
        width, height = cell_x * 2, cell_y * 3
        self.room_sprites_G.add(RoomGraphic(surface, "Main Hall", x, y, width, height))

class GameScene:
    def __init__(self,surface,clock):
        self.surface = surface
        self.clock = clock
        self.level = Level(surface)

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self._render()
            pygame.display.update()
            self.clock.tick(60)

    def _render(self):
        self.level.room_sprites_G.draw(self.surface)
