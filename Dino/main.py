import pygame
import os
import sys
from random import randrange
import sqlite3

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = screensize = (1200, 600)
FPS = 60

bg_col = (247, 247, 247)
speed = 6
score = 0

screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
pygame.display.set_caption("Dino")

path = os.path.dirname(os.path.abspath(__file__))

path_to_sound = os.path.join(path, 'Assets/Sounds/')
jump_sound = pygame.mixer.Sound(path_to_sound + 'jump.wav')
die_sound = pygame.mixer.Sound(path_to_sound + 'die.wav')

path_to_db = os.path.join(path, '../Database/games.db')
conn = sqlite3.connect(path_to_db)

high_score = conn.execute('SELECT MAX(score) FROM dino').fetchall()[0][0]
if not(high_score):
    high_score = 0
new_record = True


def load_image(name, colorkey=-1):
    fullname = os.path.join(path, 'Assets/Sprites', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return (image, image.get_rect())


def load_sheet(sheet, rect, image_count):
    tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
    images = []
    for tup in tups:
        rect = pygame.Rect(tup)
        image = pygame.Surface(rect.size).convert()
        image.blit(sheet, (0, 0), rect)
        colorkey = (0, 0, 0)
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        images.append(image)
    return images, images[0].get_rect()


class Ground():
    def __init__(self):
        self.image, self.rect = load_image('ground.png')
        self.image2, self.rect2 = load_image('ground.png')
        self.rect.bottom = self.rect2.bottom = HEIGHT
        self.rect2.left = self.rect.right
        self.speed = 5

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image2, self.rect2)

    def update(self):
        self.rect.left -= self.speed
        self.rect2.left -= self.speed
        
        if self.rect.right < 0:
            self.rect.left = self.rect2.right
        if self.rect2.right < 0:
            self.rect2.left = self.rect.right


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.images, self.rect = load_sheet(load_image('dino.png')[0], (0, 1, 88, 92), 4)
        self.image = self.images[0]
        self.rect.bottom = HEIGHT
        self.rect.left = 20
        self.isJump = False
        self.jumpVel = 23
        self.m = 5
        self.index = 0
        self.isDie = False
        self.isDucking = False

    def draw(self):
        screen.blit(self.image, self.rect)

    def handle_key(self):
        key = pygame.key.get_pressed()
        if not(self.isJump):
            if key[pygame.K_UP]:
                jump_sound.play()
                self.jump()
        else:
            if key[pygame.K_DOWN]:
                self.jumpVel = self.jumpVel - 2

    def jump(self):
        self.isJump = True

    def ducking(self):
        self.isDucking = True

    def update(self):
        self.image = self.images[self.index//5]
        self.index += 1
        if self.index == 12:
            self.index = 0
        
        if self.isJump:
            self.index = 0
            if self.jumpVel > 0:
                F = (0.5 * self.m * (self.jumpVel ** 2)) / FPS
            else:
                F = -(0.5 * self.m * (self.jumpVel ** 2)) / FPS
            self.rect.y = int(self.rect.y - F)
            self.jumpVel = self.jumpVel - 1.2
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.isJump = False
                self.jumpVel = 23

    def die(self):
        self.isDie = True
        self.image = self.images[3]
        die_sound.play()


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cactus_group, all_sprites)
        self.images, self.rect = load_sheet(load_image('cactus_big.png')[0], (0, 0, 49, 100), 4)
        self.speed = 5
        self.rect.bottom = HEIGHT
        self.rect.left = WIDTH + self.rect.width
        self.image = self.images[randrange(0, 3)]

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.rect = self.rect.move((-1*self.speed, 0))
        if self.rect.right < 0:
            self.kill()


class Scoreboard():
    def __init__(self):
        self.images, self.rect2 = load_sheet(load_image('nums.png')[0], (0, 0, 20, 21), 12)
        self.image = pygame.Surface((20*5, 21))
        self.rect = self.image.get_rect()
        self.numstr = '00000'
        self.rect.left = WIDTH - 200
        self.rect.top = 15
        
    def draw(self):
        screen.blit(self.image, self.rect)

    def change_score(self, score):
        if score > 99999:
            score = 99999
        score = self.numstr[0:5-len(str(score))] + str(score)
        return score

    def update(self, score):
        self.image.fill(bg_col)
        score = self.change_score(score)
        for num in score:
            self.image.blit(self.images[int(num)], self.rect2)
            self.rect2.left += self.rect2.width
        self.rect2.left = 0

cactus_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

ground = Ground()
dino = Dino()
scoreboard = Scoreboard()


def restart():
    replay_image, replay_rect = load_image('replay.png')
    replay_rect.center = (WIDTH // 2, HEIGHT // 2)

    gameover_image, gameover_rect = load_image('gameover.png')
    gameover_rect.center = (WIDTH // 2, HEIGHT // 3)

    screen.blit(replay_image, replay_rect)
    screen.blit(gameover_image, gameover_rect)


def draw(cactus, dino, ground, scoreboard, score):
    cactus.draw()
    cactus.update()

    dino.draw()
    dino.handle_key()
    dino.update()

    ground.draw()
    ground.update()

    scoreboard.draw()
    scoreboard.update(int(score))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dino.isDie = False
                conn.close()
                sys.exit()
            if dino.isDie and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if score > high_score:
                        high_score = int(score)
                    cactus.kill()
                    score = 0
                    speed = 6
                    dino.isDie = False
                    new_record = True

    if not(dino.isDie):
        screen.fill(bg_col)

        if not(cactus_group):
            cactus = Cactus()

        draw(cactus, dino, ground, scoreboard, score)

        if pygame.sprite.collide_mask(dino, cactus):
            if new_record:
                new_record = False
                conn.execute(f'INSERT INTO dino VALUES (NULL, {int(score)})')
                conn.commit()
            dino.die()
            screen.fill(bg_col)
            draw(cactus, dino, ground, scoreboard, score)
            restart()

        speed += 0.0066
        score += 0.16
        ground.speed = int(speed)
        cactus.speed = int(speed)

    pygame.display.flip()
    clock.tick(FPS)
