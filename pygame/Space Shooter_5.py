import pygame
import random
import sys
import os
import math

# --- 화면 및 게임 설정 ---
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
FPS = 60
TOTAL_STAGE = 5

# --- 리소스 경로 및 이미지 크기 설정 ---
ASSETS = "assets/"
IMG_PLAYER = ASSETS + "player_ship.png"
IMG_ENEMY1 = ASSETS + "enemy1.png"
IMG_ENEMY2 = ASSETS + "enemy2.png"
IMG_BOSS = ASSETS + "boss.png"
IMG_BULLET = ASSETS + "bullet.png"
IMG_ENEMY_BULLET = ASSETS + "enemy_bullet.png"
IMG_POWERUP_SHIELD = ASSETS + "powerup_shield.png"
IMG_POWERUP_MULTI = ASSETS + "powerup_multi.png"
BGM = ASSETS + "bgm.mp3"
SFX_SHOOT = ASSETS + "sfx_shoot.wav"
SFX_EXPLODE = ASSETS + "sfx_explode.wav"
SFX_POWERUP = ASSETS + "sfx_powerup.wav"
SFX_SHIELD = ASSETS + "sfx_shield.wav"
SFX_BOSS = ASSETS + "sfx_boss.wav"

PLAYER_SIZE = (40, 30)
ENEMY1_SIZE = (40, 30)
ENEMY2_SIZE = (40, 30)
BOSS_SIZE = (80, 60)
BULLET_SIZE = (12, 24)
ENEMY_BULLET_SIZE = (12, 24)
POWERUP_SIZE = (32, 32)

# --- 별 배경 클래스 ---
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH-1)
        self.y = random.randint(0, SCREEN_HEIGHT-1)
        self.speed = random.randint(1, 2)
        self.size = random.randint(1, 2)
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.x = random.randint(0, SCREEN_WIDTH-1)
            self.y = 0
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.size)

# --- 폭죽 파티클 클래스 ---
class FireworkParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.radius = random.randint(3, 6)
        self.color = random.choice([
            (255, 80, 80), (80, 255, 80), (80, 80, 255),
            (255, 255, 80), (255, 80, 255), (80, 255, 255),
            (255, 128, 0), (255, 255, 255)
        ])
        self.life = random.randint(20, 30)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.12
        self.life -= 1
        self.radius = max(1, self.radius - 0.1)
    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

# --- 플레이어 클래스 ---
class Player:
    def __init__(self, img):
        self.img = img
        self.w = img.get_width()
        self.h = img.get_height()
        self.x = SCREEN_WIDTH // 2 - self.w // 2
        self.y = SCREEN_HEIGHT - self.h - 20
        self.speed = 5
        self.lives = 3
        self.cooldown = 0
        self.shield = 0
        self.multi = 0
        self.score = 0
    def move(self, dx, dy):
        self.x = max(0, min(SCREEN_WIDTH - self.w, self.x + dx))
        self.y = max(0, min(SCREEN_HEIGHT - self.h, self.y + dy))
    def move_to_cursor(self, mx, my, instant=False):
        cx = mx - self.w // 2
        cy = my - self.h // 2
        if instant:
            self.x = max(0, min(SCREEN_WIDTH - self.w, cx))
            self.y = max(0, min(SCREEN_HEIGHT - self.h, cy))
        else:
            self.x += int((cx - self.x) * 0.3)
            self.y += int((cy - self.y) * 0.3)
            self.x = max(0, min(SCREEN_WIDTH - self.w, self.x))
            self.y = max(0, min(SCREEN_HEIGHT - self.h, self.y))
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        if self.shield > 0:
            pygame.draw.ellipse(surface, (100, 200, 255, 120), (self.x-10, self.y-10, self.w+20, self.h+20), 3)
        # 동그라미 하나 + xN 텍스트로 생명 표시
        pygame.draw.circle(surface, (200, 240, 255), (30, SCREEN_HEIGHT - 25), 10)
        font_life = pygame.font.SysFont("malgungothic", 24)
        text = font_life.render(f"x{self.lives}", True, (200, 240, 255))
        surface.blit(text, (30 + 20, SCREEN_HEIGHT - 35))

