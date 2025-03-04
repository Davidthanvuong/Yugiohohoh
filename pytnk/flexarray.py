from .header_pygame import *

class FlexArray(IClickable):
    '''Bạn ghét canh giữa mọi thứ, chỉnh thủ công từng vị trí một ư? Đừng lo đã có FlexArray'''

    def __init__(self, axis='y', space=2, activeFit=1.2, use_relativeFit=True, 
                 interactable=True, foldable=False, reorderable=False, use_crowding=False, 
                 includeSelf=False, **kwargs):
        super().__init__(hoverable=interactable, clickable=foldable, draggable=reorderable, **kwargs)
        self.axis = axis
        self.space = space
        self.interactable = interactable
        self.foldable = foldable
        self.reorderable = reorderable
        self.activeFit = activeFit              # Khi chọn một vật, đẩy ra bao xa so với các items khác
        self.use_relativeFit = use_relativeFit  # Kích thước tương đối theo size vật
        self.use_crowding = use_crowding        # Thay vì scroll, đè tỉ lệ với nhau
        self.includeSelf = includeSelf          # Tham gia vào flexArray
        self.active_id = -1
        self.folding = False
        self.cache: dict[int, tuple[Transform, float]] = {}
        self.flexOffset = vec(0, 0)
        self.renderOffset = vec(0, 0)


    # def update_logic(self):
    #     rawv = 0
    #     for i, tf in enumerate(self.tf.childrens):
    #         flex = tf.tryComponent(FlexArray)
    #         target = flex.renderOffset if flex else tf.hitbox
    #         if tf.enabled:
    #             dist = getattr(target, self.axis)
    #         else: dist = 0
    #         if self.active_id == i: # TODO: Animation later
    #             dist *= self.activeFit

    #         self.cache[i] = (tf, dist)

    #         if tf.enabled:
    #             rawv += dist

    #     box = getattr(self.tf.hitbox, self.axis)
    #     if self.use_crowding and rawv > 0:
    #         ratio = box / rawv
    #     else:
    #         ratio = 1  # Tỉ lệ chật
 
    #     v = box if self.includeSelf else 0
    #     for tf in self.cache.values(): # Cứ duyệt theo cache
    #         setattr(tf[0].pos, self.axis, v)

    #         v += tf[1] * ratio
    #         v += self.space if tf[1] != 0 else 0

    #     setattr(self.flexOffset, self.axis, v)
    #     setattr(self.renderOffset, self.axis, box if self.folding else v - self.space)
    #     #print(self.tf.name, self.tf.pos, self.tf.hitbox)

    def update_logic(self):
        # Define the perpendicular axis for size calculations
        perp_axis = 'y' if self.axis == 'x' else 'x'
        rawv = 0  # Total length along the layout axis (unscaled)
        max_perp = 0  # Maximum size along the perpendicular axis

        # Step 1: Cache child data and calculate total length and max perpendicular size
        self.cache.clear()
        for i, tf in enumerate(self.tf.childrens):
            flex = tf.tryComponent(FlexArray)
            target = flex.renderOffset if flex else tf.hitbox
            if tf.enabled:
                length = getattr(target, self.axis)  # Size along the layout axis
                perp_size = getattr(target, perp_axis)  # Size along the perpendicular axis
                if perp_size > max_perp:
                    max_perp = perp_size
            else:
                length = 0
            if self.active_id == i:  # Scale length for the active item
                length *= self.activeFit
            self.cache[i] = (tf, length)
            if tf.enabled:
                rawv += length + (self.space if i < len(self.tf.childrens) - 1 else 0)  # Include space except after last item

        # Step 2: Determine scaling ratio based on hitbox and crowding
        box = getattr(self.tf.hitbox, self.axis)
        if self.use_crowding and rawv > box > 0:
            ratio = box / rawv  # Scale down to fit within hitbox
        else:
            ratio = 1.0  # No scaling if not crowding or no overflow

        # Step 3: Position children along the layout axis and calculate scaled size
        v = box if self.includeSelf else 0  # Starting position
        total_scaled_size = v  # Track total size including scaled spacing
        for i, (tf, length) in enumerate(self.cache.values()):
            setattr(tf.pos, self.axis, v)
            scaled_length = length * ratio
            v += scaled_length
            if tf.enabled and length != 0 and i < len(self.cache) - 1:  # Add space except after last item
                scaled_space = self.space * ratio
                v += scaled_space
                total_scaled_size = v  # Update total size with position + space
            else:
                total_scaled_size = v  # Update total size without extra space

        # Step 4: Update flexOffset and renderOffset
        if self.folding:
            # When folding, limit renderOffset to the hitbox size
            self.renderOffset.x = self.tf.hitbox.x
            self.renderOffset.y = self.tf.hitbox.y
            setattr(self.flexOffset, self.axis, box)
        else:
            # When not folding, set offsets to the content size, respecting crowding
            setattr(self.flexOffset, self.axis, total_scaled_size)
            self.renderOffset.x = total_scaled_size if self.axis == 'x' else max_perp
            self.renderOffset.y = total_scaled_size if self.axis == 'y' else max_perp


    def on_startClick(self):
        print("CLICKLED")
        self.folding = not self.folding
        for ch in self.tf.childrens:
            ch.enabled = not self.folding


    def take_a_seat(self, tf: Transform, pos: vec):
        '''Bình tĩnh, thả nó cái vị trí, nó tự insert vô đứa thứ mấy trong parent'''
        pass