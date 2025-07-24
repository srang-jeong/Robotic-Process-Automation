import pygame
import sys

# 게임 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 게임 설정
clock = pygame.time.Clock()
FPS = 60

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
        
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # 벽 충돌 처리
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= self.radius:
            self.speed_y = -self.speed_y
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5

class Brick:
    def __init__(self, x, y, color):
        self.width = 75
        self.height = 30
        self.x = x
        self.y = y
        self.color = color
        self.destroyed = False
    
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def create_bricks():
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
    
    for row in range(5):
        for col in range(10):
            x = col * 80 + 10
            y = row * 35 + 50
            color = colors[row % len(colors)]
            bricks.append(Brick(x, y, color))
    
    return bricks

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    
    running = True
    
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")
        
        # 공 이동
        ball.move()
        
        # 패들과 공 충돌 검사
        if ball.get_rect().colliderect(paddle.get_rect()) and ball.speed_y > 0:
            ball.speed_y = -ball.speed_y
            # 패들의 어느 부분에 맞았는지에 따라 각도 조정
            hit_pos = (ball.x - paddle.x) / paddle.width
            ball.speed_x = 8 * (hit_pos - 0.5)
        
        # 벽돌과 공 충돌 검사
        for brick in bricks:
            if not brick.destroyed and ball.get_rect().colliderect(brick.get_rect()):
                brick.destroyed = True
                ball.speed_y = -ball.speed_y
                score += 10
                break
        
        # 공이 바닥에 떨어졌을 때
        if ball.y > SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0:
                # 게임 오버
                ball.reset()
                bricks = create_bricks()
                score = 0
                lives = 3
            else:
                ball.reset()
        
        # 모든 벽돌이 파괴되었을 때
        if all(brick.destroyed for brick in bricks):
            bricks = create_bricks()
            ball.reset()
        
        # 화면 그리기
        screen.fill(WHITE)
        
        # 게임 객체 그리기
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        
        # UI 그리기
        score_text = font.render(f"점수: {score}", True, BLACK)
        lives_text = font.render(f"생명: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()