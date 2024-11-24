import pygame

def draw_sky(type, screen):

    if type == "day":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 1/'
        num_images = 4
    elif type == "night":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 3/'
        num_images = 4
    elif type == "sun_rise":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/sun_rise/'
        num_images = 3
    elif type == "sun_set":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 2/'
        num_images = 4
    elif type == "rainy":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/rainy/'
        num_images = 2
    elif type == "cloudy":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 5/'
        num_images = 5
    elif type == "dark_clouds":
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 7/'
        num_images = 4
    else:
        path = f'BG Images/free-sky-with-clouds-background-pixel-art-set/Clouds/Clouds 1/'
        num_images = 4

    bg_images = []
    for i in range(1, num_images+1):
        bg_image = pygame.image.load(f'{path}{i}.png').convert_alpha()
        bg_images.append(bg_image)

    bg_width = bg_images[0].get_width()

    for x in range(5):
        speed = 1
        for bg_image in bg_images:
            screen.blit(bg_image, ((x * bg_width),0))
            speed += 0.2


def draw_tree(type, screen):
    
    num_images = 1

    bg_images = []
    for i in range(1, num_images+1):
        bg_image = pygame.image.load(f'BG Images/summer_pine_tree_tiles.png').convert_alpha()
        bg_images.append(bg_image)

    bg_width = bg_images[0].get_width()

    for x in range(5):
        speed = 1
        for bg_image in bg_images:
            screen.blit(bg_image, ((x * bg_width),500))
            speed += 0.2