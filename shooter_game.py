import pygame
from pygame import *
from random import randint
import time

# Клас GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        pass

# Клас Player
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, health):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = health

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.y, 15, 20, -10)
        bullets.add(bullet)

# Клас Enemy
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, health):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = health

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40

# Клас Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Ініціалізація Pygame
pygame.init()


# Встановлення розмірів вікна та назви
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

# Завантаження зображень та звуків
img_back = "space.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
fire_sound = pygame.mixer.Sound("fire.ogg")
damage_sound = pygame.mixer.Sound("damage.mp3")

mixer.music.load("space.ogg")
mixer.music.play()

# Створення фону
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення групи спрайтів
all_sprites = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

# Створення гравця
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 30)
all_sprites.add(ship)

# Встановлення початкових значень лічильників
score = 0
missed = 0
time_s = 0

# Встановлення шрифту
font_score = pygame.font.Font("Comic.ttf", 26)
font_lost = pygame.font.Font("Comic.ttf", 40)

# Ініціалізація змінних
finish = False
run = True
start_time = time.time()
FPS = 60
clock = pygame.time.Clock()
wait_atack = 0


# Головний цикл гри
while run:
    # Перебір подій гри
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    # Оновлення гравця та ворогів
    all_sprites.update()
    

    # Перевірка зіткнень гравця та ворогів
    collisions = sprite.spritecollide(ship, monsters, False)
    if collisions and wait_atack > 5:
        wait_atack = 0
        ship.health -= 10
        damage_sound.play()
        if ship.health <= 0:
            finish = True

    # Перевірка зіткнень куль та ворогів
    bullet_collisions = sprite.groupcollide(monsters, bullets, True, True)
    for bullet_collision in bullet_collisions:
        score += 1

    # Перевірка умов перемоги та програшу
    if score >= 10:
        finish = True

    # Додавання нових ворогів
    if len(monsters) < 5 and not finish:
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), 1)
        monsters.add(monster)
        all_sprites.add(monster)

    # Відображення екрану
    if not finish:
        window.blit(background, (0, 0))
        all_sprites.draw(window)
        bullets.update()
        bullets.draw(window)
        text_score = font_score.render("Счет: " + str(score), 1, (255, 255, 255))
        text_health = font_score.render("Здоровье: " + str(ship.health), 1, (255, 255, 255))
        time_s = time.time() - start_time
        text_time = font_score.render("Время: " + str(round(time_s)), 1, (255, 255, 255))
        wait_atack = wait_atack + 0.2 #-_-
        window.blit(text_time, (10, 80))
        window.blit(text_score, (10, 20))
        window.blit(text_health, (10, 50))
    else:
        text_win = font_lost.render("Вы выйграли!", 1, (255, 0, 0))
        text_lost = font_lost.render("Вы проиграли!", 1, (255, 0, 0))
        if score >= 10:
            window.blit(text_win, (200, 200))
        else:
            window.blit(text_lost, (200, 200))



    # Оновлення екрану
    display.update()

    # Затримка
    clock.tick(FPS)

# Завершення Pygame
pygame.quit()

