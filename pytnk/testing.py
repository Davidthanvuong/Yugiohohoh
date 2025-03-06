import pygame
import sys
import time
import math

# Initialize Pygame
pygame.init()

# Define base dimensions and aspect ratio
base_width, base_height = 800, 500
aspect_ratio = base_width / base_height  # 1.6:1

# Create a resizable window with initial size 800x500
screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Pygame Window with Stats")

# Load the image
image = pygame.image.load("assets\\images\\card_empty.png").convert_alpha()
image_rect = image.get_rect()

# Define grid system: 12 units wide
grid_units_x = 12
grid_units_y = grid_units_x / aspect_ratio  # ~7.5 units tall

# Font for displaying stats
font = pygame.font.Font(None, 36)

# Variables for FPS calculation
prev_time = time.time()
frame_count = 0
fps = 0

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Get current window size
    screen_width, screen_height = screen.get_size()
    screen_aspect = screen_width / screen_height

    # Calculate the effective rendering area (letterboxed if needed)
    if screen_aspect > aspect_ratio:
        render_width = int(screen_height * aspect_ratio)
        render_height = screen_height
        offset_x = (screen_width - render_width) // 2
        offset_y = 0
    else:
        render_width = screen_width
        render_height = int(screen_width / aspect_ratio)
        offset_x = 0
        offset_y = (screen_height - render_height) // 2

    # Create a surface for the rendering area
    render_surface = pygame.Surface((render_width, render_height))

    # Calculate grid unit size based on render area
    unit_size = render_width / grid_units_x

    # Scale the image relative to the grid (2x3 grid units)
    image_grid_width, image_grid_height = 2, 3
    scaled_width = int(image_grid_width * unit_size)
    scaled_height = int(image_grid_height * unit_size)
    scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

    # Position the image on the grid (at 5, 2)
    grid_x, grid_y = 5, 2
    image_x = int(grid_x * unit_size)
    image_y = int(grid_y * unit_size)

    # Fill render surface with a background color
    render_surface.fill((100, 100, 100))

    # Draw the scaled image on the render surface
    offset = (math.cos(time.time() * 20) - 0.5) * 200
    render_surface.blit(scaled_image, (image_x + offset, image_y))

    # Fill the screen with black for letterboxing
    screen.fill((0, 0, 0))

    # Blit the render surface onto the screen
    screen.blit(render_surface, (offset_x, offset_y))

    # Calculate FPS
    frame_count += 1
    current_time = time.time()
    if current_time - prev_time >= 0.2:  # Update every second
        fps = frame_count / (current_time - prev_time)
        frame_count = 0
        prev_time = current_time

    # Calculate render scale (relative to 800x500)
    render_scale = render_width / base_width  # Since height follows aspect ratio

    # Render stats text
    fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    window_res_text = font.render(f"Window: {screen_width}x{screen_height}", True, (255, 255, 255))
    border_res_text = font.render(f"Border: {render_width}x{render_height}", True, (255, 255, 255))
    scale_text = font.render(f"Scale: {render_scale:.2f}x", True, (255, 255, 255))

    # Draw stats on the screen (top-left corner)
    screen.blit(fps_text, (10, 10))
    screen.blit(window_res_text, (10, 50))
    screen.blit(border_res_text, (10, 90))
    screen.blit(scale_text, (10, 130))

    # Update the display
    pygame.display.flip()

    # Removed pygame.time.Clock().tick(60) for uncapped FPS