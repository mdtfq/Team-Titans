import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((905, 703))
pygame.display.set_caption("Health Runner")
Timer = pygame.time.Clock()
game_font = pygame.font.Font('Font.ttf', 50)

# Variables
score = 0
game_active = True
game_started = False  # Flag to track if the game has started
level = 1  # Track the current level
background_surface = pygame.image.load('background.png').convert_alpha()
ground_surface = pygame.Surface((905, 430))

# Text setup
text_surface = game_font.render('Start!', False, 'Black')
text_rect = text_surface.get_rect(center=(452, 50))
game_font_small = pygame.font.Font('Font.ttf', 30)

# Character and objects
MC_overweight = pygame.image.load('MC_overweight.png').convert_alpha()
MC_slimmer = pygame.image.load('MC_slimmer.png').convert_alpha()  # Slimmer character image
burger = pygame.image.load('burger.png').convert_alpha()
dumbbell = pygame.image.load('dumbbell.png').convert_alpha()  # Add dumbbell image
burger_rect = burger.get_rect(midbottom=(905, 640))  # Fixed position of the burger
dumbbell_rect = dumbbell.get_rect(midbottom=(905, 500))  # Fixed position for dumbbell spawn
MC_rect = MC_overweight.get_rect(midbottom=(100, 680))
MC_overweight_gravity = 0

# Movement speed
move_speed = 5

# Random burger spawn interval setup
burger_spawn_time = random.randint(3, 6) * 1000  # Random spawn interval between 3-6 seconds
last_burger_spawn_time = pygame.time.get_ticks()

# Random dumbbell spawn interval setup
dumbbell_spawn_time = random.randint(5, 8) * 1000  # Random spawn interval for dumbbell
last_dumbbell_spawn_time = pygame.time.get_ticks()

# Next level button
button_rect = pygame.Rect(352, 300, 200, 60)  # Center button position

def reset_game():
    global score, game_active, burger_rect, dumbbell_rect, MC_rect, burger_spawn_time, last_burger_spawn_time, dumbbell_spawn_time, last_dumbbell_spawn_time, game_started, level
    score = 0
    game_active = True
    game_started = False  # Reset the game start flag
    MC_rect.midbottom = (100, 640)
    burger_rect.midbottom = (905, 640)  # Reset burger to the fixed position
    dumbbell_rect.midbottom = (905, 500)  # Reset dumbbell to the fixed position
    burger_spawn_time = random.randint(3, 6) * 1000  # Random spawn interval between 3-6 seconds
    last_burger_spawn_time = pygame.time.get_ticks()  # Reset the timer
    dumbbell_spawn_time = random.randint(5, 8) * 1000  # Random spawn interval for dumbbell
    last_dumbbell_spawn_time = pygame.time.get_ticks()  # Reset the dumbbell timer

