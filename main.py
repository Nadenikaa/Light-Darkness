import pygame
import keyboard

pygame.init()
SPEED = 0.6
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Свет и Тьма")
font = pygame.font.Font(None, 36)  # Шрифт для текста

# цвета
white = (255, 255, 255)
green = (102, 190, 102)
pink = (0, 51, 0)
end_rect = pygame.Rect(760, 560, 40, 40)
end_rect_light = pygame.Rect(0, 0, 10, 10)
end_rect_darkness = pygame.Rect(0, 0, 10, 10)


def load_level(filename):
    level = []
    with open(filename, 'r') as f:
        for line in f:
            row = line.strip().split(', ')  # Удаляем '\n' и разбиваем строку
            if row:  # Проверка на пустую строку
                level.append([int(x) for x in row])  # Преобразуем элементы в целые числа
        return level


LEVEL = load_level('level1.txt')
LEVEL2 = load_level('level2.txt')
LEVEL3 = load_level('level3.txt')
LEVEL4 = load_level('level4.txt')
LEVEL5 = load_level('level5.txt')
levels = [LEVEL, LEVEL2, LEVEL3, LEVEL4, LEVEL5]


def draw_start_screen():
    background_image = pygame.image.load('start.jpg')
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:  # добавлено условие running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_start = False

    background_image = pygame.image.load('hello.jpg')
    screen.blit(background_image, (0, 0))
    pygame.display.flip()
    waiting_for_start = True
    while waiting_for_start:  # добавлено условие running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_start = False
    background_image = pygame.image.load('rule.jpg')
    screen.blit(background_image, (0, 0))
    pygame.display.flip()


def check_win():
    return light.rect.colliderect(end_rect_light) and darkness.rect.colliderect(end_rect_darkness)


def draw_results_screen():
    background_image = pygame.image.load('result.jpg')
    screen.blit(background_image, (0, 0))
    text = font.render("Собрано:", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, 200))
    screen.blit(text, text_rect)
    line1 = "Свет:" + str(score_light) + ' из 3'
    line2 = "Тьма:" + str(score_darkness) + ' из 3'
    text = font.render(line1, True, white)
    text_rect = text.get_rect(center=(250, 250))
    screen.blit(text, text_rect)
    text = font.render(line2, True, white)
    text_rect = text.get_rect(center=(550, 250))

    screen.blit(text, text_rect)
    pygame.display.flip()


def draw_end_screen():
    background_image = pygame.image.load('end.jpg')
    screen.blit(background_image, (0, 0))
    pygame.display.flip()


class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = SPEED

    def update(self):
        self.dx = 0
        self.dy = 0
        if keyboard.is_pressed('A'):
            self.dx -= 1
        if keyboard.is_pressed('D'):
            self.dx += 1
        if keyboard.is_pressed('W'):
            self.dy -= 1
        if keyboard.is_pressed('s'):
            self.dy += 1

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        self.rect.clamp_ip(0, 0, 800, 600)
        # Проверка столкновений
        self.check_collision(current_level)

    def check_collision(self, current_level):  # dx и dy передаются как аргументы
        global end_rect_light
        global score_light
        level = levels[current_level]
        for row in range(len(level)):
            for col in range(len(level[row])):
                if level[row][col] == 2:
                    end_rect_light = pygame.Rect(col * title_wight, row * tile_hight, 40, 40)
                    if self.rect.colliderect(end_rect_light):  # Более быстрая проверка
                        self.rect.x = col * title_wight
                        self.rect.y = row * tile_hight
                if level[row][col] == 1:
                    wall_rect = pygame.Rect(col * title_wight, row * tile_hight, title_wight, tile_hight)
                    if self.rect.colliderect(wall_rect):  # Более быстрая проверка
                        self.rect.x -= self.dx * self.speed
                        self.rect.y -= self.dy * self.speed
                if level[row][col] == 4:  # Проверка на столкновение с целью (4)
                    target_rect = pygame.Rect(col * title_wight, row * tile_hight, title_wight, tile_hight)
                    if self.rect.colliderect(target_rect):
                        level[row][col] = 0
                        score_light += 1


