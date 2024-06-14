import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)

# Шрифты
font = pygame.font.Font(None, 36)

# Игровые объекты
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('C:/Work/learn/spaceg/images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))  # Уменьшение размера модели игрока
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.invincible = False
        self.invincible_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничение движения игрока в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # Обработка состояния неуязвимости
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_time > 2000:  # Неуязвимость длится 2 секунды
                self.invincible = False
                self.image.set_alpha(255)  # Восстановить полную непрозрачность

    def take_damage(self):
        self.invincible = True
        self.invincible_time = pygame.time.get_ticks()
        self.image.set_alpha(128)  # Сделать корабль полупрозрачным

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20, 70)
        self.image = pygame.image.load('C:/Work/learn/spaceg/images/meteor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - size)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(3, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('C:/Work/learn/spaceg/images/heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 30))  # Уменьшение размера сердца, если необходимо
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    button_color = WHITE
    button_hover_color = GREEN
    button_click_color = BLUE
    buttons = [
        {"text": "Start Game", "rect": pygame.Rect(20, 60, 200, 40), "action": game},
        {"text": "High Scores", "rect": pygame.Rect(20, 100, 200, 40), "action": high_scores},
        {"text": "Register", "rect": pygame.Rect(20, 140, 200, 40), "action": register},
        {"text": "Exit", "rect": pygame.Rect(20, 180, 200, 40), "action": sys.exit}
    ]

    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, 20, 20)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for button in buttons:
            color = button_color
            if button["rect"].collidepoint(mouse_pos):
                color = button_hover_color
                if mouse_click[0]:
                    color = button_click_color
                    button["action"]()

            pygame.draw.rect(screen, color, button["rect"])
            draw_text(button["text"], font, BLACK, screen, button["rect"].x + 10, button["rect"].y + 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game():
    all_sprites = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    hearts = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(10):
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors.add(meteor)

    running = True
    clock = pygame.time.Clock()
    lives = 3  # Количество жизней игрока
    score = 0  # Счет игрока
    start_time = pygame.time.get_ticks()
    last_heart_spawn_time = pygame.time.get_ticks()

    # Загрузка фона
    background = pygame.image.load('C:/Work/learn/spaceg/images/spaceback.png').convert()
    background_rect1 = background.get_rect()
    background_rect2 = background.get_rect()
    background_rect2.y = -background_rect2.height

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Обновление спрайтов
        all_sprites.update()

        # Обновление фона
        background_rect1.y += 2
        background_rect2.y += 2
        if background_rect1.top >= screen_height:
            background_rect1.y = background_rect2.y - background_rect1.height
        if background_rect2.top >= screen_height:
            background_rect2.y = background_rect1.y - background_rect2.height

        # Проверка на столкновение пуль с метеоритами
        hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
        for hit in hits:
            score += 1
            meteor = Meteor()
            all_sprites.add(meteor)
            meteors.add(meteor)

        # Проверка на столкновение игрока с метеоритами
        if not player.invincible and pygame.sprite.spritecollideany(player, meteors):
            lives -= 1
            player.take_damage()
            if lives == 0:
                running = False

        # Проверка на столкновение игрока с сердечками
        heart_hits = pygame.sprite.spritecollide(player, hearts, True)
        for heart in heart_hits:
            lives += 1

        # Спавн сердечек
        current_time = pygame.time.get_ticks()
        if current_time - last_heart_spawn_time > 10000:  # Раз в минуту
            heart = Heart()
            all_sprites.add(heart)
            hearts.add(heart)
            last_heart_spawn_time = current_time

        # Вычисление времени игры
        elapsed_time = (current_time - start_time) // 1000  # Время в секундах

        # Отрисовка
        screen.fill(BLACK)
        screen.blit(background, background_rect1)
        screen.blit(background, background_rect2)
        all_sprites.draw(screen)

        # Отрисовка количества жизней, счета и времени игры
        draw_text(f'Lives: {lives}', font, WHITE, screen, 10, 10)
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 40)
        draw_text(f'Time: {elapsed_time}s', font, WHITE, screen, 10, 70)

        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

    main_menu()

def high_scores():
    # Здесь будет код для отображения рекордов
    pass

def register():
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно

    email = simpledialog.askstring("Registration", "Enter your email:")
    if email:
        print(f"Registered with email: {email}")
        # Здесь можно добавить код для сохранения email или отправки его на сервер

    root.destroy()

main_menu()