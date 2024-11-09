import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((905, 703))
pygame.display.set_caption("Health Runner")
Timer = pygame.time.Clock()
game_font = pygame.font.Font('Font.ttf', 50)
game_active = True

score = 0
game_font = pygame.font.Font('Font.ttf', 30)

background_surface = pygame.image.load('background.png').convert_alpha()
ground_surface = pygame.Surface((905, 430))

text_surface = game_font.render('Start!', False, 'Black')
text_rect = text_surface.get_rect(center=(452, 50))

MC_overweight = pygame.image.load('MC_overweight.png').convert_alpha()
MC_slimmer = pygame.image.load('MC_slimmer.png').convert_alpha()
MC_fit = pygame.image.load('MC_fit.png').convert_alpha()

dumbbell = pygame.image.load('dumbbell.png').convert_alpha()
dumbbell_rect = dumbbell.get_rect(midbottom=(905, 680))

burger = pygame.image.load('burger.png').convert_alpha()
burger_rect = burger.get_rect(midbottom=(905, 655))
burger_rect.midbottom = (905, 640)

MC_rect = MC_overweight.get_rect(midbottom=(100, 680))
MC_rect.midbottom = (100, 640)

# Define gravity for the character
MC_overweight_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and MC_rect.bottom >= 680:
                    MC_overweight_gravity = -20
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.K_SPACE:
                game_active = True

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 680))
        screen.blit(text_surface, text_rect)

        # Smaller collision rectangle for the character
        MC_collision_rect = MC_rect.inflate(-200, -200)  # Further reduced width and height

        # Smaller collision rectangle for the burger
        burger_collision_rect = burger_rect.inflate(-150, -150)  # Further reduced width and height

        # Draw rectangles for debugging (optional)
        pygame.draw.rect(screen, (255, 0, 0), MC_collision_rect, 1)  # Red for character hitbox
        pygame.draw.rect(screen, (0, 255, 0), burger_collision_rect, 1)  # Green for burger hitbox

        # Gravity and position updates for the main character
        MC_overweight_gravity += 1
        MC_rect.y += MC_overweight_gravity
        if MC_rect.bottom >= 680:
            MC_rect.bottom = 680
        screen.blit(MC_overweight, MC_rect)

        # Update dumbbell position
        dumbbell_rect.left -= 0
        if dumbbell_rect.right <= 0:
            dumbbell_rect.left = 905
        screen.blit(dumbbell, dumbbell_rect)

        # Move burger
        burger_rect.left -= 4
        if burger_rect.right <= 0:
            burger_rect.left = 905

        # Move character forward
        MC_rect.left += 1
        screen.blit(burger, burger_rect)

        # Check collision with dumbbell and update score
        if MC_collision_rect.colliderect(dumbbell_rect):
            score += 10

        # Check collision with burger to end game
        if burger_collision_rect.colliderect(MC_collision_rect):
            game_active = False

        # Display updated score
        score_surface = game_font.render(f'Score: {score}', False, 'Black')
        screen.blit(score_surface, (10, 10))

    pygame.display.update()
    Timer.tick(60)
