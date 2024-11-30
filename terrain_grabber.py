import pygame


class TerrainSheet:
    def __init__(self, filename, width, height, rows, cols):
        image = pygame.image.load(filename).convert()
        print(f"Image dimensions: {image.get_width()} x {image.get_height()}")

        self.tile_table = []
        self.usable_tiles = []
        self.tile_labels = {}

        for tile_x in range(cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(rows):
                rect = (tile_x * width, tile_y * height, width, height)
                tile = image.subsurface(rect)

                if not self._is_empty(tile):
                    self.usable_tiles.append(tile)

                line.append(tile)

    def label_tiles(self, labels):
        tile_indices = [0, 2, 17, 5, 12, 18, 1, 3, 22]
        for i, label in zip(tile_indices, labels):
            self.tile_labels[label] = self.usable_tiles[i]

    def _is_empty(self, tile):
        pixel_data = pygame.image.tostring(tile, "RGBA")
        first_pixel = pixel_data[:4]
        for i in range(0, len(pixel_data), 4):
            if pixel_data[i:i + 4] != first_pixel:
                return False
        return True

    def get_tile_by_label(self, label):
        return self.tile_labels[label]

    def draw(self, screen, with_labels=False, scale_factor=2, padding=5):
        if with_labels:
            screen.fill((0, 0, 0))  # Clear the screen with black
            font = pygame.font.SysFont("Arial", 20)  # Initialize font for labels
            tile_width = self.usable_tiles[0].get_width() * scale_factor
            tile_height = self.usable_tiles[0].get_height() * scale_factor

            for i, (label, tile) in enumerate(self.tile_labels.items()):
                # Calculate vertical position for the tile and label
                y = i * (tile_height + padding)  # Stack vertically with padding
                x_tile = padding  # Fixed left margin for tiles
                x_label = x_tile + tile_width + padding  # Label to the right of the tile

                # Scale and draw the tile
                scaled_tile = pygame.transform.scale(tile, (tile_width, tile_height))
                screen.blit(scaled_tile, (x_tile, y))

                # Render and draw the label
                text_surface = font.render(label, True, (255, 255, 255))
                screen.blit(text_surface,
                            (x_label, y + (tile_height - text_surface.get_height()) // 2))  # Center label vertically
        else:
            tile_width = self.tile_table[0][0].get_width() * scale_factor
            tile_height = self.tile_table[0][0].get_height() * scale_factor

            for x, row in enumerate(self.tile_table):
                for y, tile in enumerate(row):
                    # Scale the tile before drawing
                    scaled_tile = pygame.transform.scale(tile, (tile_width, tile_height))
                    screen.blit(scaled_tile, (x * (tile_width + padding), y * (tile_height + padding)))
