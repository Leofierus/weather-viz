import pygame

class Background:
    def __init__(self, screen, type, mountain_type):
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

        if mountain_type == "winter":
            self.mountain_path = f'BG Images/mountains/winter/'
            self.mountain_num_images = 1
            self.mountain_scale = 1.2
            self.base_h = 300
            self.base_shift = 0.3
            self.horizontal_shift = 30
        elif mountain_type == "rocky":
            self.mountain_path = f"BG Images/mountains/rocky/"
            self.mountain_num_images = 2
            self.mountain_scale = 1.2
            self.base_h = 400
            self.base_shift = 0.3
            self.horizontal_shift = 30
        elif mountain_type == "day":
            self.mountain_path = f"BG Images/mountains/day/"
            self.mountain_num_images = 2
            self.mountain_scale = 1.2
            self.base_h = 200
            self.base_shift = 0.3
            self.horizontal_shift = 30
        elif mountain_type == "night":
            self.mountain_path = f"BG Images/mountains/night/"
            self.mountain_num_images = 1
            self.mountain_scale = 1
            self.base_h = 200
            self.base_shift = 0.1
            self.horizontal_shift = 100
        else:
            self.mountain_path = f"BG Images/mountains/day/"
            self.mountain_num_images = 2
            self.mountain_scale = 1.2
            self.base_h = 200
            self.base_shift = 0.3
            self.horizontal_shift = 30


    def draw_sky(self):

        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'{self.path}{i}.png').convert_alpha()
            bg_images.append(bg_image)

        bg_width = bg_images[0].get_width()
        bg_height = bg_images[0].get_height()
        y = 3*bg_height
        for c in range(7):
            for x in range(10):
                speed = 1
                for bg_image in bg_images:
                    self.screen.blit(bg_image, ((x * bg_width) - speed*self.scroll, y))
                    speed += 0.3
            self.scroll += 1
            self.scroll = self.scroll%bg_width
            y = y - (0.5*bg_height)
    
    def draw_mountains(self):
        bg_images = []
        for i in range(1, self.mountain_num_images + 1):
            # Load the image
            bg_image = pygame.image.load(f'{self.mountain_path}{i}.png').convert_alpha()
            
            # Get the original width and height
            original_width, original_height = bg_image.get_size()
            
            # Scale the image height by 2 while maintaining aspect ratio
            scaled_image = pygame.transform.scale(bg_image, (original_width, self.mountain_scale*original_height))
            
            bg_images.append(scaled_image)

        bg_width = bg_images[0].get_width()
        bg_height = bg_images[0].get_height()

        for c in range(10):
            y = self.base_h + (c*self.base_shift*bg_height)
            for x in range(10):
                for bg_image in bg_images:
                    self.screen.blit(bg_image, ((x * bg_width)-self.horizontal_shift*c, y)) 

    def draw_tree(self):

        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'BG Images/summer_pine_tree_tiles.png').convert_alpha()
            bg_images.append(bg_image)

        bg_width = bg_images[0].get_width()

        for x in range(5):
            for bg_image in bg_images:
                self.screen.blit(bg_image, ((x * bg_width),500))
