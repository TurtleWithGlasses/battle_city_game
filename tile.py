import pygame
import gameconfig as gc


class TileType(pygame.sprite.Sprite):
    def __init__(self, pos, group, map_tile):
        super().__init__(group)
        self.group = group
        self.images = map_tile
        self.x_pos = pos[0]
        self.y_pos = pos[1]
    
    def update(self):
        pass

    def _get_rect_and_size(self, position):
        self.rect = self.image.get_rect(topleft=position)
        self.width, self.height = self.image.get_size()

    def draw(self, window):
        window.blit(self.image, self.rect)

class BrickTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.health = 2
        self.name = "Brick"

        self.image = self.images["small"]
        self._get_rect_and_size((self.x_pos, self.y_pos))