import pygame
import math

class RotatingSprite(pygame.sprite.Sprite):
    def __init__(self, images, pos, speed=2):
        super().__init__()
        self.original_images = images  # Store original images for rotation
        self.image_index = 0
        self.image = self.original_images[self.image_index]
        self.rect = self.image.get_rect(center=pos)
        
        self.angle = 0  # Rotation angle
        self.speed = speed  # Movement speed
        
        # Hitbox using mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.copy()  

    def rotate(self, angle):
        """Rotates sprite by given angle."""
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_images[self.image_index], -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Update hitbox
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.copy()

    def move(self, direction):
        """Moves sprite in given direction (angle in degrees)."""
        rad = math.radians(self.angle + direction)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y += self.speed * math.sin(rad)
        self.hitbox.center = self.rect.center  # Sync hitbox with rect

    def animate(self):
        """Handles sprite animation."""
        self.image_index = (self.image_index + 1) % len(self.original_images)
        self.image = pygame.transform.rotate(self.original_images[self.image_index], -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Updates sprite every frame."""
        self.animate()



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load animated frames
frames = [pygame.image.load(f"sprite_{i}.png") for i in range(4)]
player = RotatingSprite(frames, (400, 300))
all_sprites = pygame.sprite.Group(player)

running = True
while running:
    screen.fill((30, 30, 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rotate(5)
    if keys[pygame.K_RIGHT]:
        player.rotate(-5)
    if keys[pygame.K_UP]:
        player.move(0)

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
