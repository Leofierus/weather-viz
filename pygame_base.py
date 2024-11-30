import time

import pygame
from tilegrabber import TileSheet
from background import Background


def draw_terrain(screen, tiles, temperature_data, start_x, start_y, block_width, block_height):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    if temperature_data[0] > temperature_data[-1]:
        change = "decline"
        x = start_x
    else:
        change = "incline"
        x = start_x-block_width

    y = start_y

    surface_tile = tiles.get_tile_by_label("surface_filler")
    incline_tile = tiles.get_tile_by_label("surface_left_edge")
    decline_tile = tiles.get_tile_by_label("surface_right_edge")
    left_wall_tile = tiles.get_tile_by_label("left_wall")
    right_wall_tile = tiles.get_tile_by_label("right_wall")
    bottom_left_wall_tile = tiles.get_tile_by_label("bottom_left_wall")
    bottom_right_wall_tile = tiles.get_tile_by_label("bottom_right_wall")
    bottom_filler_tile = tiles.get_tile_by_label("bottom_filler")
    filler_tile = tiles.get_tile_by_label("filler")

    surface_positions = []

    for i in range(len(temperature_data) - 1):
        temp_diff = temperature_data[i] - temperature_data[i + 1]
        steps = int(temp_diff)  # Map temperature difference to steps

        if change == "incline":
            if steps > 0:  # Decline
                for _ in range(steps):
                    x += block_width
                    y += block_height  # Move downward
                    screen.blit(decline_tile, (x, y))
                    surface_positions.append((x, y))
            elif steps < 0:  # Incline
                for _ in range(abs(steps)):
                    x += block_width
                    y -= block_height  # Move upward
                    screen.blit(incline_tile, (x, y))
                    surface_positions.append((x, y))
            else:  # Flat
                x += block_width  # Move horizontally
                screen.blit(surface_tile, (x, y))
                surface_positions.append((x, y))
        else:
            if steps > 0:  # Decline
                for _ in range(steps):
                    screen.blit(decline_tile, (x, y))
                    surface_positions.append((x, y))
                    x += block_width
                    y += block_height  # Move downward
            elif steps < 0:  # Incline
                for _ in range(abs(steps)):
                    screen.blit(incline_tile, (x, y))
                    surface_positions.append((x, y))
                    x += block_width
                    y -= block_height  # Move upward
            else:  # Flat
                screen.blit(surface_tile, (x, y))
                surface_positions.append((x, y))
                x += block_width  # Move horizontally

        # Ensure we stop drawing at the screen boundary
        if x >= screen.get_width():
            break

    for surface_x, surface_y in surface_positions:
        current_x, current_y = surface_x, surface_y

        # Fill downwards from the surface block
        while current_y + block_height < screen_height:
            current_y += block_height
            if current_x == start_x:  # Left wall
                screen.blit(left_wall_tile, (current_x, current_y))
            elif current_x + block_width >= screen_width:  # Right wall
                screen.blit(right_wall_tile, (current_x, current_y))
            else:
                screen.blit(filler_tile, (current_x, current_y))

    for bottom_x in range(start_x, screen_width, block_width):
        bottom_y = screen_height - block_height
        if bottom_x == start_x:  # Bottom left corner
            screen.blit(bottom_left_wall_tile, (bottom_x, bottom_y))
        elif bottom_x + block_width >= screen_width:  # Bottom right corner
            screen.blit(bottom_right_wall_tile, (bottom_x, bottom_y))
        else:  # Bottom filler
            screen.blit(bottom_filler_tile, (bottom_x, bottom_y))

    return surface_positions


def generate_temperature_data(prev_hour_temp, next_hour_temp, screen_width):
    step = (next_hour_temp - prev_hour_temp) / (screen_width - 1)
    temperature_data = [int(prev_hour_temp + step * i) for i in range(screen_width)]

    return temperature_data


def screen_init(bg_image_path, tile_path, prev_hour_temp, next_hour_temp, cloud_type, width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # change type here
    background = Background(screen, cloud_type)

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

    # Make sure temp data is in Celsius
    temperature_data = generate_temperature_data(prev_hour_temp, next_hour_temp, width//16 + 1)

    start_x = 0
    start_y = int(height * 0.75)
    block_width = 16
    block_height = 16

    run = True
    while run:
        background.draw_sky()
        surface_positions = draw_terrain(screen, tiles, temperature_data, start_x, start_y, block_width, block_height)
        pygame.display.flip()

        # replace the sky type here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/1 - Grassland/Terrain (16 x 16).png"
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/2 - Autumn Forest/Terrain (16 x 16).png"
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/3 - Tropics/Terrain (16 x 16).png"
    tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/4 - Winter World/Terrain (16 x 16).png"

    image_path = "BG Images/free-nature-pixel-backgrounds-for-games/nature 4/origbig.png"
    screen_init(image_path, tile_path, 26, 31, "dark_clouds", 1200, 800)
