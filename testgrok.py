import pygame as pg
from typing import Optional as No
from pygame import Vector2 as vec


# fonts = pg.font.get_fonts()
# print('\n'.join(fonts))

# exit()

# Initialize pg and set up font
pg.init()
font = pg.font.SysFont("jetbrainsmonoregular", 16)

# Load and scale the icon (replace "path/to/icon.png" with your icon file path)
icon = pg.image.load("assets\\images\\cube.png")  # Update this path
icon = pg.transform.scale(icon, (16, 16))

# DataField class for text fields
class DataField:
    def __init__(self, text, editable=False):
        self.text = text
        self.editable = editable
        self.active = False
        self.position = vec(0, 0)
        self.rect: No[pg.Rect] = None

    def draw(self, screen):
        if self.rect and self.editable:
            pg.draw.rect(screen, (200, 200, 200), self.rect, 1)  # Gray outline
            if self.active:
                screen.fill((50, 50, 50), self.rect)  # Darker background when active
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, self.position)

    def handle_input(self, e):
        if not self.active:
            return
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif e.key == pg.K_RETURN:
                self.active = False
            elif e.unicode.isprintable():
                self.text += e.unicode

# DataBox class for attribute display
class DataBox:
    def __init__(self, obj, attr, icon):
        self.obj = obj
        self.attr = attr
        self.icon = icon
        self.name_field = DataField(attr)
        self.value = getattr(obj, attr)
        if isinstance(self.value, (int, float, str)):
            self.value_field = DataField(str(self.value), editable=True)
        else:
            self.value_field = DataField(str(self.value), editable=False)
        self.position = vec(0, 0)

    def draw(self, screen):
        # Set positions
        self.name_field.position = self.position + vec(20, 0)
        self.value_field.position = self.position + vec(150, 0)
        # Set rect for value_field if editable
        if self.value_field.editable:
            self.value_field.rect = pg.Rect(self.value_field.position, (100, 20))
        else:
            self.value_field.rect = None
        # Draw box
        box_rect = pg.Rect(self.position[0], self.position[1], 250, 20)
        pg.draw.rect(screen, (100, 100, 100), box_rect, 1)
        # Draw icon
        screen.blit(self.icon, (self.position[0] + 2, self.position[1] + 2))
        # Draw fields
        self.name_field.draw(screen)
        self.value_field.draw(screen)

    def update_value(self):
        if self.value_field.editable:
            try:
                new_value = type(self.value)(self.value_field.text)
                setattr(self.obj, self.attr, new_value)
            except ValueError:
                print(f"Invalid value for {self.attr}: {self.value_field.text}")

# ToggleHeader class for collapsible sections
class ToggleHeader:
    def __init__(self, text, sub_items):
        self.text = text
        self.sub_items = sub_items
        self.expanded = True
        self.position = (0, 0)
        self.rect = None

    def draw(self, screen):
        toggle_text = "[-]" if self.expanded else "[+]"
        toggle_surface = font.render(toggle_text, True, (255, 255, 255))
        screen.blit(toggle_surface, (self.position[0], self.position[1]))
        header_surface = font.render(self.text, True, (255, 255, 255))
        header_pos = self.position + vec(1, 0) * 35 #(self.position[0] + 20, self.position[1])
        screen.blit(header_surface, header_pos)
        # Set rect
        header_width = 20 + header_surface.get_width()
        self.rect = pg.Rect(self.position[0], self.position[1], header_width, 20)

    def toggle(self):
        self.expanded = not self.expanded

# Function to create hierarchical items
def create_items(obj, icon):
    items = []
    for attr, value in obj.__dict__.items():
        if isinstance(value, list):
            sub_items = []
            for i, item in enumerate(value):
                if hasattr(item, '__dict__'):
                    header_text = f"{attr}[{i}]: {item.__class__.__name__}"
                    item_sub_items = create_items(item, icon)
                    header = ToggleHeader(header_text, item_sub_items)
                    sub_items.append(header)
            if sub_items:
                items.extend(sub_items)
        else:
            data_box = DataBox(obj, attr, icon)
            items.append(data_box)
    return items

# Function to draw items recursively
def draw_items(items, screen, x, y, indent=0, editable_fields=[], toggle_headers=[]):
    for item in items:
        item.position = (x + indent, y)
        if isinstance(item, DataBox):
            item.draw(screen)
            if item.value_field.editable:
                editable_fields.append((item.value_field.rect, item, item.value_field))
            y += 20
        elif isinstance(item, ToggleHeader):
            item.draw(screen)
            toggle_headers.append((item.rect, item))
            if item.expanded:
                y = draw_items(item.sub_items, screen, x, y + 20, indent + 20, editable_fields, toggle_headers)
            else:
                y += 20
    return y

# Example classes for testing
class Transform:
    def __init__(self):
        self.x = 100
        self.y = 200

class Hitbox:
    def __init__(self):
        self.width = 50
        self.height = 30

class GameObject:
    def __init__(self):
        self.name = "Player"
        self.health = 100
        self.components = [Transform(), Hitbox()]

# Main program
screen = pg.display.set_mode((600, 400))
pg.display.set_caption("Object Inspector")
clock = pg.time.Clock()

obj = GameObject()
items = create_items(obj, icon)

running = True
active_item = None
editable_fields = []
toggle_headers = []

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            click_pos = event.pos
            for rect, toggle_header in toggle_headers:
                if rect.collidepoint(click_pos):
                    toggle_header.toggle()
                    break   
            else:
                for rect, data_box, value_field in editable_fields:
                    if rect.collidepoint(click_pos):
                        if active_item:
                            active_item[1].active = False
                        active_item = (data_box, value_field)
                        value_field.active = True
                        break
                else:
                    if active_item:
                        active_item[1].active = False
                        active_item = None
        elif event.type == pg.KEYDOWN:
            if active_item:
                active_item[1].handle_input(event)
            if event.key == pg.K_TAB:
                if editable_fields:
                    if active_item:
                        try:
                            index = [field[2] for field in editable_fields].index(active_item[1])
                            next_index = (index + 1) % len(editable_fields)
                        except ValueError:
                            next_index = 0
                    else:
                        next_index = 0
                    if active_item:
                        active_item[1].active = False
                    next_item = editable_fields[next_index]
                    active_item = (next_item[1], next_item[2])
                    active_item[1].active = True
    # Update value if editing is committed
    if active_item and not active_item[1].active:
        active_item[0].update_value()
        active_item = None

    # Draw everything
    screen.fill((0, 0, 0))
    draw_items(items, screen, 10, 10, 0, editable_fields, toggle_headers)
    pg.display.flip()

    for attr, data in obj.__dict__.items():
        if isinstance(data, list):
            print(f"~~~ {attr} ~~~")
            for i in data:
                if hasattr(i, '__dict__'):
                    for attr2, data2 in i.__dict__.items():
                        print(f"    {attr2}: {data2}")
        else:
            print(f"{attr}: {data}")
    clock.tick(10)

pg.quit()