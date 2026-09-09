import json
import os

import pygame

from Settings import (
    MAP_DATA_PATH,
    PHASER_ENVIRONMENT_PATH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Map:
    def __init__(self):
        with open(MAP_DATA_PATH, "r", encoding="utf-8") as map_file:
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