class Darkness(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = SPEED

    def update(self):
        self.dx = 0
        self.dy = 0
        if keyboard.is_pressed('left'):
            self.dx -= 1
        if keyboard.is_pressed('right'):
            self.dx += 1
        if keyboard.is_pressed('up'):
            self.dy -= 1
        if keyboard.is_pressed('down'):
            self.dy += 1

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        self.rect.clamp_ip(0, 0, 800, 600)
        # Проверка столкновений
        self.check_collision(current_level)

    def check_collision(self, current_level):  # dx и dy передаются как аргументы
        global end_rect_darkness
        global score_darkness
        level = levels[current_level]
        for row in range(len(level)):
            for col in range(len(level[row])):
                if level[row][col] == 3:
                    end_rect_darkness = pygame.Rect(col * title_wight, row * tile_hight, title_wight, tile_hight)
                    if self.rect.colliderect(end_rect_darkness):  # Более быстрая проверка
                        self.rect.x = col * title_wight
                        self.rect.y = row * tile_hight
                if level[row][col] == 1:
                    wall_rect = pygame.Rect(col * title_wight, row * tile_hight, title_wight, tile_hight)
                    if self.rect.colliderect(wall_rect):  # Более быстрая проверка
                        self.rect.x -= self.dx * self.speed
                        self.rect.y -= self.dy * self.speed
                if level[row][col] == 5:  # Проверка на столкновение с целью (4)
                    target_rect = pygame.Rect(col * title_wight, row * tile_hight, title_wight, tile_hight)
                    if self.rect.colliderect(target_rect):
                        level[row][col] = 0
                        score_darkness += 1


tile_hight = 40
title_wight = 40


def draw_level(current_level):
    level = levels[current_level]
    for row in range(len(level)):
        for col in range(len(level[row])):
            x = col * title_wight
            y = row * tile_hight
            if level[row][col] == 1:
                pygame.draw.rect(screen, pink, (col * title_wight, row * tile_hight, title_wight, tile_hight))
            elif level[row][col] == 2:
                screen.blit(pygame.image.load('portal_light.png').convert_alpha(), (x, y))
            elif level[row][col] == 3:
                screen.blit(pygame.image.load('portal_darkness.png').convert_alpha(), (x, y))
            elif level[row][col] == 4:
                screen.blit(pygame.image.load('light_diamond.png').convert_alpha(), (x, y))
            elif level[row][col] == 5:
                screen.blit(pygame.image.load('darkness_diamond.png').convert_alpha(), (x, y))


running = True
draw_start_screen()

# Ожидание нажатия Enter перед началом игры
waiting_for_start = True
while waiting_for_start and running:  # добавлено условие running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting_for_start = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting_for_start = False

current_level = 0
while running:
    if current_level < len(levels):
        running_game = True
        score_light = 0
        score_darkness = 0
        light = Light(40, 40, 'light.png')
        darkness = Darkness(680, 40, 'darkness.png')
        all_sprites = pygame.sprite.Group()  # Создаем группу спрайтов вне цикла
        all_sprites.add(light)
        all_sprites.add(darkness)

        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    running_game = False
            all_sprites.update()
            # screen.blit(background_image, (0, 0))
            screen.fill(green)

            draw_level(current_level)
            all_sprites.draw(screen)

            pygame.display.flip()

            if check_win():
                draw_results_screen()
                current_level += 1  # Переход к следующему уровню
                running_game = False  # Выход из игрового цикла

                # Ожидание нажатия клавиши Enter для следующего уровня
                waiting_for_next_level = True
                while waiting_for_next_level and running:  # добавлено условие running
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_next_level = False
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            waiting_for_next_level = False
                            break
    else:
        draw_end_screen()
        running = False
        waiting_for_next_level = True
        while waiting_for_next_level:  # добавлено условие running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_next_level = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_next_level = False
                    break

pygame.quit()
