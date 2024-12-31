import pygame

pygame.init()

# CREATING SCREEN 
canvas = pygame.display.set_mode((500, 500)) 
  
# TITLE OF SCREEN 
pygame.display.set_caption("Pokemon Game") 
exit = False

while not exit: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
    pygame.display.update()