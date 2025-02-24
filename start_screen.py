import pygame
import gameconfig as gc


class StartScreen:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        # Start screen coordiantes
        self.start_y = gc.SCREENHEIGHT
        self.end_y = 0

        # Start images and rectangle
        self.image = self.assets.start_screen
        self.rect = self.image.get_rect(topleft=(0,self.start_y))
        self.x, self.y = self.rect.topleft

        # Options positions
        self.option_positions = [
            (4 * gc.image_size, 7.75 * gc.image_size),
            (4 * gc.image_size, 8.75 * gc.image_size),
            (4 * gc.image_size, 9.75 * gc.image_size)
        ]

        self.token_index = 0
        self.token_image = self.assets.start_screen_token
        self.token_rect = self.token_image.get_rect(topleft=self.option_positions[self.token_index])

        self.start_screen_active = False
    
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                    return False
                
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self._switch_option_main_menu(-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self._switch_option_main_menu(+1)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._selected_option_action()

        return True

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)
        if self.start_screen_active:
            window.blit(self.token_image, self.token_rect)
    
    def _switch_option_main_menu(self, num):
        """Update the position of the token"""
        self.token_index += num
        self.token_index = self.token_index % len(self.option_positions)
        self.token_rect.topleft = self.option_positions[self.token_index]
    
    def _selected_option_action(self):
        if self.token_index == 0:
            print("Start a new game with 1 player")
        elif self.token_index == 1:
            print("Start a new game with 2 players")
        elif self.token_index == 2:
            print("Start the construction mode.")
