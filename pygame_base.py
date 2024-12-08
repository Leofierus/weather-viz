import random
import time

import pygame
from terrain_grabber import TerrainSheet
from background import Background
from tile_grabber import TileSheet


def draw_terrain(screen, tiles, temperature_data, start_x, start_y, block_width, block_height):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    if temperature_data[0] > temperature_data[-1]:
        change = "decline"
        x = start_x
    else:
        change = "incline"
        x = start_x - block_width

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
    temperature_data = [int(prev_hour_temp)] * 20

    remaining_width = screen_width - 20
    if remaining_width > 0:
        step = (next_hour_temp - prev_hour_temp) / remaining_width
        temperature_data += [int(prev_hour_temp + step * i) for i in range(1, remaining_width + 1)]

    return temperature_data


def add_weather(screen, is_windy, wind_speed, weather_type, number_of_particles):
    screen_width, screen_height = screen.get_size()
    if not hasattr(add_weather, "active_particles"):
        add_weather.active_particles = []

    # Weather assets
    rain_drop = pygame.image.load("misc/weather/rain_drop.png").convert_alpha()
    snowflake_soft = pygame.image.load("misc/weather/snowflake_soft.png").convert_alpha()
    snowflake_hard = pygame.image.load("misc/weather/snowflake_hard.png").convert_alpha()

    max_slant = min(45, 5 + wind_speed)
    slant_angle = random.uniform(5, max_slant)
    slant = -slant_angle if random.choice([True, True, True, True, False]) else slant_angle

    # Create new particles
    while len(add_weather.active_particles) < number_of_particles:
        x = random.randint(0, screen_width)
        y = random.randint(-500, 0)
        size = random.uniform(0.3, 1.0)
        speed = random.uniform(1, 3) + (wind_speed / 10)
        if weather_type == "rain":
            add_weather.active_particles.append({
                "image": rain_drop,
                "x": x,
                "y": y,
                "size": size,
                "speed_x": slant / 10,
                "speed_y": speed * 4.0,
            })
        elif weather_type == "light_snow":
            add_weather.active_particles.append({
                "image": snowflake_soft,
                "x": x,
                "y": y,
                "size": size,
                "speed_x": slant / 15,
                "speed_y": speed * 0.5,
            })
        elif weather_type == "heavy_snow":
            add_weather.active_particles.append({
                "image": snowflake_hard,
                "x": x,
                "y": y,
                "size": size,
                "speed_x": slant / 12,
                "speed_y": speed * 4.2,
            })
        elif weather_type == "mix":
            if random.random() < 0.5:
                particle_image = random.choice([rain_drop])
                add_weather.active_particles.append({
                    "image": particle_image,
                    "x": x,
                    "y": y,
                    "size": size,
                    "speed_x": slant / 13,
                    "speed_y": speed * 4.0,
                })
            else:
                particle_image = random.choice([snowflake_soft, snowflake_hard])
                add_weather.active_particles.append({
                    "image": particle_image,
                    "x": x,
                    "y": y,
                    "size": size,
                    "speed_x": slant / 13,
                    "speed_y": speed * 1.2,
                })

    for particle in add_weather.active_particles:
        particle["x"] += particle["speed_x"]
        particle["y"] += particle["speed_y"]

        scaled_particle = pygame.transform.scale(
            particle["image"],
            (
                int(particle["image"].get_width() * particle["size"]),
                int(particle["image"].get_height() * particle["size"]),
            )
        )
        screen.blit(scaled_particle, (particle["x"], particle["y"]))

    add_weather.active_particles = [
        particle for particle in add_weather.active_particles
        if particle["x"] > -50 and particle["x"] < screen_width + 50 and particle["y"] < screen_height
    ]


