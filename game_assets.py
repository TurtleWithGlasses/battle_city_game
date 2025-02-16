import pygame
import gameconfig as gc
import os


class GameAssets:
    def __init__(self):
        """Object containing all of the assets for the game"""
        # Start screen images
        self.start_screen = self.load_individual_img("start_screen", True, (gc.SCREENWIDTH, gc.SCREENHEIGHT))
        self.start_screen_token = self.load_individual_img("token", True, (gc.image_size, gc.image_size))

        # Loading in the Sprite Sheets
        self.sprite_sheet = self.load_individual_img("BattleCity")
        self.number_image_black_white = self.load_individual_img("numbers_black_white")
        self.number_image_black_orange = self.load_individual_img("numbers_black_orange")

        self.tank_images = self._load_all_tank_images()

        # Score Sheet images
        score_images = ["hiScore", "arrow", "player1", "player2", "pts", "stage", "total"]
        self.score_sheet_images = {}
        for image in score_images:
            self.score_sheet_images[image] = self.load_individual_img(image)


    def _load_all_tank_images(self):
        """Get all the tank images from the spritesheet"""        
        tank_image_dict = {}
        for tank in range(8):
            tank_image_dict[f"Tank_{tank}"] = {}
            for group in ["Gold","Silver", "Green", "Special"]:
                tank_image_dict[f"Tank_{tank}"][group] = {}
                for direction in ["Up", "Left", "Down", "Right"]:
                    tank_image_dict[f"Tank_{tank}"][group][direction] = []
        
        # Create a new image for each of the tanks
        for row in range(16):
            for col in range(16):
                surface = pygame.Surface((gc.sprite_size, gc.sprite_size))
                surface.fill(gc.BLACK)
                surface.blit(self.sprite_sheet, (0, 0), (col * gc.sprite_size, row * gc.sprite_size, gc.sprite_size, gc.sprite_size))
                surface.set_colorkey(gc.BLACK)
                # Resize each of the images
                surface = self.scale_image(surface, gc.image_size)
                # Sort the tank image in to its correct level
                tank_level = self._sort_tanks_into_levels(row)
                # Sort the tank int oits correct group
                tank_group = self._sort_tanks_into_groups(row, col)
                # Sort tank images into correct directions
                tank_direction = self._sort_tanks_by_direction(col)

                tank_image_dict[tank_level][tank_group][tank_direction].append(surface)
        return tank_image_dict

    # Sorting methods for getting tanks into the correct segments of the dictionary
    def scale_image(self, image, scale):
        """Scale the image according to the size passed in"""
        image = pygame.transform.scale(image, (scale, scale))
        return image
    
    def _sort_tanks_into_levels(self, row):
        """Sorts the tanks according to the row"""
        tank_levels = {0: "Tank_0", 1: "Tank_1", 2: "Tank_2", 3: "Tank_3",
                       4: "Tank_4", 5: "Tank_5", 6: "Tank_6", 7: "Tank_7"}
        return tank_levels[row % 8]

    def _sort_tanks_into_groups(self, row, col):
        """Sort each tank image into its different color groups"""
        if 0 <= row <= 7 and 0 <= col <= 7:
            return "Gold"
        elif 8 <= row <= 16 and 0 <= col <= 7:
            return "Green"
        elif 0 <= row <= 7 and 8 <= col <= 16:
            return "Silver"
        else:
            return "Special"
    
    def _sort_tanks_by_direction(self, col):
        """Returns the current tank image by direction"""
        if col % 7 <= 1:
            return "Up"
        elif col % 7 <= 3:
            return "Left"
        elif col % 7 <= 5:
            return "Down"
        else:
            return "Right"

    def load_individual_img(self, path, scale=False, size=(0, 0)):
        """Loading in of individual images"""
        image_path = os.path.join("assets", f"{path}.png")
        image = pygame.image.load(image_path).convert_alpha()

        if scale:
            image = pygame.transform.scale(image, size)
        
        return image