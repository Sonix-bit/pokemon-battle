import pygame
import os

pygame.init()

color = (255, 255, 255)
position = (0, 0)

DS_WIDTH = 256
DS_HEIGHT = 192
# CREATING SCREEN 
canvas = pygame.display.set_mode((DS_WIDTH * 3, DS_HEIGHT * 3)) 
  
# TITLE OF SCREEN 
pygame.display.set_caption("Pokemon Game") 

charmander = pygame.transform.scale(pygame.image.load(os.path.join("img", "charmander.jpg")), (100, 100))
bulbasaur = pygame.transform.scale(pygame.image.load(os.path.join("img", "bulbasaur.jpg")), (100, 100))
squirtle = pygame.transform.scale(pygame.image.load(os.path.join("img", "squirtle.jpg")), (100, 100))
pikachu = pygame.transform.scale(pygame.image.load(os.path.join("img", "pikachu.jpg")), (100, 100))
exit = False

while not exit: 
    canvas.fill(color) 
    canvas.blit(charmander, dest = position)
    canvas.blit(bulbasaur, dest = (100, 100))
    canvas.blit(squirtle, dest = (200, 200))
    canvas.blit(pikachu, dest = (300, 300))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
    pygame.display.update()