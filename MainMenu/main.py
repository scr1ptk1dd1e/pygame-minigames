import pygame
import os
import sys
import platform

pygame.init()

python = 'python'
if platform.system() != 'Windows':
    python = 'python3'

WIDTH, HEIGHT = screensize = (600, 600)

screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("Minigames")
clock = pygame.time.Clock()

YELLOW = (255, 219, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (255, 229, 135)

path = os.path.dirname(os.path.abspath(__file__))

font = pygame.font.Font(os.path.join(path, 'Assets/Font/small_pixel.ttf'), 25)
font_head = pygame.font.Font(os.path.join(path, 'Assets/Font/small_pixel.ttf'), 30)

text_player = font_head.render('1 Player', True, BLACK)
text_players = font_head.render('2 Players', True, BLACK)

text_scoreboard = font.render('Scoreboard', True, BLACK)
rect_scoreboard = pygame.Rect(50, 500, 500, 60)

text_dino = font.render('Dino', True, BLACK)
text_memory = font.render('Memory', True, BLACK)
text_todo = font.render('TODO', True, BLACK)
rect_dino = pygame.Rect(50, 200, 205, 60)
rect_memory = pygame.Rect(50, 300, 205, 60)
rect_todo = pygame.Rect(50, 400, 205, 60)

text_gunshot = font.render('Gunshot', True, BLACK)
text_todo2 = font.render('TODO', True, BLACK)
text_todo3 = font.render('TODO', True, BLACK)
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
    ['score', text_scoreboard, rect_scoreboard, YELLOW],
    ]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button[2].collidepoint(event.pos):
                    if button[0] == 'dino':
                        cmdpath = os.path.join(path, '../Dino/main.py')
                        cmd = python + ' ' + cmdpath
                        os.system(cmd)
                    elif button[0] == 'gunshot':
                        cmdpath = os.path.join(path, '../Gunshot/main.py')
                        cmd = python + ' ' + cmdpath
                        os.system(cmd)
                    elif button[0] == 'score':
                        cmdpath = os.path.join(path, '../Scoreboard/main.py')
                        cmd = python + ' ' + cmdpath
                        os.system(cmd)
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button[2].collidepoint(event.pos):
                    button[3] = HOVER_COLOR
                else:
                    button[3] = YELLOW

    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (WIDTH//2, 200), (WIDTH//2, 460), 3)
    screen.blit(text_player, (75, 150))
    screen.blit(text_players, (360, 150))

    for game, text, rect, color in buttons:
        pygame.draw.rect(screen, color, rect)
        center = text.get_rect(center=(rect.x+rect.width//2, rect.y+rect.height//2))
        screen.blit(text, center)

    pygame.display.flip()
    clock.tick(15)