import pygame
import gameconfig as gc


class LevelEditor:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets
        self.active = True

        self.level_data = None
        self.all_levels = []

        self.overlay_screen = self.draw_screen()
        self.matrix = self.create_level_matrix()

        self.tile_type = {
            432: self.assets.brick_tiles["small"], 482: self.assets.steel_tiles["small"],
            483: self.assets.forest_tiles["small"], 484: self.assets.ice_tiles["small"],
            533: self.assets.water_tiles["small_1"], 999: self.assets.flag["Phoenix_Alive"]
        }
        self.inserts = [
            [-1, -1, -1, -1],       #  Empty Square
            [-1, 432, -1, 432],     #  Right Vertical brick
            [-1, -1, 432, 432],     #  Bottom Row brick
            [432, -1, 432, -1],     #  Left Vertical brick
            [432, 432, -1, -1],     #  Top Row brick
            [432, 432, 432, 432],   #  Full brick
            [-1, 482, -1, 482],     #  Steel Tiles Right Vert
            [-1, -1, 482, 482],     #  Steel tile Boottom Row
            [482, -1, 482, -1],     #  Steel Tile Left Vert
            [482, 482, -1, -1],     #  Steel Tile Top Row
            [482, 482, 482, 482],   #  Steel tile Full block
            [483, 483, 483, 483],   #  Full block Forest Tile
            [484, 484, 484, 484],   #  Full block ice Tile
            [533, 533, 533, 533],   #  Full Block Water Tile
        ]
        self.index = 0
        self.insert_tile = self.inserts[self.index]
        self.icon_image = self.assets.tank_images["Tank_4"]["Gold"]["Up"][0]
        self.icon_rect = self.icon_image.get_rect(topleft=(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP))


    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.icon_rect.x += gc.image_size
                    if self.icon_rect.x >= gc.SCREEN_BORDER_RIGHT:
                        self.icon_rect.x = gc.SCREEN_BORDER_RIGHT - gc.image_size
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.icon_rect.x -= gc.image_size
                    if self.icon_rect.x <= gc.SCREEN_BORDER_LEFT:
                        self.icon_rect.x = gc.SCREEN_BORDER_LEFT
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.icon_rect.y += gc.image_size
                    if self.icon_rect.y >= gc.SCREEN_BORDER_BOTTOM:
                        self.icon_rect.y = gc.SCREEN_BORDER_BOTTOM - gc.image_size
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.icon_rect.y -= gc.image_size
                    if self.icon_rect.y <= gc.SCREEN_BORDER_TOP:
                        self.icon_rect.y = gc.SCREEN_BORDER_TOP
                #  Cycle through insert pieces
                if event.key == pygame.K_SPACE:
                    self.index += 1
                    if self.index >= len(self.inserts):
                        self.index = self.index % len(self.inserts)
                    self.insert_tile = self.inserts[self.index]

    def update(self):
        icon_grid_pos_col = (self.icon_rect.left - gc.SCREEN_BORDER_LEFT) // (gc.image_size//2)
        icon_grid_pos_row = (self.icon_rect.top - gc.SCREEN_BORDER_TOP) // (gc.image_size//2)

        self.matrix[icon_grid_pos_row][icon_grid_pos_col] = self.insert_tile[0]
        self.matrix[icon_grid_pos_row][icon_grid_pos_col + 1] = self.insert_tile[1]
        self.matrix[icon_grid_pos_row + 1][icon_grid_pos_col] = self.insert_tile[2]
        self.matrix[icon_grid_pos_row + 1][icon_grid_pos_col + 1] = self.insert_tile[3]

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))
        self.draw_grid_to_screen(window)

        for i, row in enumerate(self.matrix):
            for j, tile in enumerate(row):
                if tile == -1:
                    continue
                else:
                    window.blit(self.tile_type[tile], (gc.SCREEN_BORDER_LEFT + (j * gc.image_size//2),
                                                       gc.SCREEN_BORDER_TOP + (i * gc.image_size//2)))

        window.blit(self.icon_image, self.icon_rect)
        pygame.draw.rect(window, gc.GREEN, self.icon_rect, 1)

    def draw_screen(self):
        """Create the game screen"""
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        return overlay_screen

    def draw_grid_to_screen(self, window):
        vert_lines = (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT) // (gc.image_size)
        hor_lines = (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP) // (gc.image_size)
        for i in range(vert_lines):
            pygame.draw.line(window, gc.RED, (gc.SCREEN_BORDER_LEFT + (i * gc.image_size), gc.SCREEN_BORDER_TOP),
                             (gc.SCREEN_BORDER_LEFT + (i * gc.image_size), gc.SCREEN_BORDER_BOTTOM))
        for i in range(hor_lines):
            pygame.draw.line(window, gc.RED, (gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP + (i * gc.image_size)),
                                             (gc.SCREEN_BORDER_RIGHT, gc.SCREEN_BORDER_TOP + (i * gc.image_size)))

    def create_level_matrix(self):
        rows = (gc.SCREEN_BORDER_BOTTOM - gc.SCREEN_BORDER_TOP) // (gc.image_size//2)
        columns = (gc.SCREEN_BORDER_RIGHT - gc.SCREEN_BORDER_LEFT) // (gc.image_size//2)
        matrix = []
        for row in range(rows):
            line = []
            for col in range(columns):
                line.append(-1)
            matrix.append(line)
        return matrix