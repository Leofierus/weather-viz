import pygame
import os


class TileSheet:
    def __init__(self, folder_path, season):
        self.tiles = {}
        season_folder = str(os.path.join(folder_path, season))

        if not os.path.exists(season_folder):
            raise ValueError(f"Season folder '{season_folder}' does not exist.")

        # Load all images in the folder
        for filename in os.listdir(season_folder):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                # Load the image and convert for Pygame
                image_path = os.path.join(season_folder, filename)
                image = pygame.image.load(image_path).convert_alpha()

                # Use the filename (without extension) as the key
                key = os.path.splitext(filename)[0]
                self.tiles[key] = image

    def get_tile_by_name(self, name):
        return self.tiles.get(name)

    def get_keys(self):
        return self.tiles.keys()

    def draw(self, screen, scale_factor=2, padding=5):
        tile_width = next(iter(self.tiles.values())).get_width() * scale_factor
        tile_height = next(iter(self.tiles.values())).get_height() * scale_factor

        x = padding
        y = padding

        for name, tile in self.tiles.items():
            # Scale the tile
            scaled_tile = pygame.transform.scale(tile, (tile_width, tile_height))

            # Draw the tile
            screen.blit(scaled_tile, (x, y))

            # Move to the next position
            x += tile_width + padding
            if x + tile_width > screen.get_width():
                x = padding
                y += tile_height + padding
