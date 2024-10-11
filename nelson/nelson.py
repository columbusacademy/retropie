import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Nelson Pong")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Game settings
BALL_SIZE = 20
PADDLE_WIDTH = 40
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SPEED_X = 4 * random.choice((1, -1))
BALL_SPEED_Y = 4 * random.choice((1, -1))
WINNING_SCORE = 5

# Load images
tennis_ball_img = pygame.image.load('tennis_ball.png')
dog_img = pygame.image.load('dog.png')
tennis_ball_img = pygame.transform.scale(tennis_ball_img, (BALL_SIZE, BALL_SIZE))
dog_img = pygame.transform.scale(dog_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Define positions
ball_rect = tennis_ball_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
left_paddle_rect = dog_img.get_rect(topleft=(30, HEIGHT // 2 - PADDLE_HEIGHT // 2))
right_paddle_rect = dog_img.get_rect(topright=(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2))

# Font settings
font = pygame.font.Font(None, 74)

# Initialize joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

def reset_ball():
    global ball_rect, BALL_SPEED_X, BALL_SPEED_Y
    ball_rect.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= random.choice((1, -1))
    BALL_SPEED_Y *= random.choice((1, -1))

def main():
    clock = pygame.time.Clock()
    
    left_score = 0
    right_score = 0
    game_over = False

    ball_speed_x = BALL_SPEED_X
    ball_speed_y = BALL_SPEED_Y

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    left_score, right_score = 0, 0
                    game_over = False
                    reset_ball()
            if game_over and event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:  # Button 1 for starting a new game
                    left_score, right_score = 0, 0
                    game_over = False
                    reset_ball()
        
        # Check for game over condition
        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            game_over = True
        
        if not game_over:
            # Movement controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or (len(joysticks) > 1 and joysticks[1].get_axis(1) < -0.1):
                if left_paddle_rect.top > 0:
                    left_paddle_rect.y -= PADDLE_SPEED
            if keys[pygame.K_s] or (len(joysticks) > 1 and joysticks[1].get_axis(1) > 0.1):
                if left_paddle_rect.bottom < HEIGHT:
                    left_paddle_rect.y += PADDLE_SPEED
            if keys[pygame.K_UP] or (len(joysticks) > 0 and joysticks[0].get_axis(1) < -0.1):
                if right_paddle_rect.top > 0:
                    right_paddle_rect.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] or (len(joysticks) > 0 and joysticks[0].get_axis(1) > 0.1):
                if right_paddle_rect.bottom < HEIGHT:
                    right_paddle_rect.y += PADDLE_SPEED

            # Ball movement
            ball_rect.x += ball_speed_x
            ball_rect.y += ball_speed_y

            # Ball collision with top and bottom walls
            if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
                ball_speed_y *= -1

            # Ball collision with paddles
            if ball_rect.colliderect(left_paddle_rect) or ball_rect.colliderect(right_paddle_rect):
                ball_speed_x *= -1

            # Ball goes out of bounds
            if ball_rect.left <= 0:
                right_score += 1
                reset_ball()
            if ball_rect.right >= WIDTH:
                left_score += 1
                reset_ball()

        # Fill background
        screen.fill(GREEN)

        # Draw elements
        screen.blit(tennis_ball_img, ball_rect)
        screen.blit(dog_img, left_paddle_rect)
        screen.blit(dog_img, right_paddle_rect)

        # Display score
        text_left = font.render(str(left_score), True, WHITE)
        screen.blit(text_left, (WIDTH // 4, 20))
        text_right = font.render(str(right_score), True, WHITE)
        screen.blit(text_right, (WIDTH * 3 // 4, 20))

        # Display game over message
        if game_over:
            winner = "Left Player" if left_score >= WINNING_SCORE else "Right Player"
            game_over_text = font.render(f"{winner} Wins!", True, WHITE)
            restart_text = pygame.font.Font(None, 48).render("Press SPACE or Button 1 to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        # Refresh screen
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