def add_thunder(screen, surface_positions, number):
    screen_width, screen_height = screen.get_size()
    upper_third = screen_height // 4

    if not hasattr(add_thunder, "lightning_animations"):
        add_thunder.lightning_animations = {
            1: [pygame.image.load(f"misc/lightning/lightning_1/{i}.png").convert_alpha() for i in range(1, 10)],
            2: [pygame.image.load(f"misc/lightning/lightning_2/{i}.png").convert_alpha() for i in range(1, 17)],
            3: [pygame.image.load(f"misc/lightning/lightning_3/{i}.png").convert_alpha() for i in range(1, 10)],
            4: [pygame.image.load(f"misc/lightning/lightning_4/{i}.png").convert_alpha() for i in range(1, 10)],
        }
        add_thunder.last_strike_time = 0
        add_thunder.active_strikes = []

    current_time = pygame.time.get_ticks() / 1000
    interval = 10 / number

    if current_time - add_thunder.last_strike_time > interval:
        strike_type = random.choice([1, 2, 3, 4])
        animation_frames = add_thunder.lightning_animations[strike_type]
        duration = len(animation_frames) * 0.1

        if strike_type in [1, 2]:
            x = random.randint(0, screen_width)
            add_thunder.active_strikes.append({
                "type": "cloud_to_land",
                "x_start": x,
                "y_start": 0,
                "y_end": add_thunder.lightning_animations[strike_type][2].get_height(),
                "frames": animation_frames,
                "current_frame": 0,
                "start_time": current_time,
                "duration": duration,
            })
        else:
            x_start = random.randint(0, screen_width)
            x_end = 16 + x_start
            y_level = random.randint(0, upper_third)
            add_thunder.active_strikes.append({
                "type": "cloud_to_cloud",
                "x_start": x_start,
                "y_start": y_level,
                "x_end": x_end,
                "y_end": y_level,
                "frames": animation_frames,
                "current_frame": 0,
                "start_time": current_time,
                "duration": duration,
            })
        add_thunder.last_strike_time = current_time

    for strike in add_thunder.active_strikes:
        elapsed_time = current_time - strike["start_time"]
        if elapsed_time > strike["duration"]:
            continue

        frame_index = int(elapsed_time / 0.1)
        if frame_index < len(strike["frames"]):
            strike["current_frame"] = frame_index
            frame = strike["frames"][frame_index]

            if strike["type"] == "cloud_to_land":
                x = strike["x_start"]
                y_start = strike["y_start"]
                y_end = strike["y_end"]
                frame_height = frame.get_height()

                for y in range(y_start, y_end, frame_height):
                    screen.blit(frame, (x, y))
            elif strike["type"] == "cloud_to_cloud":
                x_start = strike["x_start"]
                y_start = strike["y_start"]
                x_end = strike["x_end"]
                y_end = strike["y_end"]

                for i in range(frame_index + 1):
                    x = x_start + (x_end - x_start) * (i / len(strike["frames"]))
                    y = y_start + (y_end - y_start) * (i / len(strike["frames"]))
                    screen.blit(frame, (x, y))

    add_thunder.active_strikes = [
        strike for strike in add_thunder.active_strikes
        if current_time - strike["start_time"] < strike["duration"]
    ]


