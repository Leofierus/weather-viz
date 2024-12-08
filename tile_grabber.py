import random

import pygame
import os


class TileSheet:
    def __init__(self, folder_path, season):
        self.tiles = {}
        self.active_leaves = []
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

    def animate_leaves(self, screen, speed, number_of_leaves, bottom_edge):
        screen_width, screen_height = screen.get_size()

        # Initialize leaves if it's the first frame
        if not self.active_leaves:
            for _ in range(number_of_leaves):
                leaf_key = random.choice(list(self.tiles.keys()))  # Random leaf
                x = random.randint(0, screen_width + 100)  # Spread horizontally across screen
                y = random.randint(0, bottom_edge)  # Random vertical position
                scale_factor = random.uniform(0.1, 1.0)  # Random size variation
                leaf_speed = random.uniform(speed - 3, speed + 3)  # Random speed per leaf
                self.active_leaves.append({
                    "key": leaf_key,
                    "x": x,
                    "y": y,
                    "scale": scale_factor,
                    "speed": leaf_speed  # Store speed individually for each leaf
                })
        # Update and draw each leaf
        for leaf in self.active_leaves:
            leaf["x"] -= leaf["speed"]  # Use each leaf's individual speed
            self.draw_by_key(screen, leaf["key"], leaf["x"], leaf["y"], leaf["scale"])

        # Remove leaves that are out of bounds
        self.active_leaves = [leaf for leaf in self.active_leaves if leaf["x"] + 20 > 0]  # Assuming leaf width <= 20

        while len(self.active_leaves) < number_of_leaves:
            leaf_key = random.choice(list(self.tiles.keys()))  # Random leaf
            x = random.randint(screen_width, screen_width + 100)  # Start off-screen
            y = random.randint(0, bottom_edge)  # Random vertical position
            scale_factor = random.uniform(0.5, 1.5)  # Random size variation
            leaf_speed = random.uniform(speed - 1, speed + 1)  # Random speed per leaf
            self.active_leaves.append({
                "key": leaf_key,
                "x": x,
                "y": y,
                "scale": scale_factor,
                "speed": leaf_speed
            })
