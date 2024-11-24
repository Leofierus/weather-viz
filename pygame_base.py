import time

import pygame
from tilegrabber import TileSheet
from background import draw_sky, draw_tree

def screen_init(bg_image_path, tile_path, width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # replace the sky type here
    draw_sky("day", screen)
    draw_tree("day", screen)

    pygame.display.flip()

    tiles = TileSheet(tile_path,16, 16, 10, 17)
    print(f"Number of usable tiles: {len(tiles.usable_tiles)}")

    tiles.draw(screen)  # Draw all tiles
    pygame.display.flip()

    tile_labels = [
        "surface_left_edge", "surface_filler", "surface_right_edge",
        "left_wall", "filler", "right_wall",
        "bottom_left_wall", "bottom_filler", "bottom_right_wall"
    ]
    tiles.label_tiles(tile_labels)

    # tiles.draw(screen, with_labels=True, padding=20)  # Draw labeled tiles
    # pygame.display.flip()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/1 - Grassland/Terrain (16 x 16).png"
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/2 - Autumn Forest/Terrain (16 x 16).png"
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/3 - Tropics/Terrain (16 x 16).png"
    tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/4 - Winter World/Terrain (16 x 16).png"

    image_path = "BG Images/free-nature-pixel-backgrounds-for-games/nature 4/origbig.png"
    screen_init(image_path, tile_path, 1200, 800)
