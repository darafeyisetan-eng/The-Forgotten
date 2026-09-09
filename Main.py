import sys
import pygame

from Settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    HERO_MAX_HEALTH,
    HERO_SCALE,
    load_hero_sprites,
    load_arrow_sprite
)

from Player import Hero
from Arrow import Arrow
from Map import Map
from Enemy import Enemy


class Game:

    def __init__(self):

        # =====================================================
        # PYGAME
        # =====================================================

        pygame.init()

        # =====================================================
        # WINDOW
        # =====================================================

        self.screen = pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        pygame.display.set_caption(
            GAME_TITLE
        )

        # =====================================================
        # LOAD ASSETS
        # =====================================================

        # The display exists now, so convert_alpha()
        # can safely be used by Settings.py.

        self.hero_sprites = load_hero_sprites()

        self.arrow_sprite = load_arrow_sprite()

        # =====================================================
        # CLOCK
        # =====================================================

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)

        self.running = True

        # =====================================================
        # PLAYER
        # =====================================================

        self.player = Hero(
            SCREEN_WIDTH // 2 - 35,
            SCREEN_HEIGHT // 2 - 35,
            HERO_MAX_HEALTH,
            HERO_SCALE,
            self.hero_sprites
        )

        # =====================================================
        # ARROWS
        # =====================================================

        self.arrows = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group(
            Enemy(150, 150),
            Enemy(650, 180),
            Enemy(650, 450)
        )
        self.map = Map()
        self.game_over = False

        # =====================================================
        # MOUSE
        # =====================================================

        self.mouse_held = False

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        while self.running:

            dt = (
                self.clock.tick(FPS)
                / 1000.0
            )

            # Prevent very large time jumps
            dt = min(
                dt,
                0.1
            )

            self.handle_events()

            self.update(dt)

            self.draw()

            pygame.display.flip()

        self.close()

    # =====================================================
    # EVENTS
    # =====================================================

    def handle_events(self):

        for event in pygame.event.get():

            # =================================================
            # QUIT
            # =================================================

            if event.type == pygame.QUIT:

                self.running = False

            # =================================================
            # KEYBOARD
            # =================================================

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_m:

                    self.toggle_bow()

                elif event.key == pygame.K_h:
                    self.player.heal()

                elif event.key == pygame.K_r and self.game_over:
                    self.restart()

            # =================================================
            # MOUSE DOWN
            # =================================================

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    self.mouse_held = True

                    # -----------------------------------------
                    # BOW
                    # -----------------------------------------

                    if self.player.bow_equipped:

                        self.player.start_bow()

                    # -----------------------------------------
                    # MELEE
                    # -----------------------------------------

                    else:

                        self.player.attack()
                        self.melee_attack()

            # =================================================
            # MOUSE UP
            # =================================================

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:

                    self.mouse_held = False

                    # -----------------------------------------
                    # RELEASE BOW
                    # -----------------------------------------

                    if self.player.bow_equipped:

                        self.player.release_bow()

    # =====================================================
    # TOGGLE BOW
    # =====================================================

    def toggle_bow(self):

        self.player.bow_equipped = (
            not self.player.bow_equipped
        )

        self.player.weapon_equipped = (
            self.player.bow_equipped
        )

        # =================================================
        # BOW UNEQUIPPED
        # =================================================

        if not self.player.bow_equipped:

            self.mouse_held = False

            self.player.cancel_bow()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        if self.game_over:
            return

        # =====================================================
        # PLAYER MOVEMENT
        # =====================================================

        self.player.keyboard_input(
            dt
        )
        self.player.update_status(dt)

        # =====================================================
        # PLAYER ANIMATION
        # =====================================================

        self.player.update_animation(
            dt
        )

        # =====================================================
        # BOW
        # =====================================================

        if (
            self.player.bow_equipped
            and self.mouse_held
            and not self.player.attacking
        ):

            self.player.start_bow()

        # =====================================================
        # ATTACK
        # =====================================================

        self.player.update_attack(
            dt
        )

        # =====================================================
        # FIRE ARROW
        # =====================================================

        if self.player.fire_arrow:

            self.shoot_arrow()

            self.player.fire_arrow = False

        # =====================================================
        # ARROWS
        # =====================================================

        self.arrows.update(
            dt
        )
        for enemy in self.enemies:
            enemy.update(dt, self.player)
        self.handle_arrow_hits()
        for enemy in list(self.enemies):
            if enemy.health <= 0:
                enemy.kill()
        if self.player.health <= 0:
            self.game_over = True

    def melee_attack(self):
        attack_range = self.player.rect.inflate(55, 55)
        for enemy in self.enemies:
            if attack_range.colliderect(enemy.rect):
                enemy.take_damage(25)

    def handle_arrow_hits(self):
        for arrow in list(self.arrows):
            hit = pygame.sprite.spritecollideany(arrow, self.enemies)
            if hit is not None:
                hit.take_damage(25)
                arrow.kill()

    def restart(self):
        self.player.health = self.player.max_health
        self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = pygame.sprite.Group(
            Enemy(150, 150),
            Enemy(650, 180),
            Enemy(650, 450)
        )
        self.game_over = False

    # =====================================================
    # SHOOT ARROW
    # =====================================================

    def shoot_arrow(self):

        mouse_x, mouse_y = (
            pygame.mouse.get_pos()
        )

        arrow = Arrow(
            self.player.rect.centerx,
            self.player.rect.centery,
            mouse_x,
            mouse_y,
            self.arrow_sprite
        )

        self.arrows.add(
            arrow
        )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        # Clear the previous frame before drawing transparent map areas.
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for arrow in self.arrows:
            arrow.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_hud()

    def draw_hud(self):
        panel = pygame.Rect(12, 12, 280, 82)
        pygame.draw.rect(self.screen, (20, 25, 35), panel, border_radius=8)
        pygame.draw.rect(self.screen, (235, 235, 235), panel, 2, border_radius=8)
        health_bar = pygame.Rect(24, 24, 220, 18)
        pygame.draw.rect(self.screen, (75, 30, 35), health_bar)
        health_bar.width = int(220 * self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, (70, 190, 95), health_bar)
        text = self.font.render(
            f"Health: {self.player.health}/{self.player.max_health}",
            True, (255, 255, 255)
        )
        self.screen.blit(text, (24, 48))
        controls = self.font.render("WASD move  H heal  M bow  LMB attack", True, (255, 255, 255))
        self.screen.blit(controls, (12, SCREEN_HEIGHT - 32))
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 175))
            self.screen.blit(overlay, (0, 0))
            message = self.font.render("You fell in the forest - press R to restart", True, (255, 230, 180))
            self.screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        pygame.quit()

        sys.exit()


# =========================================================
# START GAME
# =========================================================

if __name__ == "__main__":

    game = Game()

    game.run()
