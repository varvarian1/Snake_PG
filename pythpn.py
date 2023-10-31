import pygame as pg
from random import randrange

# Переменные и функции (остаются неизменными)

window = 700
size = 25
range_ = (size // 2, window - size // 2, size) 
random_position = lambda: [randrange(*range_), randrange(*range_)]
snake = pg.rect.Rect([0, 0, size - 2, size - 2])
snake.center = random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = random_position()
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
count = 0
record = 0
pg.font.init()
font = pg.font.SysFont('Arial', 24)
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Объявляем, что будем использовать глобальную переменную

def show_start_screen():
    global record  
    font_large = pg.font.SysFont('Arial', 36)
    text1 = font_large.render("Snake Game", True, (255, 255, 255))
    text2 = font.render("Press Enter to Start", True, (255, 255, 255))
    text3 = font.render(f"Record: {record}", True, (255, 255, 255))

    # Добавлено отображение рекорда

    screen.blit(text1, (window // 2 - text1.get_width() // 2, window // 2 - 100))
    screen.blit(text2, (window // 2 - text2.get_width() // 2, window // 2))
    screen.blit(text3, (window // 2 - text3.get_width() // 2, window // 2 + 100))
    pg.display.flip()

def reset_game():
    global snake, length, segments, snake_dir, food, count
    snake.center = random_position()
    length = 1
    segments = [snake.copy()]
    snake_dir = (0, 0)
    food.center = random_position()

    # Устанавливаем новый рекорд, если текущее количество очков больше записанного рекорда

    global record
    if count > record:
        record = count
    count = 0

# Название

pg.display.set_caption("Змейка")

# Основной Цикл и Управление

running = True
game_started = False

while running:
    if game_started:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -size)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, size)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-size, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (size, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        
        screen.fill('black')

        [pg.draw.rect(screen, 'green', segment) for segment in segments]

        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1

        # Сброс флага для вывода игрока на стартовый экран

        if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or self_eating:
            reset_game()
            game_started = False

        if snake.center == food.center:
            food.center = random_position()
            length += 1
            count += 1

        pg.draw.rect(screen, 'red', food)

        count_text = font.render(f'Count: {count}', True, (255, 255, 255))
        screen.blit(count_text, (10, 10))

        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

        pg.display.flip()
        clock.tick(60)
    else:
        show_start_screen()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    reset_game()
                    game_started = True

pg.quit()