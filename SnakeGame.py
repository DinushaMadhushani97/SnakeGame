import pygame
import random

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)
dark_blue = (0, 0, 102)
light_red = (255, 102, 102)
light_green = (102, 255, 102)

# Screen dimensions
width = 800
height = 600

# Create the game screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Enhanced Snake Game by Dinusha')

# Set clock speed
clock = pygame.time.Clock()

# Snake block size and initial speed
block_size = 20
initial_speed = 10

# Font styles
font_style = pygame.font.SysFont('Arial', 30, bold=True)
score_font = pygame.font.SysFont('Arial', 25)

# Function to display score
def display_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [10, 10])

# Function to draw the snake
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], block_size, block_size])

# Function to display messages on screen
def message(msg, color, y_displace=0):
    msg_surface = font_style.render(msg, True, color)
    msg_rect = msg_surface.get_rect(center=(width / 2, height / 2 + y_displace))
    screen.blit(msg_surface, msg_rect)

# Button function to create clickable buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)

    # Draw button with hover effect
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, ac, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, button_rect)

    # Add text to the button
    text = score_font.render(msg, True, black)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# Start game function
def start_game():
    game_loop()

# Quit game function
def quit_game():
    pygame.quit()
    quit()

# Pause game function
def pause():
    paused = True
    while paused:
        screen.fill(dark_blue)
        message("Paused", yellow, -50)
        message("Press C to Continue or Q to Quit", white, 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = width // 2
    y = height // 2

    # Snake movement
    x_change = 0
    y_change = 0

    # Initial snake body and length
    snake_list = []
    length_of_snake = 1

    # Initial speed
    speed = initial_speed

    # Food position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:

        while game_close:
            screen.fill(dark_blue)
            message("You Lost!", red, -50)
            message("Press C to Play Again or Q to Quit", white, 50)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0
                elif event.key == pygame.K_p:
                    pause()  # Pause the game

        # Check for boundaries
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        # Update position
        x += x_change
        y += y_change
        screen.fill(dark_blue)  # Better background color
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        # Snake growth mechanism
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check collision with self
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Draw snake and display score
        draw_snake(block_size, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        # Check if the snake has eaten the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            length_of_snake += 1
            speed += 1  # Increase speed for added difficulty

        clock.tick(speed)

    pygame.quit()
    quit()

# Main menu with buttons
def game_intro():
    intro = True
    while intro:
        screen.fill(blue)
        message("Welcome to the Enhanced Snake Game!", white, -100)
        button("Start", 150, 450, 150, 60, light_green, green, start_game)
        button("Quit", 550, 450, 150, 60, light_red, red, quit_game)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False

# Start the game intro
game_intro()
