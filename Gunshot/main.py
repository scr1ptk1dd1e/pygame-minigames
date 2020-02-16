import pygame
import sys
import os
import sqlite3

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

WIDTH, HEIGHT = screensize = (650, 600)
FPS = 60
font = pygame.font.Font(None, 35)
font_win = pygame.font.Font(None, 50)
font_restart = pygame.font.Font(None, 45)
restart_button = pygame.Rect(325-75, 350-40, 150, 80)
stop = False
bg_col = (247, 247, 247)

screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
pygame.display.set_caption("Gunshot")

path = os.path.dirname(os.path.abspath(__file__))

path_to_sound = os.path.join(path, 'Assets/Sounds/')
shoot_sound = pygame.mixer.Sound(path_to_sound + 'shoot.wav')
reload_sound = pygame.mixer.Sound(path_to_sound + 'reload.wav')

score_red = 0
score_blue = 0

path_to_db = os.path.join(path, '../Database/games.db')
conn = sqlite3.connect(path_to_db)
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


class Player_red(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_red, all_sprites)
        self.image, self.rect = load_image('player_red.png')
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        
        self.speed = int(300 / FPS)
        self.direction = 0  # 0 - left, 1 - right

        self.bullet_image, self.bullet_rect = load_image('bullet_red.png')
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.reload_delay = 700
        self.clip = 5
        self.clip_list = pygame.Surface((16, 20*5))

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def draw_clip(self):
        self.clip_list.fill(bg_col)
        for _ in range(self.clip):
            self.clip_list.blit(self.bullet_image, self.bullet_rect)
            self.bullet_rect.top += 20
        self.bullet_rect.top = 0
        screen.blit(self.clip_list, (618, 450))

    def handle_key(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.shoot()
        if key[pygame.K_LEFT]:
            self.direction = 0
        if key[pygame.K_RIGHT]:
            self.direction = 1

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay and self.clip:
            self.last_shot = now
            self.clip -= 1
            bullet = Bullet_red(self.rect.centerx, self.rect.y)
            shoot_sound.play()

        if not(self.clip) and now - self.last_shot > self.reload_delay:
            self.last_shot = now
            self.clip = 5
            reload_sound.play()

    def update(self):
        self.handle_key()
        self.draw_clip()
        if self.direction:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= 600:
            self.rect.right = 600
            self.direction = 0


class Player_blue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_blue, all_sprites)
        self.image, self.rect = load_image('player_blue.png')
        self.rect.center = (WIDTH // 2, 50)
        self.speed = int(300 / FPS)
        self.direction = 0  # 0 - left, 1 - right

        self.bullet_image, self.bullet_rect = load_image('bullet_blue.png')
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.reload_delay = 700
        self.clip = 5
        self.clip_list = pygame.Surface((16, 20*5))

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def draw_clip(self):
        self.clip_list.fill(bg_col)
        for _ in range(self.clip):
            self.clip_list.blit(self.bullet_image, self.bullet_rect)
            self.bullet_rect.top += 20
        self.bullet_rect.top = 0
        screen.blit(self.clip_list, (618, 50))  

    def handle_key(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.shoot()
        if key[pygame.K_a]:
            self.direction = 0
        if key[pygame.K_d]:
            self.direction = 1

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay and self.clip:
            self.last_shot = now
            self.clip -= 1
            bullet = Bullet_blue(self.rect.centerx, self.rect.y)
            shoot_sound.play()

        if not(self.clip) and now - self.last_shot > self.reload_delay:
            self.last_shot = now
            self.clip = 5
            reload_sound.play()

    def update(self):
        self.handle_key()
        self.draw_clip()
        if self.direction:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= 600:
            self.rect.right = 600
            self.direction = 0


class Bullet_red(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullet_red, all_sprites)
        self.image, self.rect = load_image('bullet_red.png')
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 9

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


class Bullet_blue(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullet_blue, all_sprites)
        self.image, self.rect = load_image('bullet_blue.png')
        self.rect.top = y
        self.rect.centerx = x
        self.speed = 9

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

all_sprites = pygame.sprite.Group()
player_red = pygame.sprite.Group()
player_blue = pygame.sprite.Group()
bullet_red = pygame.sprite.Group()
bullet_blue = pygame.sprite.Group()

player1 = Player_red()
player2 = Player_blue()

text_red = font.render(str(score_red), 1, (255, 0, 0))
text_blue = font.render(str(score_blue), 1, (0, 0, 255))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn.close()
                sys.exit()
            elif stop:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart_button.collidepoint(mouse_pos):
                        new_record = True
                        stop = False
                        score_red = 0
                        score_blue = 0
                        all_sprites.empty()
                        player_red.empty()
                        player_blue.empty()
                        bullet_red.empty()
                        bullet_blue.empty()
                        player1 = Player_red()
                        player2 = Player_blue()
                        text_blue = font.render(str(score_blue), 1, (0, 0, 255))
                        text_red = font.render(str(score_red), 1, (255, 0, 0))

    screen.fill(bg_col)
    pygame.draw.line(screen, pygame.Color('black'), (600, 0), (600, 600), 2)

    pygame.sprite.groupcollide(bullet_blue, bullet_red, True, True)

    if pygame.sprite.groupcollide(bullet_blue, player_red, True, False):
        score_blue += 1
        text_blue = font.render(str(score_blue), 1, (0, 0, 255))
    if pygame.sprite.groupcollide(bullet_red, player_blue, True, False):
        score_red += 1
        text_red = font.render(str(score_red), 1, (255, 0, 0))

    screen.blit(text_blue, (620, HEIGHT//2 - 100))
    screen.blit(text_red, (620, HEIGHT//2 + 100))
    
    all_sprites.draw(screen)

    if score_red < 15 and score_blue < 15:
        all_sprites.update()
    else:
        stop = True
        tempbg = pygame.Surface((WIDTH, HEIGHT))
        tempbg.set_alpha(128)
        tempbg.fill((0, 0, 0))
        screen.blit(tempbg, (0, 0))
        if score_red > score_blue:
            text = font_win.render('RED WIN', 1, (255, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), restart_button)
        else:
            text = font_win.render('BLUE WIN', 1, (0, 0, 255))
            pygame.draw.rect(screen, (0, 0, 255), restart_button)
        text_x = WIDTH//2-text.get_width()//2
        text_y = (HEIGHT//2-text.get_height()//2) - 50
        screen.blit(text, (text_x, text_y))
        text = font_restart.render('RESTART', 1, (255, 255, 255))
        text_x = WIDTH//2-text.get_width()//2
        text_y = (HEIGHT//2-text.get_height()//2) - 50
        screen.blit(text, (text_x, text_y + 100))
        if new_record:
            new_record = False
            conn.execute(f'INSERT INTO gunshot VALUES(NULL, {score_red}, {score_blue})')
            conn.commit()

    pygame.display.flip()
    clock.tick(FPS)
