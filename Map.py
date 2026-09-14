import json
import os

import pygame

from Settings import (
    MAP_DATA_PATH,
    SECOND_MAP_DATA_PATH,
    PHASER_ENVIRONMENT_PATH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Map:
    def __init__(self, scene="forest"):
        self.scene = scene
        map_path = MAP_DATA_PATH if scene == "forest" else SECOND_MAP_DATA_PATH
        if not os.path.isfile(map_path):
            map_path = MAP_DATA_PATH

        with open(map_path, "r", encoding="utf-8") as map_file:
            map_data = json.load(map_file)

        self.tile_size = map_data["tilewidth"]
        self.width = map_data["width"]
        self.height = map_data["height"]
        self.world_size = (
            self.width * self.tile_size,
            self.height * self.tile_size,
        )
        self.image = pygame.Surface(self.world_size, pygame.SRCALPHA)
        self.image.fill((30, 55, 35))
        scale_x = SCREEN_WIDTH / self.world_size[0]
        scale_y = SCREEN_HEIGHT / self.world_size[1]
        self.collision_rects = []
        collision_layer = next(
            (
                layer for layer in map_data["layers"]
                if layer["type"] == "tilelayer"
                and "collision" in layer["name"].lower()
            ),
            None,
        )
        if collision_layer is not None:
            for index, raw_gid in enumerate(collision_layer["data"]):
                if raw_gid & 0x1FFFFFFF:
                    x = (index % self.width) * self.tile_size * scale_x
                    y = (index // self.width) * self.tile_size * scale_y
                    collision_rect = pygame.Rect(
                        round(x),
                        round(y),
                        max(1, round(self.tile_size * scale_x)),
                        max(1, round(self.tile_size * scale_y)),
                    )
                    # Keep collision geometry in the same screen-space
                    # coordinate system as the scaled map image.
                    collision_rect = collision_rect.clip(
                        pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                    )
                    if collision_rect.width and collision_rect.height:
                        self.collision_rects.append(collision_rect)

        portal_height = 96
        portal_y = (SCREEN_HEIGHT - portal_height) // 2
        if scene == "forest":
            self.road_entrance = pygame.Rect(
                SCREEN_WIDTH - 80, portal_y, 80, portal_height
            )
        else:
            self.road_entrance = pygame.Rect(
                0, portal_y, 80, portal_height
            )

        tilesets = []
        for tileset_data in map_data["tilesets"]:
            image_path = os.path.join(
                PHASER_ENVIRONMENT_PATH,
                os.path.basename(tileset_data["image"]),
            )
            tilesets.append(
                (
                    tileset_data["firstgid"],
                    tileset_data["columns"],
                    pygame.image.load(image_path).convert_alpha(),
                )
            )

        for layer in map_data["layers"]:
            if layer["type"] != "tilelayer" or "collision" in layer["name"].lower():
                continue
            self._draw_layer(layer["data"], tilesets)

        self.image = pygame.transform.smoothscale(
            self.image,
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        self.rect = self.image.get_rect(topleft=(0, 0))

    def _draw_layer(self, tile_data, tilesets):
        for index, raw_gid in enumerate(tile_data):
            gid = raw_gid & 0x1FFFFFFF
            if gid == 0:
                continue

            tileset = None
            for candidate in tilesets:
                if candidate[0] <= gid:
                    tileset = candidate
                else:
                    break
            if tileset is None:
                continue

            first_gid, columns, tileset_image = tileset
            tile_index = gid - first_gid
            source_rect = pygame.Rect(
                (tile_index % columns) * self.tile_size,
                (tile_index // columns) * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            target_rect = pygame.Rect(
                (index % self.width) * self.tile_size,
                (index // self.width) * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            self.image.blit(tileset_image, target_rect, source_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides(self, rect):
        # The road is deliberately traversable so scene transitions remain
        # possible even though it is adjacent to the collision layer.
        if rect.colliderect(self.road_entrance):
            return False
        return any(rect.colliderect(obstacle) for obstacle in self.collision_rects)

    def at_road_exit(self, rect):
        return rect.colliderect(self.road_entrance)