def add_text(screen, text):
    if not hasattr(add_text, "font_size"):
        add_text.font_size = 27
        add_text.increasing = True
        add_text.max_size = 27
        add_text.min_size = 27
        add_text.counter = 0

    if add_text.increasing and add_text.counter % 15 == 0:
        add_text.font_size += 1
        if add_text.font_size >= add_text.max_size:
            add_text.increasing = False
    elif not add_text.increasing and add_text.counter % 15 == 0:
        add_text.font_size -= 1
        if add_text.font_size <= add_text.min_size:
            add_text.increasing = True
    add_text.counter += 1

    retro_font = pygame.font.Font("misc/font.ttf", add_text.font_size)
    rendered_text = retro_font.render(text, True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    text_position = (10, screen_height - rendered_text.get_height() - 10)

    screen.blit(rendered_text, text_position)


def screen_init(tile_path, prev_hour_temp, next_hour_temp, cloud_type, mountain_type, season, is_windy, wind_speed,
                is_lightning, number_of_strikes_10s, weather_effects, weather_type, weather_intensity, screen_text,
                width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # change type here
    background = Background(screen, cloud_type, mountain_type)

    tiles = TerrainSheet(tile_path, 16, 16, 10, 17)
    print(f"Number of usable tiles: {len(tiles.usable_tiles)}")

    # tiles.draw(screen)
    # pygame.display.flip()

    tile_labels = [
        "surface_left_edge", "surface_filler", "surface_right_edge",
        "left_wall", "filler", "right_wall",
        "bottom_left_wall", "bottom_filler", "bottom_right_wall"
    ]
    tiles.label_tiles(tile_labels)

    # tiles.draw(screen, with_labels=True, padding=20)  # Draw labeled tiles
    # pygame.display.flip()

    house = TileSheet("misc/houses", season)
    house_data = house.get_data()

    leaves = TileSheet("misc/leaves", season)
    leaf_data = leaves.get_data()

    trees = TileSheet("misc/trees", season)
    tree_data = trees.get_data()
    bushes = [key for key in tree_data.keys() if key.startswith("bush")]
    trees_list = [key for key in tree_data.keys() if key.startswith("tree")]

    if len(bushes) < 2 or len(trees_list) < 2:
        raise ValueError("Not enough bushes or trees available in the tileset.")

    selected_bushes = random.sample(bushes, 2)
    selected_trees = random.sample(trees_list, 2)

    # trees_2.draw(screen)
    # pygame.display.flip()
    # time.sleep(5)

    temperature_data = generate_temperature_data(prev_hour_temp, next_hour_temp, width // 16 + 1)

    start_x = 0
    start_y = int(height * 0.85)
    block_width = 16
    block_height = 16
    vegetation_positions = []
    right_terrain_start = int(width / 4)

    surface_positions = draw_terrain(screen, tiles, temperature_data, start_x, start_y, block_width, block_height)
    min_y = min([y for _, y in surface_positions])
    for surface_x, surface_y in surface_positions:
        if surface_x >= right_terrain_start:
            if random.random() > 0.7:
                tree_key = random.choice(selected_trees)
                vegetation_positions.append((tree_key, surface_x, surface_y - 126, 1.3))
            else:
                bush_key = random.choice(selected_bushes)
                vegetation_positions.append((bush_key, surface_x, surface_y - 15, 0.7))

    # Jumble up vegetation positions
    random.shuffle(vegetation_positions)

    run = True
    darken = 0
    if cloud_type in ["cloudy", "rainy", "dark_clouds"]:
        darken = 0.4
    while run:
        # screen.fill((0, 0, 0))
        background.draw_sky()

        if 0 < darken <= 1:
            screen_width, screen_height = screen.get_size()
            dark_surface = pygame.Surface((screen_width, screen_height))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(int(darken * 255))
            screen.blit(dark_surface, (0, 0))

        background.draw_mountains()
        draw_terrain(screen, tiles, temperature_data, start_x, start_y, block_width, block_height)
        house.draw_by_key(screen, season, start_x + 21, start_y - (house_data[season][1] * 0.9 - 6), scale_factor=0.9)
        # trees.draw(screen)

        for vegetation_key, x, y, scale in vegetation_positions:
            trees.draw_by_key(screen, vegetation_key, x, y, scale_factor=scale)

        if is_windy:
            leaves.animate_leaves(screen, wind_speed, 70, min_y)

        if weather_effects:
            add_weather(screen, is_windy, wind_speed, weather_type, weather_intensity*1000)

        if is_lightning:
            add_thunder(screen, surface_positions, number_of_strikes_10s)

        add_text(screen, screen_text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/1 - Grassland/Terrain (16 x 16).png"  # Spring
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/2 - Autumn Forest/Terrain (16 x 16).png"  # Fall
    # tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/3 - Tropics/Terrain (16 x 16).png"  # Summer
    tile_path = "tiles/Seasonal Tilesets/Seasonal Tilesets/4 - Winter World/Terrain (16 x 16).png"  # Winter

    # Make sure temp data is in Celsius
    # If is_windy=True, wind_speed should be greater than 3
    # Number_of_strikes_10s = Number of lightning strikes in 10 seconds
    # Weather_intensity = Number of particles * 1000 on the screen
    # Weather_type = rain, light_snow or heavy_snow
    # Pass screen_text as a string, should have the below 3 values
    screen_text = "Temperature: 10°C (50°F)  Wind Speed: 5 kmh (3 mph)  Rain expected"
    screen_init(tile_path, 15, 13, "dark_clouds", "rocky", "Winter",
                False, 40, False, 15, False,
                "rain", 10, screen_text, 1200, 800)
