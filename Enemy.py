import math
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size=42):
        super().__init__()
        self.max_health = 60
        self.health = self.max_health
        self.speed = 70
        self.damage = 8
        self.attack_cooldown = 0
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (112, 47, 55), (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, (244, 214, 120), (size // 3, size // 3), 4)
        pygame.draw.circle(self.image, (244, 214, 120), (size * 2 // 3, size // 3), 4)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt, player):
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        direction = pygame.Vector2(player.rect.center) - self.rect.center
        if direction.length_squared() > 48 ** 2:
            self.rect.center += direction.normalize() * self.speed * dt
        elif self.attack_cooldown == 0:
            player.take_damage(self.damage)
            self.attack_cooldown = 0.8

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        return self.health == 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        bar = pygame.Rect(self.rect.left, self.rect.top - 8, self.rect.width, 5)
        pygame.draw.rect(screen, (50, 20, 20), bar)
        bar.width = int(bar.width * self.health / self.max_health)
        pygame.draw.rect(screen, (210, 70, 65), bar)
