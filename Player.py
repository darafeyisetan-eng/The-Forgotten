import pygame

from Settings import (
    HERO_SPEED,
    HERO_SCALE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class Hero(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        health,
        scale,
        hero_sprites
    ):

        super().__init__()

        # =====================================================
        # PLAYER
        # =====================================================

        self.max_health = health
        self.health = health
        self.heal_cooldown = 0
        self.scale = scale

        self.hero_sprites = hero_sprites

        # =====================================================
        # WEAPON
        # =====================================================

        self.weapon_equipped = False
        self.bow_equipped = False

        # =====================================================
        # BOW
        # =====================================================

        self.shooting = False
        self.fire_arrow = False

        # =====================================================
        # POSITION
        # =====================================================

        self.rect = pygame.Rect(
            x,
            y,
            scale,
            scale
        )

        # =====================================================
        # MOVEMENT
        # =====================================================

        self.speed = HERO_SPEED
        self.moving = False

        # =====================================================
        # DIRECTION
        # =====================================================

        self.direction = "front"
        self.flip = False

        # =====================================================
        # WALK ANIMATION
        # =====================================================

        self.animation_speed = 0.15
        self.animation_timer = 0
        self.frame = 0

        # =====================================================
        # ATTACK
        # =====================================================

        self.attacking = False
        self.attack_timer = 0
        self.attack_frame = 0

        self.attack_animation_speed = 0.12

        # =====================================================
        # IMAGE
        # =====================================================

        self.image = pygame.transform.scale(
            self.hero_sprites["walk_front"][0],
            (
                self.scale,
                self.scale
            )
        )

        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

    # =====================================================
    # MOVEMENT
    # =====================================================

    def keyboard_input(self, dt, collision_checker=None):

        keys = pygame.key.get_pressed()

        self.moving = False

        dx = 0
        dy = 0

        if keys[pygame.K_a]:

            dx = -1
            self.direction = "side"
            self.flip = True
            self.moving = True

        elif keys[pygame.K_d]:

            dx = 1
            self.direction = "side"
            self.flip = False
            self.moving = True

        if keys[pygame.K_w]:

            dy = -1
            self.direction = "back"
            self.flip = False
            self.moving = True

        elif keys[pygame.K_s]:

            dy = 1
            self.direction = "front"
            self.flip = False
            self.moving = True

        # =================================================
        # DIAGONAL MOVEMENT
        # =================================================

        if dx != 0 and dy != 0:

            multiplier = 0.7071

            dx *= multiplier
            dy *= multiplier

        # =================================================
        # MOVE
        # =================================================

        move_x = int(dx * self.speed * dt)
        move_y = int(dy * self.speed * dt)
        if move_x:
            candidate = self.rect.move(move_x, 0)
            if collision_checker is None or not collision_checker(candidate):
                self.rect = candidate
        if move_y:
            candidate = self.rect.move(0, move_y)
            if collision_checker is None or not collision_checker(candidate):
                self.rect = candidate

        # =================================================
        # SCREEN BOUNDARIES
        # =================================================

        self.rect.left = max(
            0,
            self.rect.left
        )

        self.rect.right = min(
            SCREEN_WIDTH,
            self.rect.right
        )

        self.rect.top = max(
            0,
            self.rect.top
        )

        self.rect.bottom = min(
            SCREEN_HEIGHT,
            self.rect.bottom
        )

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount=25):
        if self.health <= 0 or self.heal_cooldown > 0:
            return False
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        if self.health == old_health:
            return False
        self.heal_cooldown = 1.0
        return True

    def update_status(self, dt):
        self.heal_cooldown = max(0, self.heal_cooldown - dt)

    # =====================================================
    # WALK ANIMATION
    # =====================================================

    def update_animation(self, dt):

        if self.attacking:
            return

        if self.moving:

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:

                self.animation_timer -= (
                    self.animation_speed
                )

                self.frame += 1

            animation = self.get_walk_animation()

            if self.frame >= len(animation):

                self.frame = 0

        else:

            self.frame = 0
            self.animation_timer = 0

        self.update_image()

    # =====================================================
    # GET WALK ANIMATION
    # =====================================================

    def get_walk_animation(self):

        if self.direction == "side":

            return self.hero_sprites[
                "walk_side"
            ]

        elif self.direction == "back":

            return self.hero_sprites[
                "walk_back"
            ]

        return self.hero_sprites[
            "walk_front"
        ]

    # =====================================================
    # UPDATE WALK IMAGE
    # =====================================================

    def update_image(self):

        animation = self.get_walk_animation()

        if self.frame >= len(animation):

            self.frame = 0

        image = pygame.transform.scale(
            animation[self.frame],
            (
                self.scale,
                self.scale
            )
        )

        image = pygame.transform.flip(
            image,
            self.flip,
            False
        )

        centre = self.rect.center

        self.image = image

        self.rect = self.image.get_rect(
            center=centre
        )

    # =====================================================
    # MELEE ATTACK
    # =====================================================

    def attack(self):

        if self.attacking:
            return

        if self.bow_equipped:
            return

        self.attacking = True

        self.attack_timer = 0
        self.attack_frame = 0

        self.set_attack_direction()

        self.update_attack_image()

    # =====================================================
    # SET ATTACK DIRECTION
    # =====================================================

    def set_attack_direction(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        difference_x = (
            mouse_x -
            self.rect.centerx
        )

        difference_y = (
            mouse_y -
            self.rect.centery
        )

        if abs(difference_x) > abs(difference_y):

            self.direction = "side"

            self.flip = (
                difference_x < 0
            )

        else:

            if difference_y >= 0:

                self.direction = "front"

            else:

                self.direction = "back"

            self.flip = False

    # =====================================================
    # UPDATE ATTACK
    # =====================================================

    def update_attack(self, dt):

        if not self.attacking:
            return

        # =================================================
        # BOW
        # =================================================

        if self.bow_equipped:

            self.set_attack_direction()

            self.attack_timer += dt

            if self.attack_timer >= self.attack_animation_speed:

                self.attack_timer -= (
                    self.attack_animation_speed
                )

                # Move toward final bow frame
                if self.attack_frame < 2:

                    self.attack_frame += 1

                self.update_attack_image()

            return

        # =================================================
        # MELEE
        # =================================================

        self.attack_timer += dt

        if self.attack_timer >= self.attack_animation_speed:

            self.attack_timer -= (
                self.attack_animation_speed
            )

            self.attack_frame += 1

            animation = self.get_attack_animation()

            if self.attack_frame >= len(animation):

                self.attack_frame = 0
                self.attacking = False

                self.frame = 0
                self.animation_timer = 0

                self.update_image()

                return

        self.update_attack_image()

    # =====================================================
    # GET ATTACK ANIMATION
    # =====================================================

    def get_attack_animation(self):

        if self.weapon_equipped:

            if self.direction == "side":

                return self.hero_sprites[
                    "attack_weapon_side"
                ]

            elif self.direction == "back":

                return self.hero_sprites[
                    "attack_weapon_back"
                ]

            return self.hero_sprites[
                "attack_weapon_front"
            ]

        if self.direction == "side":

            return self.hero_sprites[
                "attack_side"
            ]

        elif self.direction == "back":

            return self.hero_sprites[
                "attack_back"
            ]

        return self.hero_sprites[
            "attack_front"
        ]

    # =====================================================
    # UPDATE ATTACK IMAGE
    # =====================================================

    def update_attack_image(self):

        animation = self.get_attack_animation()

        if self.attack_frame >= len(animation):

            self.attack_frame = (
                len(animation) - 1
            )

        image = pygame.transform.scale(
            animation[self.attack_frame],
            (
                self.scale,
                self.scale
            )
        )

        image = pygame.transform.flip(
            image,
            self.flip,
            False
        )

        centre = self.rect.center

        self.image = image

        self.rect = self.image.get_rect(
            center=centre
        )

    # =====================================================
    # START BOW
    # =====================================================

    def start_bow(self):

        if not self.bow_equipped:
            return

        if self.attacking:
            return

        self.set_attack_direction()

        self.attacking = True
        self.shooting = True

        self.fire_arrow = False

        self.attack_timer = 0
        self.attack_frame = 0

        self.update_attack_image()

    # =====================================================
    # RELEASE BOW
    # =====================================================

    def release_bow(self):

        if not self.bow_equipped:
            return

        if not self.attacking:
            return

        # Tell Game to create the arrow
        self.fire_arrow = True

        self.shooting = False
        self.attacking = False

        self.attack_timer = 0
        self.attack_frame = 0

        self.frame = 0
        self.animation_timer = 0

        self.update_image()

    # =====================================================
    # CANCEL BOW
    # =====================================================

    def cancel_bow(self):

        self.shooting = False
        self.fire_arrow = False
        self.attacking = False

        self.attack_timer = 0
        self.attack_frame = 0

        self.frame = 0
        self.animation_timer = 0

        self.update_image()

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )
