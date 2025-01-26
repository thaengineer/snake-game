import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Set clock
clock = pygame.time.Clock()

# Set snake parameters
snake_block = 10
snake_speed = 15

# Set font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def read_highscore():
    try:
        with open("score.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def write_highscore(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0
    last_direction = None

    snake_List = []
    Length_of_snake = 1
    score = 0
    highscore = read_highscore()

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    last_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and last_direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    last_direction = 'RIGHT'
                elif event.key == pygame.K_UP and last_direction != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    last_direction = 'UP'
                elif event.key == pygame.K_DOWN and last_direction != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    last_direction = 'DOWN'

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)

        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        # Draw the food
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])

        # Display the score
        score_text = font_style.render(f"Score: {score}", True, white)
        display.blit(score_text, [10, 10])

        # Display the high score
        highscore_text = font_style.render(f"Highscore: {highscore}", True, white)
        display.blit(highscore_text, [(width - highscore_text.get_width()) // 2, 10])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            if Length_of_snake % 10 == 0:
                score += 60  # Award 60 points for every 10th apple
            else:
                score += 10  # Increment score by 10 for each apple
            if score > highscore:
                highscore = score
                write_highscore(highscore)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()