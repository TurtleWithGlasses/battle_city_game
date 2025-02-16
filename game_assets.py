import pygame
import gameconfig as gc


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

        # Score Sheet images
        score_images = ["hiScore", "arrow", "player1", "player2", "pts", "stage", "total"]
        self.score_sheet_images = {}
        for image in score_images:
            self.score_sheet_images[image] = self.load_individual_img(image)


    def load_individual_img(self, path, scale=False, size=(0, 0)):
        """Loading in of individual images"""
        image = pygame.image.load(f"assets\\{path}.png").convert_alpha()

        if scale:
            image = pygame.transform.scale(image, size)
        
        return image