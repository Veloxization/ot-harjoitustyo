# Used for testing the game with a GUI
import pygame

#from GUI.mainmenu import MainMenu
from GUI.gamescene import GameScene

if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("OT Detective Game")
    clock = pygame.time.Clock()
    #mainmenu = MainMenu(surface,clock)
    #mainmenu.start()
    scene = GameScene(surface,clock)
    scene.start()
