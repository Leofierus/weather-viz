import pygame


def screen_init(background_image, width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    # Add origbig.png from background/background_image as the background
    background = pygame.image.load(f"background/{background_image}/orig.png")
    screen.blit(background, (0, 0))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


screen_init("clear_icy", 800, 600)
