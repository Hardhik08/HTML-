import sys
try:
    import pygame
except ImportError:
    print("Please run: pip install pygame")
    sys.exit(1)

import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (10, 10, 15)
CYAN = (0, 255, 255)
RED = (255, 50, 50)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Dodge Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.size = 20
        self.rect = pygame.Rect(WIDTH//2, HEIGHT - 100, self.size, self.size)
        self.color = CYAN

    def update(self):
        # Follow mouse position exactly
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        # Keep inside window
        self.rect.clamp_ip(screen.get_rect())

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Neon glow effect
        glow_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 255, 255, 40), (self.size * 1.5, self.size * 1.5), self.size * 1.5)
        surface.blit(glow_surface, (self.rect.centerx - self.size * 1.5, self.rect.centery - self.size * 1.5))

class Enemy:
    def __init__(self, speed_multiplier):
        self.size = random.randint(15, 30)
        self.rect = pygame.Rect(random.randint(0, WIDTH - self.size), -self.size, self.size, self.size)
        
        # Calculate speed based on current game difficulty
        self.speed = random.uniform(3, 8) * speed_multiplier
        self.color = RED

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Red neon glow effect
        glow = pygame.Surface((self.size*3, self.size*3), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 50, 50, 40), (self.size * 1.5, self.size * 1.5), self.size * 1.5)
        surface.blit(glow, (self.rect.centerx - self.size * 1.5, self.rect.centery - self.size * 1.5))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6, 6)
        self.vy = random.uniform(-6, 6)
        self.life = 255
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 8  # Fade out speed

    def draw(self, surface):
        if self.life > 0:
            color = (*self.color, max(0, self.life))
            s = pygame.Surface((4, 4), pygame.SRCALPHA)
            s.fill(color)
            surface.blit(s, (int(self.x), int(self.y)))

def main():
    player = Player()
    enemies = []
    particles = []
    score = 0
    font = pygame.font.SysFont("Arial", 36, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)
    
    speed_multiplier = 1.0
    spawn_rate = 30 # frames between spawns initially
    frame_count = 0

    game_over = False

    while True:
        # Background color
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Restart game when clicked during Game Over screen
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                player = Player()
                enemies.clear()
                particles.clear()
                score = 0
                speed_multiplier = 1.0
                spawn_rate = 30
                game_over = False

        if not game_over:
            pygame.mouse.set_visible(False)  # Hide cursor
            player.update()
            player.draw(screen)

            frame_count += 1
            if frame_count >= spawn_rate:
                enemies.append(Enemy(speed_multiplier))
                frame_count = 0
                
                # Increase difficulty over time
                speed_multiplier += 0.01
                spawn_rate = max(5, int(spawn_rate * 0.99))

            # Update and draw enemies
            for enemy in enemies[:]:
                enemy.update()
                
                # Check collision with player
                if player.rect.colliderect(enemy.rect):
                    game_over = True
                    
                    # Spawn explosion particle effects
                    for _ in range(50):
                        particles.append(Particle(player.rect.centerx, player.rect.centery, (0, 255, 255)))
                    for _ in range(50):
                        particles.append(Particle(enemy.rect.centerx, enemy.rect.centery, (255, 50, 50)))
                    enemies.remove(enemy)
                
                # Enemy successfully dodged
                elif enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
                    score += 1

                # Draw enemy if it wasn't removed
                if enemy in enemies:
                    enemy.draw(screen)

        else:
            pygame.mouse.set_visible(True)  # Show cursor again
            
            # Draw game over overlay
            go_text = font.render(f"GAME OVER", True, WHITE)
            score_text = font.render(f"Final Score: {score}", True, CYAN)
            restart_text = small_font.render("Click anywhere to restart", True, (150, 150, 150))
            
            screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 10))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

        # Update and draw particles globally
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        # Draw live score in top left
        if not game_over:
            s_text = font.render(str(score), True, WHITE)
            screen.blit(s_text, (20, 20))

        # Refresh screen
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
