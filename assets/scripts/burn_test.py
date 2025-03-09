import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 200, 300
FPS = 60
SIMULATION_TRIM = 2  # 2 means 2x2 pixels per simulation pixel

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Optimized Shader Burning Card")
clock = pygame.time.Clock()

class Shader_BurningCard:
    def __init__(self, image_path, crisp_points=10, initial_burn_groups=50, burn_speed=0.015,
                 fire_color=(255, 165, 0), fire_alpha=128, simulation_trim=SIMULATION_TRIM):
        """Initialize the burning card shader with optimized simulation."""
        # Load and scale the card image
        self.original_surf = pygame.image.load(image_path).convert_alpha()
        if self.original_surf.get_size() != (WIDTH, HEIGHT):
            self.original_surf = pygame.transform.scale(self.original_surf, (WIDTH, HEIGHT))
        
        # Parameters
        self.crisp_points = crisp_points
        self.initial_burn_groups = initial_burn_groups
        self.burn_speed = burn_speed
        self.fire_color = fire_color
        self.fire_alpha = fire_alpha
        self.simulation_trim = simulation_trim
        
        # Trimmed dimensions
        self.trim_width = WIDTH // simulation_trim
        self.trim_height = HEIGHT // simulation_trim
        
        # Burning state: 0 (unburnt) to 1 (fully burnt)
        self.burning_state = np.zeros((self.trim_height, self.trim_width), dtype=np.float32)
        
        # Crisp matrix: Controls burn speed variation
        self.crisp_matrix = self._generate_crisp_matrix()
        
        # Initialize burning pixels once
        self._init_burning_pixels()

    def _generate_crisp_matrix(self):
        """Generate a crisp matrix at trimmed resolution for burn variation."""
        # Random points for crispness variation
        points = [(random.randint(0, self.trim_width-1), random.randint(0, self.trim_height-1)) 
                  for _ in range(self.crisp_points)]
        crisp_matrix = np.zeros((self.trim_height, self.trim_width), dtype=np.float32)
        
        # Calculate distance to nearest point for each pixel
        for y in range(self.trim_height):
            for x in range(self.trim_width):
                min_dist = float('inf')
                for px, py in points:
                    dist = np.sqrt((x - px) ** 2 + (y - py) ** 2)
                    min_dist = min(min_dist, dist)
                crisp_matrix[y, x] = min_dist
        
        # Normalize to 0-1
        max_dist = crisp_matrix.max()
        if max_dist > 0:
            crisp_matrix /= max_dist
        return crisp_matrix

    def _init_burning_pixels(self):
        """Set initial burning patches at trimmed resolution using random only here."""
        for _ in range(self.initial_burn_groups):
            x, y = random.randint(0, self.trim_width-1), random.randint(0, self.trim_height-1)
            self.burning_state[y, x] = 0.01  # Start with a small burn value

    def update(self):
        """Update the burning state linearly at trimmed resolution."""
        # Create a mask of currently burning pixels
        burning_mask = self.burning_state > 0
        # Increase burning progress based on crispness
        self.burning_state[burning_mask] += self.burn_speed * (1 - self.crisp_matrix[burning_mask] * 0.5)
        # Cap burning state at 1
        self.burning_state[self.burning_state > 1] = 1
        
        # Spread burn to adjacent unburnt pixels
        new_burning = np.zeros_like(self.burning_state, dtype=bool)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        
        for dy, dx in directions:
            # Shift the burning mask in each direction
            shifted_y = slice(max(0, dy), self.trim_height + min(0, dy)) if dy != 0 else slice(None)
            shifted_x = slice(max(0, dx), self.trim_width + min(0, dx)) if dx != 0 else slice(None)
            orig_y = slice(max(0, -dy), self.trim_height + min(0, -dy)) if dy != 0 else slice(None)
            orig_x = slice(max(0, -dx), self.trim_width + min(0, -dx)) if dx != 0 else slice(None)
            
            # Pixels that are unburnt but have a burning neighbor
            new_burning[shifted_y, shifted_x] |= (self.burning_state[orig_y, orig_x] > 0) & (self.burning_state[shifted_y, shifted_x] == 0)
        
        # Start new burning pixels
        self.burning_state[new_burning] = 0.01

    def render(self):
        """Render the card and fire effects at full resolution."""
        # Upscale burning state to full resolution
        full_burning_state = np.repeat(np.repeat(self.burning_state, self.simulation_trim, axis=0), 
                                      self.simulation_trim, axis=1)
        
        # Create surfaces
        card_surf = self.original_surf.copy()
        pixels = pygame.surfarray.pixels3d(card_surf)
        alpha = pygame.surfarray.pixels_alpha(card_surf)
        original_pixels = pygame.surfarray.pixels3d(self.original_surf)
        
        fire_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fire_pixels = pygame.surfarray.pixels3d(fire_surf)
        fire_alpha = pygame.surfarray.pixels_alpha(fire_surf)
        
        # Apply burning effect
        for y in range(HEIGHT):
            for x in range(WIDTH):
                t = full_burning_state[y, x]
                if t > 0:
                    if t <= 0.6:
                        # Fade to black
                        s = t / 0.6
                        pixels[x, y] = [int(original_pixels[x, y, c] * (1 - s)) for c in range(3)]
                        alpha[x, y] = 255
                    else:
                        # Fade to transparent
                        s = (t - 0.6) / 0.4
                        pixels[x, y] = [0, 0, 0]
                        alpha[x, y] = int(255 * (1 - s))
                
                # Add fire at burning front
                trim_x, trim_y = x // self.simulation_trim, y // self.simulation_trim
                if (self.burning_state[trim_y, trim_x] > 0 and
                    any(self.burning_state[ny, nx] == 0 for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]
                        if 0 <= (ny := trim_y + dy) < self.trim_height and 0 <= (nx := trim_x + dx) < self.trim_width)):
                    fire_pixels[x, y] = self.fire_color
                    fire_alpha[x, y] = self.fire_alpha
        
        return card_surf, fire_surf

# Create shader instance
shader = Shader_BurningCard(
    image_path="assets\\images\\card_empty.png",
    crisp_points=10,
    initial_burn_groups=50,
    burn_speed=0.015,
    fire_color=(255, 165, 0),
    fire_alpha=128,
    simulation_trim=SIMULATION_TRIM
)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and render
    shader.update()
    card_surf, fire_surf = shader.render()

    # Draw
    screen.fill((0, 0, 0))
    screen.blit(card_surf, (0, 0))
    screen.blit(fire_surf, (0, 0))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()