# --- 총알 클래스 ---
class Bullet:
    def __init__(self, img, x, y, dx=0, dy=-10):
        self.img = img
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.w, self.h = img.get_width(), img.get_height()
    def update(self):
        self.x += self.dx
        self.y += self.dy
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

# --- 적 클래스 ---
class Enemy:
    def __init__(self, img, pattern="straight", stage=1):
        self.img = img
        self.w, self.h = img.get_width(), img.get_height()
        self.x = random.randint(0, SCREEN_WIDTH - self.w)
        self.y = -self.h
        self.speed = random.randint(2, 3) + stage
        self.pattern = pattern
        self.angle = 0
        self.bullet_timer = random.randint(40, 80) - stage*5
        self.hp = 1 + stage // 2
    def update(self):
        if self.pattern == "straight":
            self.y += self.speed
        elif self.pattern == "zigzag":
            self.y += self.speed
            self.x += int(4 * math.sin(self.angle))
            self.angle += 0.2
        elif self.pattern == "sine":
            self.y += self.speed
            self.x += int(10 * math.sin(self.y / 20))
        if self.y > SCREEN_HEIGHT + 10:
            return False
        self.x = max(0, min(SCREEN_WIDTH - self.w, self.x))
        return True
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

# --- 파워업 클래스 ---
class PowerUp:
    def __init__(self, img, kind, x, y):
        self.img = img
        self.kind = kind
        self.x, self.y = x, y
        self.w, self.h = img.get_width(), img.get_height()
        self.speed = 3
    def update(self):
        self.y += self.speed
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

