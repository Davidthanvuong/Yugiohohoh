from .header_pygame import *
from time import time

class DataField(IClickable):
    def __init__(self, size: tff = (200, 30), editable = True, **kwargs):
        self.text = text
        self.editable = editable # Địa chỉ, dãy,... không được phép modify
        self.size = vec(size)
        self.pos = vec(0, 0)
        self.font = pygame.font.Font(None, 24)

    def draw(self, dummy_screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(dummy_screen, colormap['gray'], rect)
        pygame.draw.rect(dummy_screen, (200, 200, 200), rect, 1)  # Light gray border
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        dummy_screen.blit(text_surface, (self.position.x + 5, self.position.y + 5))

    def handle_input(self, e):
        if not self.active:
            return
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_BACKSPACE:
                if e.key == pg.K_LCTRL:
                    self.text = ""
                else:
                    self.text = self.text[:-1]
            elif e.key == pg.K_RETURN:
                self.active = False
            elif e.unicode.isprintable():
                self.text += e.unicode


class DataBox(Component):
    def __init__(self, tf: Transform, com: Component, attr_name: str, comment: str = "Hello, World!"):
        super().__init__(tf=tf)
        self.com = com
        self.value = getattr(com, attr_name)
        self.comment: str = comment
        self.outline_color: tuple[int, int, int] = (100, 100, 100)
        self.hovering: bool = False
        self.clicking: bool = False
        self.hover_start_time: float | None = None
        self.show_hint: bool = False

        # Vector handling
        if isinstance(self.value, vec):
            self.fields: list[DataField] = [
                DataField(str(self.value.x), editable=True),
                DataField(str(self.value.y), editable=True)
            ]
        else:
            self.fields: list[DataField] = [
                DataField(str(self.value), editable=isinstance(self.value, (int, float, str)))
            ]

    def update_render(self):
        #render("databox.png")  # Background via abstraction layer
        for i, field in enumerate(self.fields):
            field.position = vec(self.tf.pos.x + 5 + i * (field.width + 5), self.tf.pos.y + 2)
            field.draw(dummy_screen)

        if self.show_hint and self.comment:
            hint_surface = writer.render(self.comment, True, (255, 255, 255))
            hint_rect = hint_surface.get_rect(topleft=(self.tf.pos.x, self.tf.pos.y - 25))
            pg.draw.rect(dummy_screen, (80, 80, 80), hint_rect.inflate(10, 10))
            dummy_screen.blit(hint_surface, hint_rect.topleft)

    def on_startHover(self):
        self.outline_color = (0, 200, 255)
        self.hover_start_time = time()

    def on_stopHover(self):
        self.outline_color = (100, 100, 100)
        self.hover_start_time = None
        self.show_hint = False

    def on_startClick(self):
        print("Do nothing yet")
        #pass  # Add click behavior if needed

    def on_hovering(self):
        if self.hover_start_time and (time() - self.hover_start_time) >= 1:
            self.show_hint = True


class ToggleHeader(Component):
    def __init__(self, tf: Transform, com: Component):
        super().__init__(tf=tf)
        self.com = com
        self.name = com.__class__.__name__
        self.expanded: bool = True
        self.data_boxes: list[DataBox] = []
        self.generate_data_box()

    def generate_data_box(self):
        y_offset = 35
        for attr, value in self.com.__dict__.items():
            db_tf = Transform(pos=(self.tf.pos.x, self.tf.pos.y + y_offset), hitbox=(300, 25))
            self.data_boxes.append(DataBox(db_tf, self.com, attr, f"Edit {attr}"))
            y_offset += 30

    def update_render(self):
        #render("components.png")  # Header background
        toggle_text = "[-] " if self.expanded else "[+] "
        header_text = toggle_text + self.name
        text_surface = writer.render(header_text, True, (255, 255, 255))
        dummy_screen.blit(text_surface, (self.tf.pos.x + 5, self.tf.pos.y + 5))

        if self.expanded:
            for db in self.data_boxes:
                db.update_render()

    def update_click(self):
        if mouse.host and mouse.clicked:
            self.expanded = not self.expanded
        if self.expanded:
            for db in self.data_boxes:
                db.update_click()

class InspectorFrame:
    def __init__(self, tf: Transform):
        self.headers = [ToggleHeader(tf, com) for com in tf.coms.values()]

# # Example object with attributes
# class ExampleComponent:
#     def __init__(self):
#         self.position = vec(100, 200)  # Vector attribute
#         self.speed = 5  # Scalar attribute

# # Create a Transform and ToggleHeader for the component
# tf = Transform(pos=(50, 50))
# component = ExampleComponent()
# attributes = {"position": component.position, "speed": component.speed}
# header = ToggleHeader(tf, "ExampleComponent", attributes)

# # Main loop (simplified)
# dummy_screen = pygame.display.set_mode((800, 600))
# clock = pygame.time.Clock()
# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     mouse.pos = vec(pygame.mouse.get_pos())
#     mouse.clicked = pygame.mouse.get_pressed()[0]

#     dummy_screen.fill((30, 30, 30))  # Dark background
#     header.click_update()
#     header.render_update()
#     pygame.display.flip()
#     clock.tick(60)