import pygame

class Background:
    def __init__(self, screen, type, mountain_type):
        self.scroll = 0
        self.screen = screen
        self.speed = 1
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

        self.mountain_scroll = 0
        if mountain_type == "winter":
            self.mountain_path = f'BG Images/mountains/winter/'
            self.mountain_num_images = 1
            self.mountain_scale = 2
            self.base_h = 140
            self.base_shift = 0.2
            self.horizontal_shift = 60
        elif mountain_type == "rocky":
            self.mountain_path = f"BG Images/mountains/rocky/"
            self.mountain_num_images = 2
            self.mountain_scale = 2
            self.base_h = 230
            self.base_shift = 0.3
            self.horizontal_shift = 60
        elif mountain_type == "day":
            self.mountain_path = f"BG Images/mountains/day/"
            self.mountain_num_images = 2
            self.mountain_scale = 1.5
            self.base_h = 0
            self.base_shift = 0.3
            self.horizontal_shift = 30
        elif mountain_type == "night":
            self.mountain_path = f"BG Images/mountains/night/"
            self.mountain_num_images = 1
            self.mountain_scale = 1.5
            self.base_h = -50
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
        self.speed = 0.5
        
        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'{self.path}{i}.png').convert_alpha()
            # Get the original width and height
            original_width, original_height = bg_image.get_size()
            
            # Scale the image height by 2 while maintaining aspect ratio
            scaled_image = pygame.transform.scale(bg_image, (original_width, 1.2*original_height))
            bg_images.append(scaled_image)

        bg_width = bg_images[0].get_width()
        bg_height = bg_images[0].get_height()
        for x in range(20):
            self.speed = 1
            for bg_image in bg_images:
                self.screen.blit(bg_image, ((x * bg_width) - self.speed*self.scroll, 0))
                self.speed += 0.3
        self.scroll += 1
        self.scroll = self.scroll%bg_width
    
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

        base_speed = self.speed
        for c in range(10):
            y = self.base_h + (c*self.base_shift*bg_height)
            base_speed = base_speed+1
            for x in range(20):
                self.speed = base_speed
                for bg_image in bg_images:
                    self.screen.blit(bg_image, ((x * bg_width)-self.horizontal_shift*c - self.speed*self.mountain_scroll, y)) 
                    self.speed += 0.3
        
        self.mountain_scroll += 1
        self.mountain_scroll = self.mountain_scroll%bg_width

    def draw_tree(self):

        bg_images = []
        for i in range(1, self.num_images+1):
            bg_image = pygame.image.load(f'BG Images/summer_pine_tree_tiles.png').convert_alpha()
            bg_images.append(bg_image)

        bg_width = bg_images[0].get_width()

        for x in range(5):
            for bg_image in bg_images:
                self.screen.blit(bg_image, ((x * bg_width),500))