# --- 보스 클래스 ---
class Boss:
    def __init__(self, img, stage=1):
        self.img = img
        self.w, self.h = img.get_width(), img.get_height()
        self.x = SCREEN_WIDTH // 2 - self.w // 2
        self.y = 50
        self.hp = 80 if stage == 1 else 120 + stage * 60
        self.bullet_timer = 0
        self.move_dir = 1
        self.stage = stage
    def update(self):
        self.x += self.move_dir * (2 + self.stage)
        if self.x < 0 or self.x > SCREEN_WIDTH - self.w:
            self.move_dir *= -1
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        max_hp = 80 if self.stage == 1 else 120 + self.stage*60
        pygame.draw.rect(surface, (255,0,0), (self.x, self.y-10, self.w, 7))
        pygame.draw.rect(surface, (0,255,0), (self.x, self.y-10, self.w * self.hp // max_hp, 7))

# --- 게임 초기화 및 리소스 로드 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 28)
font_small = pygame.font.SysFont("malgungothic", 18)

def load_img(path, fallback_color=(255,255,255), size=(40,40)):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

img_player = load_img(IMG_PLAYER, (80,200,255), PLAYER_SIZE)
img_enemy1 = load_img(IMG_ENEMY1, (255,80,80), ENEMY1_SIZE)
img_enemy2 = load_img(IMG_ENEMY2, (255,180,80), ENEMY2_SIZE)
img_boss = load_img(IMG_BOSS, (255,0,180), BOSS_SIZE)
img_bullet = load_img(IMG_BULLET, (255,255,0), BULLET_SIZE)
img_enemy_bullet = load_img(IMG_ENEMY_BULLET, (255,80,80), ENEMY_BULLET_SIZE)
img_powerup_shield = load_img(IMG_POWERUP_SHIELD, (100,200,255), POWERUP_SIZE)
img_powerup_multi = load_img(IMG_POWERUP_MULTI, (255,255,100), POWERUP_SIZE)

if os.path.exists(BGM):
    pygame.mixer.music.load(BGM)
    pygame.mixer.music.play(-1)
sfx_shoot = pygame.mixer.Sound(SFX_SHOOT) if os.path.exists(SFX_SHOOT) else None
sfx_explode = pygame.mixer.Sound(SFX_EXPLODE) if os.path.exists(SFX_EXPLODE) else None
sfx_powerup = pygame.mixer.Sound(SFX_POWERUP) if os.path.exists(SFX_POWERUP) else None
sfx_shield = pygame.mixer.Sound(SFX_SHIELD) if os.path.exists(SFX_SHIELD) else None
sfx_boss = pygame.mixer.Sound(SFX_BOSS) if os.path.exists(SFX_BOSS) else None

stars = [Star() for _ in range(80)]

# --- reset_game 함수: 스테이지에 따라 생명 수 결정 ---
def reset_game(stage=1):
    player = Player(img_player)
    player.lives = 3 + (stage - 1)  # 1스테이지: 3, 2스테이지: 4, ...
    bullets = []
    enemy_bullets = []
    enemies = []
    powerups = []
    boss = None
    boss_spawned = False
    score = 0
    enemy_spawn_timer = 0
    game_over = False
    fireworks = []
    boss_defeated = False
    firework_timer = 0
    return player, bullets, enemy_bullets, enemies, powerups, boss, boss_spawned, score, enemy_spawn_timer, game_over, fireworks, boss_defeated, firework_timer

def wait_for_enter(stage):
    waiting = True
    while waiting:
        dt = clock.tick(FPS)
        screen.fill((10, 10, 30))
        for star in stars:
            star.update()
            star.draw(screen)
        msg = font.render(f"Space Shooter - Stage {stage}", True, (255,255,0))
        msg2 = font.render("엔터키를 눌러 시작하세요!", True, (255,255,255))
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(msg2, (SCREEN_WIDTH//2 - msg2.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    
# --- 게임 설명/튜토리얼 페이지 함수 ---
def show_tutorial():
    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill((10, 10, 30))
        for star in stars:
            star.update()
            star.draw(screen)
        # 제목
        title = font.render("게임 방법 및 아이템 설명", True, (255,255,0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        # 조작법
        control1 = font_small.render("[조작법]", True, (80, 200, 255))
        control2 = font_small.render("←→↑↓/마우스 이동", True, (200, 220, 255))
        control3 = font_small.render("스페이스/마우스 클릭: 발사", True, (200, 220, 255))
        screen.blit(control1, (40, 80))
        screen.blit(control2, (60, 110))
        screen.blit(control3, (60, 135))
        # 아이템 설명
        item_y = 190
        # 쉴드
        screen.blit(img_powerup_shield, (60, item_y))
        txt1 = font_small.render("쉴드: 일정 시간 무적 상태가 됩니다.", True, (100,200,255))
        screen.blit(txt1, (110, item_y+8))
        # 멀티샷
        screen.blit(img_powerup_multi, (60, item_y+50))
        txt2 = font_small.render("멀티샷: 여러 방향으로 총알을 발사합니다.", True, (255,255,100))
        screen.blit(txt2, (110, item_y+58))
        # 기타 안내
        info1 = font_small.render("보스를 처치하면 다음 스테이지로 이동합니다.", True, (255,255,255))
        info2 = font_small.render("목숨이 모두 소진되면 게임 오버!", True, (255,180,180))
        screen.blit(info1, (40, 320))
        screen.blit(info2, (40, 350))
        # 엔터 안내
        enter_msg = font.render("엔터키를 눌러 계속", True, (255,255,0))
        screen.blit(enter_msg, (SCREEN_WIDTH//2 - enter_msg.get_width()//2, SCREEN_HEIGHT-80))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
first_run = True
stage = 1
while True:
    if first_run:
        show_tutorial()
        first_run = False
    if stage > TOTAL_STAGE:
        screen.fill((10, 10, 30))
        msg = font.render("축하합니다! 모든 스테이지 클리어!", True, (255,255,0))
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.wait(3500)
        stage = 1
        continue

    wait_for_enter(stage)
    player, bullets, enemy_bullets, enemies, powerups, boss, boss_spawned, score, enemy_spawn_timer, game_over, fireworks, boss_defeated, firework_timer = reset_game(stage)

    while True:
        dt = clock.tick(FPS)
        screen.fill((10, 10, 30))
        for star in stars:
            star.update()
            star.draw(screen)

        # --- 이벤트 처리 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not boss_defeated:
                if player.cooldown == 0:
                    bx = player.x + player.w // 2 - img_bullet.get_width()//2
                    by = player.y
                    if player.multi > 0:
                        bullets.append(Bullet(img_bullet, bx-15, by, dx=-3, dy=-10))
                        bullets.append(Bullet(img_bullet, bx, by))
                        bullets.append(Bullet(img_bullet, bx+15, by, dx=3, dy=-10))
                    else:
                        bullets.append(Bullet(img_bullet, bx, by))
                    if sfx_shoot: sfx_shoot.play()
                    player.cooldown = 10

        keys = pygame.key.get_pressed()
        if not game_over and not boss_defeated:
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += player.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += player.speed
            player.move(dx, dy)
            mx, my = pygame.mouse.get_pos()
            if pygame.mouse.get_focused():
                player.move_to_cursor(mx, my, instant=True)
            if keys[pygame.K_SPACE] and player.cooldown == 0:
                bx = player.x + player.w // 2 - img_bullet.get_width()//2
                by = player.y
                if player.multi > 0:
                    bullets.append(Bullet(img_bullet, bx-15, by, dx=-3, dy=-10))
                    bullets.append(Bullet(img_bullet, bx, by))
                    bullets.append(Bullet(img_bullet, bx+15, by, dx=3, dy=-10))
                else:
                    bullets.append(Bullet(img_bullet, bx, by))
                if sfx_shoot: sfx_shoot.play()
                player.cooldown = 10
            if player.cooldown > 0:
                player.cooldown -= 1

            enemy_spawn_timer += 1
            if enemy_spawn_timer > max(30 - stage*3, 10) and not boss_spawned:
                pattern = random.choice(["straight", "zigzag", "sine"])
                img = img_enemy1 if pattern == "straight" else img_enemy2
                enemies.append(Enemy(img, pattern, stage))
                enemy_spawn_timer = 0

            if not boss_spawned and player.score >= 200 + (stage-1)*100:
                boss = Boss(img_boss, stage)
                boss_spawned = True
                if sfx_boss: sfx_boss.play()

        for bullet in bullets[:]:
            bullet.update()
            if bullet.y < -10 or bullet.x < -10 or bullet.x > SCREEN_WIDTH + 10:
                bullets.remove(bullet)
        for enemy in enemies[:]:
            alive = enemy.update()
            if not alive:
                enemies.remove(enemy)
        for pu in powerups[:]:
            pu.update()
            if pu.y > SCREEN_HEIGHT:
                powerups.remove(pu)
        for eb in enemy_bullets[:]:
            eb.update()
            if eb.y > SCREEN_HEIGHT:
                enemy_bullets.remove(eb)

        for enemy in enemies:
            enemy.bullet_timer -= 1
            if enemy.bullet_timer <= 0:
                bx = enemy.x + enemy.w // 2 - img_enemy_bullet.get_width()//2
                by = enemy.y + enemy.h
                enemy_bullets.append(Bullet(img_enemy_bullet, bx, by, dy=6+stage))
                enemy.bullet_timer = random.randint(50, 100) - stage*5

        # --- 보스 이동 및 공격 ---
        if boss_spawned and boss is not None:
            boss.update()
            boss.bullet_timer += 1
            if boss.bullet_timer > max(25 - stage*3, 7):
                bx = boss.x + boss.w//2 - img_enemy_bullet.get_width()//2
                by = boss.y + boss.h
                for dx in [-5, 0, 5]:
                    enemy_bullets.append(Bullet(img_enemy_bullet, bx+dx*5, by, dx=dx, dy=8+stage))
                boss.bullet_timer = 0

        # --- 충돌 판정(총알-적) ---
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.rect().colliderect(bullet.rect()):
                    enemy.hp -= 1
                    bullets.remove(bullet)
                    if enemy.hp <= 0:
                        if random.random() < 0.25 + 0.05*stage:
                            kind = random.choice(["shield", "multi"])
                            img = img_powerup_shield if kind == "shield" else img_powerup_multi
                            powerups.append(PowerUp(img, kind, enemy.x, enemy.y))
                        enemies.remove(enemy)
                        player.score += 10
                        if sfx_explode: sfx_explode.play()
                    break

        # --- 충돌 판정(총알-보스) ---
        if boss_spawned and boss is not None:
            for bullet in bullets[:]:
                if boss is not None and boss.rect().colliderect(bullet.rect()):
                    boss.hp -= 7 if stage == 1 else 5
                    bullets.remove(bullet)
                    if sfx_explode: sfx_explode.play()
                    if boss.hp <= 0:
                        boss = None
                        boss_spawned = False
                        player.score += 200
                        boss_defeated = True
                        fireworks = []
                        for _ in range(12):
                            fx = SCREEN_WIDTH // 2 + random.randint(-40,40)
                            fy = 100 + random.randint(-20,20)
                            for _ in range(20):
                                fireworks.append(FireworkParticle(fx, fy))
                        firework_timer = FPS * 3

        for enemy in enemies[:]:
            if enemy.rect().colliderect(player.rect()):
                enemies.remove(enemy)
                if player.shield > 0:
                    player.shield = 0
                else:
                    player.lives -= 1
                    if sfx_explode: sfx_explode.play()
                    if player.lives <= 0:
                        game_over = True

        for eb in enemy_bullets[:]:
            if eb.rect().colliderect(player.rect()):
                enemy_bullets.remove(eb)
                if player.shield > 0:
                    player.shield = 0
                else:
                    player.lives -= 1
                    if sfx_explode: sfx_explode.play()
                    if player.lives <= 0:
                        game_over = True

        for pu in powerups[:]:
            if pu.rect().colliderect(player.rect()):
                if pu.kind == "shield":
                    player.shield = FPS * 5
                    if sfx_shield: sfx_shield.play()
                elif pu.kind == "multi":
                    player.multi = FPS *99
                    if sfx_powerup: sfx_powerup.play()
                powerups.remove(pu)

        if player.shield > 0:
            player.shield -= 1
        if player.multi > 0:
            player.multi -= 1

        # --- 화면 그리기 ---
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for pu in powerups:
            pu.draw(screen)
        for eb in enemy_bullets:
            eb.draw(screen)
        if boss_spawned and boss is not None:
            boss.draw(screen)
        player.draw(screen)

        # --- HUD(점수, 스테이지) ---
        score_text = font.render(f"점수: {player.score}", True, (255,255,255))
        stage_text = font.render(f"Stage: {stage}/{TOTAL_STAGE}", True, (255,255,0))
        screen.blit(score_text, (SCREEN_WIDTH-150, 10))
        screen.blit(stage_text, (20, 10))

        # --- 오른쪽 하단에 조작방법 멘트(작은 폰트) ---
        control_text = font_small.render("←→↑↓/마우스 이동  스페이스/클릭 발사", True, (80, 120, 155))
        text_rect = control_text.get_rect()
        text_rect.bottomright = (SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5)
        screen.blit(control_text, text_rect)

        # --- 보스 클리어 연출 및 스테이지 전환 ---
        if boss_defeated:
            for particle in fireworks[:]:
                particle.update()
                if particle.life <= 0:
                    fireworks.remove(particle)
            for particle in fireworks:
                particle.draw(screen)
            firework_timer -= 1
            msg = font.render("보스를 격파했습니다!", True, (255,255,0))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 40))
            msg2 = font.render("다음 스테이지로 이동합니다...", True, (255,255,255))
            screen.blit(msg2, (SCREEN_WIDTH//2 - msg2.get_width()//2, SCREEN_HEIGHT//2 + 5))
            if firework_timer <= 0:
                pygame.display.flip()
                pygame.time.wait(1500)
                stage += 1
                break
        elif game_over:
            over_text = font.render("게임 오버! 다시 시작하려면 R", True, (255, 100, 100))
            screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                stage = 1
                break

        pygame.display.flip()