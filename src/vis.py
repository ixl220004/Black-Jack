import pygame
import sys


pygame.init()


x, y = 800, 600
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("blackjack")


#game loop
running = True
while running:
    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #game logic

    #draw
    screen.fill((0,0,0))

    #dislpay flip
    pygame.display.flip()

pygame.quit()
sys.exit()