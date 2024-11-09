import pygame
from sys import exit
import random


pygame.init()
screen = pygame.display.set_mode((905, 703))# sets the display screen size
pygame.display.set_caption("Health Runner")# sets the name of the game
Timer = pygame.time.Clock()
game_font = pygame.font.Font('Font.ttf', 50)#font used in the game


# Variables for the code
score = 0
game_active = True
game_started = False  # this is a flag to track if the game has started
level = 1  # this is to track the current level
background_surface = pygame.image.load('background.png').convert_alpha()
ground_surface = pygame.Surface((905, 430))


# the basic text settings
text_surface = game_font.render(f'Level {level}', False, 'Black')
text_rect = text_surface.get_rect(center=(452, 50))
game_font_small = pygame.font.Font('Font.ttf', 30)


# the character and objects for the game 
MC_overweight = pygame.image.load('MC_overweight.png').convert_alpha()# Level 1 character
MC_slimmer = pygame.image.load('MC_slimmer.png').convert_alpha()  # Slimmer character image, level 2 character
MC_fit = pygame.image.load('MC_fit.png').convert_alpha()  # Fit character image for level 3
burger = pygame.image.load('burger.png').convert_alpha()#obstacle
dumbbell = pygame.image.load('dumbbell.png').convert_alpha()  # to add dumbbell image
burger_rect = burger.get_rect(midbottom=(905, 640))  # Fixed position of the burger
dumbbell_rect = dumbbell.get_rect(midbottom=(905, 500))  # Fixed position for dumbbell spawn
MC_rect = MC_overweight.get_rect(midbottom=(100, 680))
MC_overweight_gravity = 0


# to track the movement speed
move_speed = 5


# Random burger spawn interval to make the game more difficult
burger_spawn_time = random.randint(3, 6) * 1000  # Random spawn interval set for 3-6 seconds to throw off the user
last_burger_spawn_time = pygame.time.get_ticks()


# Random dumbbell spawn interval setup
dumbbell_spawn_time = random.randint(5, 8) * 1000  # Random spawn interval for dumbbell
last_dumbbell_spawn_time = pygame.time.get_ticks()


# button to proceed to the next level
button_rect = pygame.Rect(352, 300, 200, 60)  # Center button position


# button to play the game again from the start
play_again_btn = pygame.Rect(352, 450, 200, 60)  # Position below game over text


# settings to reset the game
def reset_game():
    global score, game_active, burger_rect, dumbbell_rect, MC_rect
    global burger_spawn_time, last_burger_spawn_time, dumbbell_spawn_time
    global last_dumbbell_spawn_time, game_started
    score = 0
    game_active = True
    game_started = False
    MC_rect.midbottom = (100, 640)
    burger_rect.midbottom = (905, 640)
    dumbbell_rect.midbottom = (905, 500)
    burger_spawn_time = random.randint(3, 6) * 1000
    last_burger_spawn_time = pygame.time.get_ticks()
    dumbbell_spawn_time = random.randint(5, 8) * 1000
    last_dumbbell_spawn_time = pygame.time.get_ticks()


def display_victory_screen():
    if level == 3 and score == 300:
        # Use game background instead of black
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 680))
       
        # to display "Congratulations!"
        victory_surface = game_font.render('Congratulations!', False, 'Black')  # Changed to black text
        victory_rect = victory_surface.get_rect(center=(452, 150))
        screen.blit(victory_surface, victory_rect)
       
        #to display "You are fit!" as a victory message
        fit_surface = game_font.render('You are fit!', False, 'Black')  # Changed to black text
        fit_rect = fit_surface.get_rect(center=(452, 220))
        screen.blit(fit_surface, fit_rect)
       
        # Display Play Again button
        pygame.draw.rect(screen, (0, 255, 0), button_rect)
        button_text = game_font_small.render('Play Again', False, 'White')
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
    else:
        # A victory screen for levels 1 and 2
        victory_surface = game_font.render('You Win!', False, 'White')
        victory_rect = victory_surface.get_rect(center=(452, 200))
        screen.blit(victory_surface, victory_rect)
       
        pygame.draw.rect(screen, (0, 255, 0), button_rect)
        button_text = game_font_small.render('Next Level', False, 'White')
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)


