# from .header_objects import *
# from typing import TypeVar, Union, cast
# from dataclasses import dataclass
# from random import randint as rint

# T = TypeVar("T", bound="Component")




# #@assetclass
# class Transform:
#     '''Phiên bản nhẹ kí của Transform'''

#     # Info của chuột, xóa khi gặp 1 vật tương tác đc

#     def __init__(self, name: str = "", pos: tff = CENTER, rot = 0.0, scale: tff = ONE, pivot: tff = HALF, 
#                  hitbox: tff = (64, 64), parent: No['Transform'] = None, simple = False, enable = True):
#         print(pos, scale)
#         self.name = name if name != "" else f"Object {rint(0, 2**60)}"
#         self.pos = vec(pos)
#         self.rot = rot
#         self.scale = vec(scale)
#         self.pivot = vec(pivot)
#         self.parent = parent
#         self.hitbox = vec(hitbox)
#         self.coms: dict[type['Component'], 'Component'] = {}
#         self.mark_as_simple = simple
#         self.enable = enable

#     def get(self, com: type[T]) -> T:
#         return cast(T, self.coms[com])

#     def logic_update(self):
#         '''Hàm để chạy các components'''

#     def click_update(self):
#         for com in self.coms.values():
#             com.click_update()

#     def render_update(self):
#         for com in self.coms.values():
#             com.render_update()


# class Component:
#     '''Class để chạy các chức năng từ vật (Translite)'''

#     def __init__(self, tf: Transform):
#         self.tf = tf
#         tf.coms[self.__class__.mro()[0]] = self
#         #for base in reversed(self.__class__.mro())

#     @abstractmethod
#     def logic_update(self): pass

#     @abstractmethod
#     def click_update(self): pass

#     @abstractmethod
#     def render_update(self): pass


# class IClickable(Component):
#     '''Click'''
#     def __init__(self, clickable=True, draggable=False, **kwargs):
#         super().__init__(**kwargs)

#         self.clickable = clickable
#         self.draggable = draggable # Cho phép kéo thả
#         self.hovering = False
#         self.clicking = False

#     def try_getMouse(self):
#         '''Thử lấy chuột trong hitbox'''
#         if mouse.host and mouse.host is not self:
#             return False
    
#         box = self.tf.hitbox.elementwise() * self.tf.scale
#         a = box.elementwise() * -self.tf.pivot
#         b = a + box
#         rel = mouse.pos - self.tf.pos
#         if not self.tf.mark_as_simple:
#             rel.rotate_ip(-self.tf.rot)

#         return (a.x <= rel.x <= b.x) and \
#                (a.y <= rel.y <= b.y)

#     def click_update(self):
#         if self.try_getMouse():
#             if not self.hovering:
#                 mouse.host = self # Đánh dấu vật đã dùng chuột
#                 self.on_startHover()
#                 self.hovering = True
            
#             if not self.clickable:
#                 return
#             if mouse.clicked:
#                 if not self.clicking:
#                     self.on_startClick()
#                     self.clicking = True
#                 self.on_clicking()
#             elif self.clicking:
#                 self.on_stopClick()
#                 self.clicking = False

#             self.on_hovering()
#         elif self.hovering:
#             self.on_stopHover()
#             mouse.host = None
#             self.hovering = False

#     @abstractmethod
#     def render_update(self): pass

#     # Hàm rỗng nhưng không abstract để cho inheritance
#     def logic_update(self): pass
#     def on_startHover(self): pass
#     def on_startClick(self): pass
#     def on_stopHover(self): pass
#     def on_stopClick(self): pass
#     def on_hovering(self): pass
#     def on_clicking(self): pass