import os
import pygame


# =====================================================
# GAME SETTINGS
# =====================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60

GAME_TITLE = "The Forgotten"


# =====================================================
# HERO SETTINGS
# =====================================================

HERO_SPEED = 250
HERO_SCALE = 70
HERO_MAX_HEALTH = 100


# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =====================================================
# ASSET PATH
# =====================================================

# Support both layouts used by the downloadable project:
#   project/tiny-RPG-forest-files/Assets/PNG
#   tiny-RPG-forest-files/project/ (when the project is copied into the bundle)
_asset_roots = (
    os.path.join(BASE_DIR, "tiny-RPG-forest-files"),
    os.path.dirname(BASE_DIR),
)
_bundle_root = next(
    (
        root for root in _asset_roots
        if os.path.isdir(os.path.join(root, "Assets", "PNG"))
    ),
    _asset_roots[0],
)

ASSET_PATH = os.path.join(
    _bundle_root,
    "Assets",
    "PNG"
)

ENVIRONMENT_PATH = os.path.join(
    ASSET_PATH,
    "environment"
)

MAP_PATH = os.path.join(
    ENVIRONMENT_PATH,
    "tileset.png"
)

MAP_DATA_PATH = os.path.join(
    ASSET_PATH,
    "..",
    "Phaser Demo",
    "assets",
    "maps",
    "map.json"
)

SECOND_MAP_DATA_PATH = os.path.join(
    ASSET_PATH,
    "..",
    "Phaser Demo",
    "assets",
    "maps",
    "map copy.json",
)

PHASER_ENVIRONMENT_PATH = os.path.join(
    ASSET_PATH,
    "..",
    "Phaser Demo",
    "assets",
    "environment"
)


# =====================================================
# SPRITE PATH
# =====================================================

SPRITE_PATH = os.path.join(
    ASSET_PATH,
    "sprites"
)


# =====================================================
# HERO PATH
# =====================================================

HERO_PATH = os.path.join(
    SPRITE_PATH,
    "hero"
)


# =====================================================
# ARROW PATH
# =====================================================

ARROW_PATH = os.path.join(
    SPRITE_PATH,
    "misc",
    "arrow.png"
)


# =====================================================
# LOAD IMAGE
# =====================================================

def load_image(path):

    if not os.path.isfile(path):

        raise FileNotFoundError(
            f"\nImage not found:\n{path}\n"
        )

    return pygame.image.load(
        path
    ).convert_alpha()


# =====================================================
# LOAD HERO SPRITES
# =====================================================

def load_hero_sprites():

    return {

        # =================================================
        # WALKING
        # =================================================

        "walk_back": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "walk",
                    "hero-walk-back",
                    f"hero-walk-back-{x}.png"
                )
            )
            for x in range(1, 7)
        ],

        "walk_front": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "walk",
                    "hero-walk-front",
                    f"hero-walk-front-{x}.png"
                )
            )
            for x in range(1, 7)
        ],

        "walk_side": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "walk",
                    "hero-walk-side",
                    f"hero-walk-side-{x}.png"
                )
            )
            for x in range(1, 7)
        ],


        # =================================================
        # UNARMED ATTACK
        # =================================================

        "attack_back": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack",
                    "hero-attack-back",
                    f"hero-attack-back-{x}.png"
                )
            )
            for x in range(1, 4)
        ],

        "attack_front": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack",
                    "hero-attack-front",
                    f"hero-attack-front-{x}.png"
                )
            )
            for x in range(1, 4)
        ],

        "attack_side": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack",
                    "hero-attack-side",
                    f"hero-attack-side-{x}.png"
                )
            )
            for x in range(1, 4)
        ],


        # =================================================
        # BOW / WEAPON
        # =================================================

        "attack_weapon_back": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack-weapon",
                    "hero-attack-back",
                    f"hero-attack-back-weapon-{x}.png"
                )
            )
            for x in range(1, 4)
        ],

        "attack_weapon_front": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack-weapon",
                    "hero-attack-front",
                    f"hero-attack-front-weapon-{x}.png"
                )
            )
            for x in range(1, 4)
        ],

        "attack_weapon_side": [
            load_image(
                os.path.join(
                    HERO_PATH,
                    "attack-weapon",
                    "hero-attack-side",
                    f"hero-attack-side-weapon-{x}.png"
                )
            )
            for x in range(1, 4)
        ]
    }


# =====================================================
# LOAD ARROW SPRITE
# =====================================================

def load_arrow_sprite():

    return load_image(
        ARROW_PATH
    )
