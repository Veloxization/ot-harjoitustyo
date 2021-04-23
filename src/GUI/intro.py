import pygame
# Intro text when a new game is started
class Intro:
    def __init__(self, scen, surface, clock):
        self.scen = scen
        self.surface = surface
        self.clock = clock
        self.text = f"""You are a detective called to a mansion to solve a murder committed during a party.
        The party started at 18:00.

        {scen.victim} was found dead in the {scen.crime_scene} at {scen.time.index_to_string(scen.time.final_index)} by {scen.discoverer}.

        No one has seen or heard anything.
        It's up to you to solve this mystery."""
        print("Do stuff here")

    def start(self):
        board = Board(self.surface)
        text = Text(board)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(board, text)
        text.write(self.text)
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
            all_sprites.update()
            all_sprites.draw(self.surface)
            pygame.display.update()
            self.clock.tick(60)

class Text(pygame.sprite.Sprite):
    def __init__(self, board):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.image = pygame.Surface((10, 20))
        self.text = []
        self.text_width = 10
        self.text_height = 17
        self.rect = self.image.get_rect(topleft=(self.text_width, self.text_height))
        self.coord_x = 20
        self.coord_y = 20
        self.cooldown = 0
        self.cooldowns = {' ': 5, '\n': 30}

    def write(self, text):
        self.text = list(text)

    def update(self):
        if not self.cooldown:
            letter = self.text.pop(0)
            if letter == '\n':
                self.coord_x = 20-self.text_width
                self.coord_y += self.text_height
            else:
                self.coord_x += self.text_width
                self.board.add(letter, (self.coord_x, self.coord_y))
            self.cooldown = self.cooldowns.get(letter)
        else:
            self.cooldown -= 1

class Board(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.image = pygame.Surface((600, 400))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("monospace", 16)

    def add(self, letter, pos):
        s = self.font.render(letter, 1, (255, 255, 255))
        self.surface.blit(s, pos)
