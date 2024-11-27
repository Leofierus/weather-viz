import pygame

class Background:
    def __init__(self, screen, type):
        self.scroll = 0
        self.screen = screen
        if type == "day":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 1/'
            self.num_images = 4
        elif type == "night":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 3/'
            self.num_images = 4
        elif type == "sun_rise":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/sun_rise/'
            self.num_images = 3
        elif type == "sun_set":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 2/'
            self.num_images = 4
        elif type == "rainy":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/rainy/'
            self.num_images = 2
        elif type == "cloudy":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 5/'
            self.num_images = 5
        elif type == "dark_clouds":
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 7/'
            self.num_images = 4
        else:
            self.path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 1/'
            self.num_images = 4

    def draw_sky(self):

        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'{self.path}{i}.png').convert_alpha()
            bg_images.append(bg_image)

        bg_width = bg_images[0].get_width()

        for x in range(10):
            speed = 1
            for bg_image in bg_images:
                self.screen.blit(bg_image, ((x * bg_width) - speed*self.scroll, 0))
                speed += 0.3
        self.scroll += 1
        self.scroll = self.scroll%bg_width

    def draw_tree(self):

        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'BG Images/summer_pine_tree_tiles.png').convert_alpha()
            bg_images.append(bg_image)

        bg_width = bg_images[0].get_width()

        for x in range(5):
            for bg_image in bg_images:
                self.screen.blit(bg_image, ((x * bg_width),500))
