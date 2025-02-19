import pygame
import gameconfig as gc


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, color="Silver", tank_level=0):
        super().__init__()
        # Game object and assets
        self.game = game
        self.assets = assets
        self.groups = groups

        # Sprite groups that may interact with tank
        self.tank_group = self.groups["All_Tanks"]

        # Add tank object to the sprite group
        self.tank_group.add(self)

        # Tank images
        self.tank_images = self.assets.tank_images

        # Tank position and direction
        self.spawn_pos = position
        self.x_pos, self.y_pos = self.spawn_pos
        self.direction = direction

        # Common tank attributes
        self.active = True
        self.tank_level = tank_level
        self.color = color

        # Tank image, rectangle and frame index
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))

    def input(self):
        pass

    def update(self):
        pass

    def draw(self, window):
        # If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
        
