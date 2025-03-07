import pygame as pg
import sys

# Khởi tạo Pygame
pg.init()

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 250, 0)

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Lớp HealthBar để quản lý thanh máu
class HealthBar:
    def __init__(self, screen, x, y, initial_width, max_width):
        self.screen = screen
        self.x = x
        self.y = y
        self.max_width = max_width
        # Tải ảnh thanh máu
        self.health_bar_image = pg.image.load('assets/images/hp.png')
        self.health_bar_rect = self.health_bar_image.get_rect(topleft=(x, y))
        # Offset cho thanh máu xanh
        self.offset_x = 267
        self.offset_y = 200
        self.health_rect = pg.Rect(
            self.health_bar_rect.x + self.offset_x,
            self.health_bar_rect.y + self.offset_y,
            initial_width,
            11  # Chiều cao cố định
        )
        self.dragging = False

    def handle_event(self, event):
        """kéo thả thanh máu"""
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (self.health_rect.right - 10 <= mouse_x <= self.health_rect.right + 10 and
                self.health_rect.top <= mouse_y <= self.health_rect.bottom):
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            new_width = mouse_x - self.health_rect.left
            new_width = max(0, min(new_width, self.max_width))
            self.health_rect.width = new_width

    def draw(self):
        self.screen.blit(self.health_bar_image, self.health_bar_rect)
        pg.draw.rect(self.screen, GREEN, self.health_rect)

    def is_depleted(self):
        return self.health_rect.width <= 0

class Character:
    def __init__(self, screen, x, y, image_path, scale_factor=0.25):
        self.screen = screen
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(
            self.image,
            (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor))
        )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dying = False
        self.dying_progress = 0
        self.show_died_message = False
        self.font = pg.font.Font(None, 36)

    def start_dying(self):
        self.is_dying = True
        self.dying_progress = 0

    def update(self):
        if self.is_dying:
            self.rect.y += 10 
            self.dying_progress += 1
            if self.dying_progress >= 60:
                self.is_dying = False
                self.show_died_message = True

    def draw(self):
        """Vẽ nhân vật hoặc thông báo chết"""
        if self.show_died_message:
            died_text = self.font.render("DIED EZ NOOB NIGGA", True, (255, 0, 0))
            self.screen.blit(died_text, (WIDTH // 2 - died_text.get_width() // 2,
                                         HEIGHT // 2 - died_text.get_height() // 2))
        else:
            if self.is_dying:
                angle = self.dying_progress * 6
                rotated_image = pg.transform.rotate(self.image, angle)
                rotated_rect = rotated_image.get_rect(center=self.rect.center)
                self.screen.blit(rotated_image, rotated_rect)
            else:
                self.screen.blit(self.image, self.rect)

health_bar = HealthBar(screen, 100, 100, 106, 106)  # Thanh máu bắt đầu với chiều rộng 106
character = Character(
    screen,
    health_bar.health_bar_rect.x + 268,
    health_bar.health_bar_rect.y + 215,
    'assets/images/notsafecard/Akeno.jpg'
)

running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        health_bar.handle_event(event)

    if health_bar.is_depleted() and not character.is_dying and not character.show_died_message:
        character.start_dying()

    character.update()

    screen.fill(WHITE)
    health_bar.draw()
    character.draw()

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()