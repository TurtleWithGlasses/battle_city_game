# Game Screen Settings
sprite_size = 16
sprite_scale = 4
image_size = sprite_size * sprite_scale

SCREENWIDTH = 16 * image_size
SCREENHEIGHT = 14 * image_size

# HUD overlay and game screen
GAME_SCREEN = (image_size, image_size // 2, image_size * 13, image_size * 13)
INFO_PANEL_X, INFO_PANEL_Y = SCREENWIDTH - (image_size * 2), image_size // 2
STD_ENEMIES = 20

# Game screen borders
SCREEN_BORDER_LEFT = GAME_SCREEN[0]
SCREEN_BORDER_TOP = GAME_SCREEN[1]
SCREEN_BORDER_RIGHT = GAME_SCREEN[2] + SCREEN_BORDER_LEFT
SCREEN_BORDER_BOTTOM = GAME_SCREEN[3] + SCREEN_BORDER_TOP

# FPS settings
FPS = 60

# Color definitions
BLACK = (0,0,0)
RED = (255, 0, 0)
GREY = (99, 99, 99)
GREEN = (0, 255, 0)

# Tank variables
TANK_SPEED = image_size // sprite_size

# Spritesheet images and coordinates
SPAWN_STAR = {"star_0": [(sprite_size * 16), (sprite_size * 6), sprite_size, sprite_size],
              "star_1": [(sprite_size * 17), (sprite_size * 6), sprite_size, sprite_size],
              "star_2": [(sprite_size * 18), (sprite_size * 6), sprite_size, sprite_size],
              "star_3": [(sprite_size * 19), (sprite_size * 6), sprite_size, sprite_size]}

SHIELD = {"shield_1": [(sprite_size * 16), (sprite_size * 9), 16, 16],
          "shield_2": [(sprite_size * 16), (sprite_size * 9), 16, 16]}

POWER_UPS = {"shield": [(16 * 16), (16 * 7), 16, 16],
             "freeze": [(16 * 17), (16 * 7), 16, 16],
             "frotify": [(16 * 18), (16 * 7), 16, 16],
             "power": [(16 * 19), (16 * 7), 16, 16],
             "explosion": [(16 * 20), (16 * 7), 16, 16],
             "extre_life": [(16 * 21), (16 * 7), 16, 16],
             "special": [(16 * 22), (16 * 7), 16, 16]}

SCORE = {"100": [(sprite_size * 18), (sprite_size * 10), 16, 16],
         "200": [(sprite_size * 19), (sprite_size * 10), 16, 16],
         "300": [(sprite_size * 20), (sprite_size * 10), 16, 16],
         "400": [(sprite_size * 21), (sprite_size * 10), 16, 16],
         "500": [(sprite_size * 22), (sprite_size * 10), 16, 16]}

FLAG = {"Phoenix_Alive": [(16 * 19), (16 * 2), 16, 16],
        "Phoenix_Dead": [(16 * 20), (16 * 2), 16, 16]}

EXPLOSIONS = {"explode_1": [(sprite_size * 16), (sprite_size * 8), 16, 16],
              "explode_2": [(sprite_size * 17), (sprite_size * 8), 16, 16],
              "explode_3": [(sprite_size * 18), (sprite_size * 8), 16, 16],
              "explode_4": [(sprite_size * 19), (sprite_size * 8), 32, 32],
              "explode_5": [(sprite_size * 21), (sprite_size * 8), 32, 32]}

BULLETS = {"Up": [(sprite_size * 20), (sprite_size * 6) + 4, 8, 8],
           "Left": [(sprite_size * 20) + 8, (sprite_size * 6) + 4, 8, 8],
           "Down": [(sprite_size * 21), (sprite_size * 6) + 4, 8, 8],
           "Right": [(sprite_size * 21) + 8, (sprite_size * 6) + 4, 8, 8]}

MAP_TILES = {
    #  Bricks
    432: {"small": [sprite_size * 16, sprite_size * 4, 8, 8],
          "small_right": [(sprite_size * 16) + 12, sprite_size * 4, 4, 8],
          "small_bot": [sprite_size * 17, (sprite_size * 4) + 4, 8, 4],
          "small_left": [(sprite_size * 17) + 8, sprite_size * 4, 4, 8],
          "small_top": [(sprite_size * 18), sprite_size * 4, 8, 4]},
    #  Steel
    482: {"small": [sprite_size * 16, (sprite_size * 4) + 8, 8, 8]},
    #  Forest
    483: {"small": [(sprite_size * 16) + 8, (sprite_size * 4) + 8, 8, 8]},
    #  Ice
    484: {"small": [(sprite_size * 17), (sprite_size * 4) + 8, 8, 8]},
    #  Water
    533: {"small_1": [(sprite_size * 16) + 8, (sprite_size * 5), 8, 8],
          "small_2": [(sprite_size * 17), (sprite_size * 5), 8, 8]}
}
HUD_INFO = {"stage":    [(16 * 20) + 8, (16 * 11), 40, 8],
            "num_0":    [(16 * 20) + 8, (16 * 11) + 8, 8, 8],
            "num_1":    [(16 * 21), (16 * 11) + 8, 8, 8],
            "num_2":    [(16 * 21) + 8, (16 * 11) + 8, 8, 8],
            "num_3":    [(16 * 22), (16 * 11) + 8, 8, 8],
            "num_4":    [(16 * 22) + 8, (16 * 11) + 8, 8, 8],
            "num_5":    [(16 * 20) + 8, (16 * 12), 8, 8],
            "num_6":    [(16 * 21), (16 * 12), 8, 8],
            "num_7":    [(16 * 21) + 8, (16 * 12), 8, 8],
            "num_8":    [(16 * 22), (16 * 12), 8, 8],
            "num_9":    [(16 * 22) + 8, (16 * 12), 8, 8],
            "life":     [(16 * 20), (16 * 12), 8, 8],
            "info_panel": [(16 * 23), (16 * 0), 32, (16 * 15)],
            "grey_square": [(16 * 23), (16 * 0), 8, 8]}

NUMS = {
    0: [0, 0, 8, 8], 1: [8, 0, 8, 8], 2: [16, 0, 8, 8], 3: [24, 0, 8, 8], 4: [32, 0, 8, 8],
    5: [0, 8, 8, 8], 6: [8, 8, 8, 8], 7: [16, 8, 8, 8], 8: [24, 8, 8, 8], 9: [32, 8, 8, 8]}

CONTEXT = {"pause": [(16 * 18), (16 * 11), 40, 8],
           "game_over": [(16 * 18), (16 * 11) + 8, 32, 16]}