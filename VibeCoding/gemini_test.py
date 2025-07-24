import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 7

# Ball
BALL_RADIUS = 7
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = -5

# Bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
bricks = []
for row in range(5):
    for col in range(10):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 25, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.x += paddle_speed

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 10
            break

    # Ball falls off screen
    if ball.bottom >= SCREEN_HEIGHT:
        lives -= 1
        if lives == 0:
            running = False
        else:
            ball.x = SCREEN_WIDTH // 2
            ball.y = SCREEN_HEIGHT // 2
            ball_speed_x = 5 * random.choice((1, -1))
            ball_speed_y = -5

    # Win condition
    if not bricks:
        running = False

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, random.choice([RED, GREEN, ORANGE, YELLOW]), brick)

    draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
    draw_text(f"Lives: {lives}", font, WHITE, screen, SCREEN_WIDTH - 100, 10)

    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

pygame.quit()