def display_game_over_screen():
    screen.fill((200, 0, 0))
    game_over_surface = game_font.render('You Lost!', False, 'White')
    game_over_rect = game_over_surface.get_rect(center=(452, 351))
    screen.blit(game_over_surface, game_over_rect)


    score_surface = game_font_small.render(f'Final Score: {score}', False, 'White')
    score_rect = score_surface.get_rect(center=(452, 400))
    screen.blit(score_surface, score_rect)
   
    # TO Draw Play Again button setup
    pygame.draw.rect(screen, (0, 255, 0), play_again_btn)
    play_again_text = game_font_small.render('Play Again', False, 'White')
    play_again_rect = play_again_text.get_rect(center=play_again_btn.center)
    screen.blit(play_again_text, play_again_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        # If game is active, allow use of movement and actions
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and MC_rect.bottom >= 680:
                    MC_overweight_gravity = -20
        # If victory screen is active, handle Next Level button
        elif (score == 100 and level == 1) or (score == 200 and level == 2) or (score == 300 and level == 3):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    if level == 3 and score == 300:
                        # Reset to level 1 when completing the game
                        level = 1
                        reset_game()
                    else:
                        # Progress to next level
                        level += 1
                        reset_game()
        # If game over screen is active, handle Play Again button
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_btn.collidepoint(event.pos):
                    level = 1  # Reset to level 1
                    reset_game()


    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 680))


        # Display level number always visible
        level_surface = game_font.render(f'Level {level}', False, 'Black')
        level_rect = level_surface.get_rect(center=(452, 50))
        screen.blit(level_surface, level_rect)


        # for displaying score of the character
        score_surface = game_font_small.render(f'Score: {score}', False, 'Black')
        screen.blit(score_surface, (10, 10))


        # Gravity for jumping
        MC_overweight_gravity += 1
        MC_rect.y += MC_overweight_gravity
        if MC_rect.bottom >= 680:
            MC_rect.bottom = 680


        # Character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and MC_rect.left > 0:
            MC_rect.x -= move_speed
            game_started = True  # Sets the game as started when the character starts moving
        if keys[pygame.K_RIGHT] and MC_rect.right < screen.get_width():
            MC_rect.x += move_speed
            game_started = True  # Set the game as started when the character starts moving


        # Update burger position - faster in level 2
        burger_speed = 4 if level == 1 else 7 if level == 2 else 10
        burger_rect.left -= burger_speed
        if burger_rect.right <= -50:
            burger_rect.left = screen.get_width()


        # Move dumbbell - faster in level 3
        dumbbell_speed = 4 if level == 1 else 7 if level == 2 else 10
        dumbbell_rect.x -= dumbbell_speed  # Always move the dumbbell


        current_time = pygame.time.get_ticks()
        if level == 1:
            if current_time - last_dumbbell_spawn_time >= dumbbell_spawn_time and dumbbell_rect.right <= -50:
                dumbbell_rect.left = screen.get_width()
                dumbbell_spawn_time = random.randint(5, 8) * 1000
                last_dumbbell_spawn_time = current_time
        elif level == 2:
            if current_time - last_burger_spawn_time >= burger_spawn_time and burger_rect.right <= -50:
                burger_rect.left = screen.get_width()
                burger_spawn_time = random.randint(1, 3) * 1000
                last_burger_spawn_time = current_time


            if current_time - last_dumbbell_spawn_time >= dumbbell_spawn_time and dumbbell_rect.right <= -50:
                dumbbell_rect.left = screen.get_width()
                dumbbell_spawn_time = random.randint(7, 10) * 1000
                last_dumbbell_spawn_time = current_time
        else:  # Level 3
            if current_time - last_burger_spawn_time >= burger_spawn_time and burger_rect.right <= -50:
                burger_rect.left = screen.get_width()
                burger_spawn_time = random.randint(1, 2) * 1000
                last_burger_spawn_time = current_time


            if current_time - last_dumbbell_spawn_time >= dumbbell_spawn_time and dumbbell_rect.right <= -50:
                dumbbell_rect.left = screen.get_width()
                dumbbell_spawn_time = random.randint(4, 6) * 1000
                last_dumbbell_spawn_time = current_time


        # Display character, burger, and dumbbell
        if level == 1:
            screen.blit(MC_overweight, MC_rect)  # Overweight character in level 1
        elif level == 2:
            screen.blit(MC_slimmer, MC_rect)  # Slimmer character in level 2
        else:
            screen.blit(MC_fit, MC_rect)  # Fit character in level 3


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
            score += 10
            if score > 300:  # Ensure the score doesn't exceed 300 in level 3
                score = 300
            dumbbell_rect.midbottom = (905, 500)


        # Victory conditions for all levels
        if score == 100 and level == 1:  # Victory condition for level 1
            game_active = False
            display_victory_screen()
        elif score == 200 and level == 2:  # Victory condition for level 2
            game_active = False
            display_victory_screen()
        elif score == 300 and level == 3:  # Victory condition for level 3
            game_active = False
            display_victory_screen()


    else:
        if MC_collision_rect.colliderect(burger_collision_rect) or score < 100 * level:
            display_game_over_screen()
        else:
            # Display victory screen
            display_victory_screen()


    pygame.display.update()
    Timer.tick(60)







