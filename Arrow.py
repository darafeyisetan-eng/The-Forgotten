import math
import pygame

from Settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class Arrow(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        arrow_sprite
    ):

        super().__init__()

        # =====================================================
        # SETTINGS
        # =====================================================

        self.speed = 600
        self.damage = 25

        # =====================================================
        # POSITION
        # =====================================================

        self.position = pygame.Vector2(
            x,
            y
        )

        # =====================================================
        # DIRECTION
        # =====================================================

        direction = pygame.Vector2(
            target_x - x,
            target_y - y
        )

        if direction.length_squared() == 0:

            direction = pygame.Vector2(
                1,
                0
            )

        direction = direction.normalize()

        self.velocity = (
            direction * self.speed
        )

        # =====================================================
        # IMAGE
        # =====================================================

        self.original_image = pygame.transform.scale(
            arrow_sprite,
            (40, 40)
        )

        # =====================================================
        # ROTATION
        # =====================================================

        angle = math.degrees(
            math.atan2(
                -self.velocity.y,
                self.velocity.x
            )
        )

        self.image = pygame.transform.rotate(
            self.original_image,
            angle
        )

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        self.position += (
            self.velocity * dt
        )

        self.rect.center = (
            round(self.position.x),
            round(self.position.y)
        )

        # =================================================
        # REMOVE OUTSIDE SCREEN
        # =================================================

        if (
            self.rect.right < 0
            or self.rect.left > SCREEN_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > SCREEN_HEIGHT
        ):

            self.kill()

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )
