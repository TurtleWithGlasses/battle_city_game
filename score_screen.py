import pygame
import gameconfig as gc


class ScoreScreen:
    def __init__(self, game, assets):
        self. game = game
        self.assets = assets
        self.white_nums = self.assets.number_black_white
        self.orange_nums = self.assets.number_black_orange
        
        self.active = False
        self.timer = pygame.time.get_ticks()

        self.images = self.assets.score_sheet_images

        # Player score totals and score lists
        self.p1_score = 3000
        self.p1_kill_list = []
        self.p2_score = 3500
        self.p2_kill_list = []

        self.top_score = 0
        self.stage = 0

        self.scoresheet = self.generate_scoresheet_screen()
        # Top score and stage number images creation
        self._create_top_score_and_stage_number_images()
        # Update player socre images with the last player score
        self.update_player_score_images()

        self.pl_1_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}
        self.pl_2_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}

        self.p1_tank_num_images, self.p1_tank_score_images = self.generate_tank_kill_images(14, 7, self.pl_1_score_values)
        self.p2_tank_num_images, self.p2_tank_score_images = self.generate_tank_kill_images(20, 25, self.pl_2_score_values)
        
    def update(self):
        if not pygame.time.get_ticks() - self.timer >= 10000:
            return
        
        self.active = False
        self.game.change_level(self.p1_score, self.p2_score)
    
    def draw(self, window):
        window.fill(gc.BLACK)
        window.blit(self.scoresheet, (0, 0))
        window.blit(self.hi_score_nums_total, self.hi_score_nums_rect)
        window.blit(self.stage_num, self.stage_num_rect)

        if self.game.player_1_active:
            window.blit(self.pl_1_score, self.pl_1_score_rect)
            for value in self.p1_tank_num_images.values():
                window.blit(value[0], value[1])
            for value in self.p1_tank_score_images.values():
                window.blit(value[0], value[1])
        
        if self.game.player_2_active:
            window.blit(self.pl_2_score, self.pl_2_score_rect)
            for value in self.p2_tank_num_images.values():
                window.blit(value[0], value[1])
            for value in self.p2_tank_score_images.values():
                window.blit(value[0], value[1])

    
    def generate_scoresheet_screen(self):
        """Generate a basic template screen for the score card transition"""
        surface = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        surface.fill(gc.BLACK)
        new_img = gc.image_size // 2
        surface.blit(self.images["hiScore"], (new_img * 8, new_img * 4))
        surface.blit(self.images["stage"], (new_img * 12, new_img * 6))
        
        arrow_left = self.images["arrow"]
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        if self.game.player_1_active:
            surface.blit(self.images["player1"], (new_img * 3, new_img * 8))
        if self.game.player_2_active:
            surface.blit(self.images["player2"], (new_img * 21, new_img * 8))

        for num, y_pos in enumerate([12.5, 15, 17.5, 20]):
            if self.game.player_1_active:
                surface.blit(self.images["pts"], (new_img * 8, new_img * y_pos))
                surface.blit(arrow_left, (new_img * 14, new_img * y_pos))
            if self.game.player_2_active:
                surface.blit(self.images["pts"], (new_img * 26, new_img * y_pos))
                surface.blit(arrow_right, (new_img * 17, new_img * y_pos))
            surface.blit(self.assets.tank_images[f"Tank_{num + 4}"]["Silver"]["Up"][0], (new_img * 15, new_img * (y_pos - 0.5)))
        

        surface.blit(self.images["total"], (new_img * 6, new_img * 22))
        return surface

    def number_image(self, score, number_color):
        """Convert a number into an image"""
        num = str(score)
        length = len(num)
        score_surface = pygame.Surface((gc.image_size // 2 * length, gc.image_size // 2))
        for index, number in enumerate(num):
            score_surface.blit(number_color[int(number)], (gc.image_size // 2 * index, 0))
        return score_surface

    def update_player_score_images(self):
        if self.game.player_1_active:
            self.pl_1_score = self.number_image(self.p1_score, self.orange_nums)
            self.pl_1_score_rect = self.pl_1_score.get_rect(
                topleft=(gc.image_size // 2 * 11 - self.pl_1_score.get_width(), gc.image_size // 2 * 10)
            )

        if self.game.player_2_active:
            self.pl_2_score = self.number_image(self.p2_score, self.orange_nums)
            self.pl_2_score_rect = self.pl_2_score.get_rect(
                topleft=(gc.image_size // 2 * 29 - self.pl_2_score.get_width(), gc.image_size // 2 * 10)
        )
    
    def _create_top_score_and_stage_number_images(self):
        self.hi_score_nums_total = self.number_image(self.top_score, self.orange_nums)
        self.hi_score_nums_rect = self.hi_score_nums_total.get_rect(topleft=(gc.image_size//2 * 19, gc.image_size//2 * 4))
        self.stage_num = self.number_image(self.stage, self.white_nums)
        self.stage_num_rect = self.stage_num.get_rect(topleft=(gc.image_size//2 * 19, gc.image_size//2 * 6))
    
    def update_basic_info(self, top_score, stage_number):
        self.top_score = top_score
        self.stage = stage_number
        self._create_top_score_and_stage_number_images()
    
    def generate_tank_kill_images(self, x1, x2, pl_dict):
        """Generate a dictionary of images and x/y coordinates for values"""
        y_pos = [12.5, 15, 17.5, 20]
        size = gc.image_size // 2

        # Generate the number images for the tank numbers
        tank_num_imgs = {}
        for i in range(4):
            tank_num_imgs[f"line{i+1}"] = []
            tank_num_imgs[f"line{i+1}"].append(self.number_image(pl_dict[f"line{i+1}"][0], self.white_nums))
            tank_num_imgs[f"line{i+1}"].append((size * x1 - tank_num_imgs[f"line{i+1}"][0].get_width(), size * y_pos[i]))
        tank_num_imgs["total"] = []
        tank_num_imgs["total"].append(self.number_image(pl_dict["total"], self.white_nums))
        tank_num_imgs["total"].append((size * x1 - tank_num_imgs["total"][0].get_width(), size * 22.5))

        # Generate images for tank score per line
        tank_score_imgs = {}
        for i in range(4):
            tank_score_imgs[f"line{i+1}"] = []
            tank_score_imgs[f"line{i+1}"].append(self.number_image(pl_dict[f"line{i+1}"][0], self.white_nums))
            tank_score_imgs[f"line{i+1}"].append((size * x2 - tank_score_imgs[f"line{i+1}"][0].get_width(), size * y_pos[i]))
        return tank_num_imgs, tank_score_imgs