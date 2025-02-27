import pygame

pygame.init()

# Create a resizable window
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen to the new size
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            print("New screen size:", screen.get_size())

pygame.quit()
