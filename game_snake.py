from random import randint
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Змейка')
pygame.display.set_icon(pygame.image.load("game_images/ava.png"))

bg = pygame.image.load('game_images/bg.png').convert_alpha()
body = pygame.image.load('game_images/snake_body.png').convert_alpha()
face = pygame.image.load('game_images/snake_face.png').convert_alpha()
death = pygame.image.load('game_images/death.png').convert_alpha()
apple = pygame.image.load('game_images/apple.png').convert_alpha()
replay = pygame.image.load("game_images/replay.png").convert_alpha()

font = pygame.font.Font('game_fonts/font.otf', 40)

ap = pygame.mixer.Sound('game_songs/ap.mp3')


def prov():
    global x_y_apple, body_snake
    for j in range(len(body_snake)):
        if x_y_apple == body_snake[j]:
            x_y_apple = [randint(0, 17), randint(0, 17)]
            prov()


x_y_apple = [randint(9, 14), randint(3, 14)]
x_y_snake = [randint(3, 8), randint(3, 14)]
body_snake = [[x_y_snake[0], x_y_snake[1]]]
rotation = randint(0, 3)
match rotation:
    case 0: body_snake.insert(0, [x_y_snake[0] - 1, x_y_snake[1]])
    case 1: body_snake.insert(0, [x_y_snake[0], x_y_snake[1] + 1])
    case 2: body_snake.insert(0, [x_y_snake[0] + 1, x_y_snake[1]])
    case 3: body_snake.insert(0, [x_y_snake[0], x_y_snake[1] - 1])
last_body = body_snake[0]
score = 0
flag = 0
prov()

with open(f'record', 'r') as file:
    best_score = file.read()

mouse = False
play = True
running = True
while running:

    screen.blit(bg, (0, 0))
    score_text = font.render(f'Счёт: {score}', True, 'white')
    if int(best_score) >= score:
        record_text = font.render(f'Рекорд: {best_score}', True, 'white')
    else:
        best_score = score
        record_text = font.render(f'Рекорд: {best_score}', True, 'white')
        with open(f'record', 'w') as file:
            file.write(str(best_score))
    screen.blit(score_text, (50, 1))
    screen.blit(record_text, (300, 1))
    screen.blit(replay, (900, 1))
    replay_rect = replay.get_rect(topleft=(900, 1))

    if replay_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        mouse = True
    elif mouse and not pygame.mouse.get_pressed()[0]:
        x_y_apple = [randint(9, 14), randint(3, 14)]
        x_y_snake = [randint(3, 8), randint(3, 14)]
        rotation = randint(0, 3)
        match rotation:
            case 0:
                body_snake = [[x_y_snake[0] - 1, x_y_snake[1]], [x_y_snake[0], x_y_snake[1]]]
            case 1:
                body_snake = [[x_y_snake[0], x_y_snake[1] + 1], [x_y_snake[0], x_y_snake[1]]]
            case 2:
                body_snake = [[x_y_snake[0] + 1, x_y_snake[1]], [x_y_snake[0], x_y_snake[1]]]
            case 3:
                body_snake = [[x_y_snake[0], x_y_snake[1] - 1], [x_y_snake[0], x_y_snake[1]]]
        last_body = body_snake[0]
        score = 0
        play = True
        mouse = False

    if play:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and rotation != 3 and body_snake[-1][1] <= body_snake[-2][1]:
            rotation = 1
        elif keys[pygame.K_a] and rotation != 0 and body_snake[-1][0] <= body_snake[-2][0]:
            rotation = 2
        elif keys[pygame.K_s] and rotation != 1 and body_snake[-1][1] >= body_snake[-2][1]:
            rotation = 3
        elif keys[pygame.K_d] and rotation != 2 and body_snake[-1][0] >= body_snake[-2][0]:
            rotation = 0

    screen.blit(apple, (50 + (x_y_apple[0] * 50), 55 + (x_y_apple[1] * 50)))
    apple_rect = apple.get_rect(topleft=(50 + (x_y_apple[0] * 50), 55 + (x_y_apple[1] * 50)))
    for i in range(len(body_snake)):
        if i == len(body_snake) - 1:
            if play:
                screen.blit(pygame.transform.rotate(face, rotation * 90),
                            (50 + (body_snake[i][0] * 50), 55 + (body_snake[i][1] * 50)))
            else:
                screen.blit(pygame.transform.rotate(death, rotation * 90),
                            (50 + (body_snake[i][0] * 50), 55 + (body_snake[i][1] * 50)))
        else:
            screen.blit(body, (50 + (body_snake[i][0] * 50), 55 + (body_snake[i][1] * 50)))
    face_rect = face.get_rect(topleft=(50 + (body_snake[-1][0] * 50), 55 + (body_snake[-1][1] * 50)))

    if face_rect.colliderect(apple_rect):
        body_snake.insert(0, last_body)
        x_y_apple = body_snake[1]
        score += 1
        ap.play()
        prov()

    if play and flag % 80 == 0:
        match rotation:
            case 1:
                if 0 <= body_snake[-1][1] - 1 <= 17:
                    for i in range(len(body_snake) - 1):
                        if [body_snake[-1][0], body_snake[-1][1] - 1] == body_snake[i]:
                            play = False
                    if play:
                        body_snake.append([body_snake[-1][0], body_snake[-1][1] - 1])
                        last_body = body_snake[0]
                        body_snake.pop(0)
                else:
                    play = False
            case 2:
                if 0 <= body_snake[-1][0] - 1 <= 17:
                    for i in range(len(body_snake) - 1):
                        if [body_snake[-1][0] - 1, body_snake[-1][1]] == body_snake[i]:
                            play = False
                    if play:
                        body_snake.append([body_snake[-1][0] - 1, body_snake[-1][1]])
                        last_body = body_snake[0]
                        body_snake.pop(0)
                else:
                    play = False
            case 3:
                if 0 <= body_snake[-1][1] + 1 <= 17:
                    for i in range(len(body_snake) - 1):
                        if [body_snake[-1][0], body_snake[-1][1] + 1] == body_snake[i]:
                            play = False
                    if play:
                        body_snake.append([body_snake[-1][0], body_snake[-1][1] + 1])
                        last_body = body_snake[0]
                        body_snake.pop(0)
                else:
                    play = False
            case 0:
                if 0 <= body_snake[-1][0] + 1 <= 17:
                    for i in range(len(body_snake) - 1):
                        if [body_snake[-1][0] + 1, body_snake[-1][1]] == body_snake[i]:
                            play = False
                    if play:
                        body_snake.append([body_snake[-1][0] + 1, body_snake[-1][1]])
                        last_body = body_snake[0]
                        body_snake.pop(0)
                else:
                    play = False

    pygame.display.update()
    flag += 0.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