def display_victory_screen():
    victory_surface = game_font.render('You Win!', False, 'White')
    victory_rect = victory_surface.get_rect(center=(452, 200))
    screen.blit(victory_surface, victory_rect)
    
    # Display the Next Level button
    pygame.draw.rect(screen, (0, 255, 0), button_rect)  # Draw button
    button_text = game_font_small.render('Next Level', False, 'White')
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # If game is active, allow movement and actions
        if game_active:
            # Handle jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and MC_rect.bottom >= 680:
                    MC_overweight_gravity = -20
        # If victory screen is active, ignore all inputs except for the "Next Level" button click
        elif score == 100:  # If the player won
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                if button_rect.collidepoint(event.pos):  # If the player clicked the Next Level button
                    level += 1  # Increment the level
                    reset_game()  # Reset game state for the new level
        else:
            # Restart the game on any key press during the game over screen or victory screen
            if event.type == pygame.KEYDOWN:
                reset_game()

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 680))

        # Only show start text if the game has not started
        if not game_started:
            screen.blit(text_surface, text_rect)

        # Gravity for jumping
        MC_overweight_gravity += 1
        MC_rect.y += MC_overweight_gravity
        if MC_rect.bottom >= 680:
            MC_rect.bottom = 680

        # Character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and MC_rect.left > 0:
            MC_rect.x -= move_speed
            game_started = True  # Set the game as started when the character starts moving
        if keys[pygame.K_RIGHT] and MC_rect.right < screen.get_width():
            MC_rect.x += move_speed
            game_started = True  # Set the game as started when the character starts moving

        # Update burger position
        burger_rect.left -= 4
        if burger_rect.right <= 0:
            burger_rect.left = 905

        # Move dumbbell towards character at random intervals
        current_time = pygame.time.get_ticks()
        if level == 1:
            # Level 1 burger and dumbbell spawn intervals
            if current_time - last_dumbbell_spawn_time >= dumbbell_spawn_time:
                dumbbell_rect.midbottom = (905, 500)  # Set the dumbbell to its spawn point
                dumbbell_spawn_time = random.randint(5, 8) * 1000  # Set a new random spawn interval
                last_dumbbell_spawn_time = current_time  # Reset the timer
        else:
            # Level 2: Faster burgers and slower dumbbells
            if current_time - last_burger_spawn_time >= burger_spawn_time:
                burger_rect.midbottom = (905, 640)  # Spawn burger at fixed position
                burger_spawn_time = random.randint(1, 3) * 1000  # Faster burger spawn (1-3 seconds)
                last_burger_spawn_time = current_time  # Reset the timer

            if current_time - last_dumbbell_spawn_time >= dumbbell_spawn_time:
                dumbbell_rect.midbottom = (905, 500)  # Set the dumbbell to its spawn point
                dumbbell_spawn_time = random.randint(7, 10) * 1000  # Slower dumbbell spawn (7-10 seconds)
                last_dumbbell_spawn_time = current_time  # Reset the timer

        if dumbbell_rect.left > 0:
            dumbbell_rect.x -= 4  # Move the dumbbell toward the character

        # If dumbbell goes off-screen (missed), reset it
        if dumbbell_rect.right <= 0:
            dumbbell_rect.midbottom = (905, 500)  # Reset the dumbbell to its spawn position

        # Display character, burger, and dumbbell
        if level == 1:
            screen.blit(MC_overweight, MC_rect)  # Overweight character in level 1
        else:
            screen.blit(MC_slimmer, MC_rect)  # Slimmer character in subsequent levels
        screen.blit(burger, burger_rect)
        screen.blit(dumbbell, dumbbell_rect)

        # Adjusted collision rectangles (smaller hitboxes)
        MC_collision_rect = MC_rect.inflate(-200, -200)  # Shrinking character hitbox
        burger_collision_rect = burger_rect.inflate(-150, -150)  # Shrinking burger hitbox
        dumbbell_collision_rect = dumbbell_rect.inflate(-150, -150)  # Shrinking dumbbell hitbox

        # Collision check with burger
        if MC_collision_rect.colliderect(burger_collision_rect):
            game_active = False

        # Collision check with dumbbell
        if MC_collision_rect.colliderect(dumbbell_collision_rect):
            score += 10  # Add 10 points on collision with dumbbell
            if score > 200:  # Ensure the score doesn't exceed 200 in level 2
                score = 200
            dumbbell_rect.midbottom = (905, 500)  # Reset dumbbell to spawn location

        # Display score
        score_surface = game_font_small.render(f'Score: {score}', False, 'Black')
        screen.blit(score_surface, (10, 10))

        if score == 100:  # Victory condition for level 1
            game_active = False  # Stop the game
            display_victory_screen()  # Show victory screen
        if score == 200:  # Victory condition for level 2
            game_active = False  # Stop the game
            display_victory_screen()  # Show victory screen

    else:
        # Game over screen (if not a win)
        if score < 100:
            screen.fill((200, 0, 0))  # Red background for game over
            game_over_surface = game_font.render('Game Over', False, 'White')
            game_over_rect = game_over_surface.get_rect(center=(452, 351))
            screen.blit(game_over_surface, game_over_rect)

            score_surface = game_font_small.render(f'Final Score: {score}', False, 'White')
            score_rect = score_surface.get_rect(center=(452, 400))
            screen.blit(score_surface, score_rect)

    pygame.display.update()
    Timer.tick(60)
