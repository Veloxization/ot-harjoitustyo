import pygame

from GUI.mainmenu import MainMenu

if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("OT Detective Game")
    clock = pygame.time.Clock()
    mainmenu = MainMenu(surface,clock)
    mainmenu.start()
