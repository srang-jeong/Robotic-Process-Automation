import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker Game")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

class Ball:
    def __init__(self):
        self.size = BALL_SIZE
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5.0
        self.speed_y = -5.0
    
    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.size)
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # 벽 충돌 처리
        if self.x <= self.size or self.x >= SCREEN_WIDTH - self.size:
            self.speed_x *= -1
        if self.y <= self.size:
            self.speed_y *= -1
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5.0 * random.choice([-1, 1])
        self.speed_y = -5.0

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.active = True
        
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.create_bricks()
        
    def create_bricks(self):
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + 2) + 1
                y = row * (BRICK_HEIGHT + 2) + 50
                color = colors[row]
                self.bricks.append(Brick(x, y, color))
    
    def check_collision(self):
        # 패들과 공 충돌
        if (self.ball.y + self.ball.size >= self.paddle.y and 
            self.ball.x >= self.paddle.x and 
            self.ball.x <= self.paddle.x + self.paddle.width):
            self.ball.speed_y *= -1
            # 패들 위치에 따른 공의 방향 조정
            relative_intersect_x = (self.paddle.x + self.paddle.width/2) - self.ball.x
            normalized_intersect_x = relative_intersect_x / (self.paddle.width/2)
            self.ball.speed_x = -normalized_intersect_x * 7
            
        # 벽돌과 공 충돌
        for brick in self.bricks:
            if brick.active:
                if (self.ball.x + self.ball.size >= brick.x and 
                    self.ball.x - self.ball.size <= brick.x + brick.width and
                    self.ball.y + self.ball.size >= brick.y and 
                    self.ball.y - self.ball.size <= brick.y + brick.height):
                    brick.active = False
                    self.ball.speed_y *= -1
                    self.score += 10
                    
        # 공이 화면 아래로 떨어졌을 때
        if self.ball.y >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()
    
    def draw(self):
        screen.fill(BLACK)
        
        # 게임 요소들 그리기
        self.paddle.draw()
        self.ball.draw()
        for brick in self.bricks:
            brick.draw()
            
        # 점수와 생명력 표시 (한글 지원 폰트 사용)
        try:
            # Windows의 기본 한글 폰트 사용
            font = pygame.font.SysFont("malgungothic", 36)
        except:
            try:
                # 다른 한글 폰트 시도
                font = pygame.font.SysFont("nanumgothic", 36)
            except:
                # 기본 폰트 사용 (한글이 깨질 수 있음)
                font = pygame.font.Font(None, 36)
        
        score_text = font.render(f"점수: {self.score}", True, WHITE)
        lives_text = font.render(f"생명: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        if self.game_over:
            game_over_text = font.render("게임 오버! R키로 재시작", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
            
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.__init__()
            
            if not self.game_over:
                # 키보드 입력 처리
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.paddle.move("left")
                if keys[pygame.K_RIGHT]:
                    self.paddle.move("right")
                
                # 공 이동
                self.ball.move()
                
                # 충돌 검사
                self.check_collision()
                
                # 승리 조건 확인
                if all(not brick.active for brick in self.bricks):
                    self.create_bricks()
                    self.ball.reset()
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()