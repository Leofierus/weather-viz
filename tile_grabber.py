import pygame
import os


class TileSheet:
    def __init__(self, folder_path, season):
        self.tiles = {}
        season_folder = str(os.path.join(folder_path, season))

        if not os.path.exists(season_folder):
            raise ValueError(f"Season folder '{season_folder}' does not exist.")

        for filename in os.listdir(season_folder):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(season_folder, filename)
                image = pygame.image.load(image_path).convert_alpha()

                key = os.path.splitext(filename)[0]
                self.tiles[key] = image

    def get_tile_by_name(self, name):
        return self.tiles.get(name)

    def get_data(self):
        data = {}
        for key, value in self.tiles.items():
            data[key] = (value.get_width(), value.get_height())
        return data

    def draw(self, screen, scale_factor=2, padding=5):
        try:
            tile_width = next(iter(self.tiles.values())).get_width() * scale_factor
            tile_height = next(iter(self.tiles.values())).get_height() * scale_factor

            x = padding
            y = padding

            for name, tile in self.tiles.items():
                scaled_tile = pygame.transform.scale(tile, (tile_width, tile_height))
                screen.blit(scaled_tile, (x, y))

                x += tile_width + padding
                if x + tile_width > screen.get_width():
                    x = padding
                    y += tile_height + padding
        except StopIteration:
            print("No tiles found in the TileSheet.")

    def draw_by_key(self, screen, key, x, y, scale_factor=1):
        tile = self.get_tile_by_name(key)
        if tile is not None:
            if scale_factor != 1:
                width = int(tile.get_width() * scale_factor)
                height = int(tile.get_height() * scale_factor)
                tile = pygame.transform.scale(tile, (width, height))

            screen.blit(tile, (x, y))
        else:
            print(f"Tile with key '{key}' not found.")
