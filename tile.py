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
    
    def hit_by_bullet(self, bullet):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)

class BrickTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.health = 2
        self.name = "Brick"

        self.image = self.images["small"]
        self._get_rect_and_size((self.x_pos, self.y_pos))
    
    def hit_by_bullet(self, bullet):
        bullet.update_owner()
        bullet.kill()
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return
        if bullet.direction == "Left":
            self.image = self.images["small_left"]
            self._get_rect_and_size((self.x_pos, self.y_pos))
        elif bullet.direction == "Right":
            self.image = self.images["small_right"]
            self._get_rect_and_size((self.x_pos + self.width//2, self.y_pos))
        elif bullet.direction == "Up":
            self.image = self.images["small_top"]
            self._get_rect_and_size((self.x_pos, self.y_pos))
        elif bullet.direction == "Down":
            self.image = self.images["small_bot"]
            self._get_rect_and_size((self.x_pos, self.y_pos + self.height//2))

class SteelTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.name = "Steel"
        self.image = self.images["small"]
        self._get_rect_and_size((self.x_pos, self.y_pos))
    
    def hit_by_bullet(self, bullet):
        bullet.update_owner()
        bullet.kill()

class ForestTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)

        self.image = self.images["small"]
        self._get_rect_and_size((self.x_pos, self.y_pos))

class IceTile(ForestTile):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)

        self.image = self.images["small"]
        self._get_rect_and_size((self.x_pos, self.y_pos))
    
class WaterTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)

        self.image = self.images["small_1"]
        self._get_rect_and_size((self.x_pos, self.y_pos))

        self.frame_index = 0
        self.timer = pygame.time.get_ticks()
    
    def update(self):
        if pygame.time.get_ticks() - self.timer >= 500:
            self.frame_index = 1 if self.frame_index == 0 else 0
            self.timer = pygame.time.get_ticks()
            self.image = self.images[f"small_{self.frame_index + 1}"]