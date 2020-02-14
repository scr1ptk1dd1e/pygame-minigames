'''
import pygame
import sys

pygame.init()

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = screensize = (650, 600)
FPS = 60
font = pygame.font.Font('Assets/Font/small_pixel.ttf', 16)

screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
pygame.display.set_caption("Mainwindow")

button_surface = pygame.Surface()

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    screen.fill(BLUE)
    text = font.render('Dino', 1, WHITE)
    screen.blit(text, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
'''

import pygame
import os

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

YELLOW = (255, 219, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (50, 70, 90)

FONT = pygame.font.Font('Assets/Font/small_pixel.ttf', 25)

text_dino = FONT.render("Dino", True, BLACK)
text_memory = FONT.render("Memory", True, BLACK)
text_todo = FONT.render("TODO", True, BLACK)
rect_dino = pygame.Rect(50, 200, 205, 60)
rect_memory = pygame.Rect(50, 300, 205, 60)
rect_todo = pygame.Rect(50, 400, 205, 60)

text_gunshot = FONT.render("gunshot", True, BLACK)
text_todo2 = FONT.render("TODO", True, BLACK)
text_todo3 = FONT.render("TODO", True, BLACK)
rect_gunshot = pygame.Rect(345, 200, 205, 60)
rect_todo2 = pygame.Rect(345, 300, 205, 60)
rect_todo3 = pygame.Rect(345, 400, 205, 60)

buttons = [
    ['dino', text_dino, rect_dino, YELLOW],
    ['memory', text_memory, rect_memory, YELLOW],
    ['todo', text_todo, rect_todo, YELLOW],
    ['gunshot', text_gunshot, rect_gunshot, YELLOW],
    ['todo', text_todo2, rect_todo2, YELLOW],
    ['todo', text_todo3, rect_todo3, YELLOW],
    ]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button[2].collidepoint(event.pos):
                    if button[0] == 'dino':
                        os.system('python ../Dino/main.py')
                    elif button[0] == 'gunshot':
                        os.system('python ../gunshot/main.py')

    screen.fill(WHITE)

    for type, text, rect, color in buttons:
        pygame.draw.rect(screen, color, rect)
        center = text.get_rect(center=(rect.x+102, rect.y+30))
        screen.blit(text, center)

    pygame.display.flip()
    clock.tick(15)