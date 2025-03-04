from .header_pygame import *

class TransfField(IClickable):
    # Class variable to track the currently dragged item
    dragging = None

    def __init__(self, target: Transform, bind: 'Hierarchy', indent_level: int = 0, **kwargs):
        # Initialize IClickable with draggable enabled
        super().__init__(draggable=True, **kwargs)
        self.target = target
        self.bind = bind
        self.indent_level = indent_level
        self.children_fields = []  # List to store child TransfField instances
        self.is_dragging = False
        self.preview_line = bind.preview_line # Image for drag preview

        # Visual components
        self.com_image = self.tf.get(Image)
        self.com_text = self.tf.get(Text)
        # self.com_image = Image(
        #     attach=self.target,
        #     path="white.png",
        #     size=(100, 22),
        #     standalone=True
        # )
        # self.com_text = Text(
        #     attach=self.target,
        #     text=target.name,
        #     color=colormap['dark']
        # )

        # Apply indentation based on hierarchy level (20 pixels per level)
        indent_offset = self.indent_level * 20
        self.target.pos.x += indent_offset
        self.target.hitbox.x += indent_offset

        # Recursively create TransfField for each child
        for child in target.childrens:
            child_field = TransfField(child, self.bind, indent_level + 1, attach=self.target)
            self.children_fields.append(child_field)

    def update_logic(self):
        """Update the position of the field if it's being dragged."""
        super().update_logic()
        if self.is_dragging:
            # Follow the mouse position
            self.target.pos = MOUSE.pos
            # Update preview line position (simplified to just above the item)
            if self.preview_line:
                self.preview_line.pos = MOUSE.pos - (0, 10)

    def on_startHover(self):
        """Highlight the field when hovered."""
        self.com_image.changed = True
        self.com_image.cache.native.fill(colormap['light'])

    def on_stopHover(self):
        """Reset highlight when not hovered, unless dragging."""
        if not self.is_dragging:
            self.com_image.changed = True
            self.com_image.cache.native.fill(colormap['white'])

    def on_startClick(self):
        """Begin dragging the field."""
        if self.draggable:
            TransfField.dragging = self
            self.is_dragging = True
            self.preview_line.enable = True
            # Detach from parent temporarily
            if self.target.parent:
                self.target.parent.childrens.remove(self.target)
            # Create a preview line to show where it will be placed
            #self.preview_line
            # Width matches the field, height is 2 for a bold line
            #self.preview_line.pos = self.target.pos - (0, 10)

    def on_stopClick(self):
        """Finish dragging and reattach the field to a new parent."""
        if self.is_dragging:
            self.is_dragging = False
            self.preview_line.enable = False
            TransfField.dragging = None
            # Find the TransfField under the mouse to become the new parent
            for f in self.bind.tf.childrens:  # Assume a global list of all TransfFields
                # todo: Abstraction cho hitbox và collidepoint (simple dùng trong trường hợp này vẫn ok)
                if f != self and f.collidepoint(MOUSE.pos):
                    f.own(self.target)
                    break
            # If no parent is found, it could remain detached or attach to a root (logic TBD)
            # Remove the preview line
            if self.preview_line:
                self.preview_line.enable = False  # No. Assuming a destroy method exists

    def on_stopFocus(self):
        """Reset appearance when focus is lost."""
        self.com_image.changed = True
        self.com_image.cache.native.fill(colormap['white'])


class Hierarchy(FlexibleMenu):
    '''name'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preview_line = Transform() #Image(
        #     path="white.png",
        #     size=(100, 5),  # Width matches the field, height is 2 for a bold line
        #     standalone=True
        # )
        self.preview_line.enable = False