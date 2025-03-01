from .header_pygame import *
from typing import TypeVar, cast
from random import randint as rint
import pickle, os
from copy import deepcopy

T = TypeVar("T", bound="Component")

class Transform:
    '''Class quốc dân'''
    storage: dict[str, 'Transform'] = {}

    def __init__(self, name: str = "", pos: tff = CENTER, rot = 0.0, scale: tff = ONE, pivot: tff = HALF, enable = True,
                 hitbox: tff = ZERO, parent: No['Transform'] = None, simple = False):
        self.name = name if name != "" else f"Object {rint(0, 2**60)}"
        self.pos = vec(pos)
        self.rot = rot
        self.scale = vec(scale)
        self.pivot = vec(pivot)
        self.parent = parent
        self.hitbox = vec(hitbox)
        if parent: parent.own(self)
        
        self.childrens: list['Transform'] = []
        self.coms: dict[type['Component'], 'Component'] = {}

        self.simple = simple
        self.enable = enable

        self.global_pos = vec(pos)
        self.global_rot = rot
        self.global_scale = vec(scale)


    def update_logic(self):
        if not self.enable: return
        for com in self.coms.values():
            com.update_logic()
        self.update_global()

        for child in self.childrens:
            child.update_logic()


    def update_click(self): # Click update / Hitbox update trên cùng trước
        if not self.enable: return
        for com in reversed(self.coms.values()):
            com.update_click()

        for child in reversed(self.childrens):
            child.update_click()


    def update_render(self):
        if not self.enable: return
        for com in self.coms.values():
            com.update_render()

        for child in self.childrens:
            child.update_render()


    def update_global(self):
        '''Cập nhật tính chất global của vật (chỉ chạy mỗi frame)'''
        if not self.parent:
            self.global_pos = self.pos
            if not self.simple:
                self.global_rot = self.rot
                self.global_scale = self.scale
        elif self.simple:
            self.global_pos = self.pos + self.parent.global_pos
            print("Children", self.parent.global_pos)
        else:
            self.global_rot = self.rot + self.parent.global_rot
            self.global_scale = self.scale.elementwise() * self.parent.global_scale

            rel = (self.pos.elementwise() * self.parent.global_scale).rotate_rad(self.parent.global_rot)
            self.global_pos = self.parent.global_pos + rel

    
    def get(self, com: type[T]) -> T:
        return cast(T, self.coms[com])
    

    def try_get(self, com: type[T]) -> T | None:
        t = self.coms.get(com)
        return cast(T, t) if t else None
    

    def own(self, tf: 'Transform'):
        self.childrens.append(tf)

    
    def required(self, com: type[T]) -> 'Component | None':
        if not self.coms.get(com):
            return com(attach=self)
        return None
    

    @staticmethod
    def exist_prefab(name: str, store = True) -> bool:
        if store and Transform.storage.get(name):
            return True
 
        path = f"assets\\prefabs\\{name}"
        return os.path.exists(path)
    

    @staticmethod
    def prefab(name: str, parent: No['Transform'] = None, store = True) -> 'Transform':
        if store:
            obj = Transform.storage.get(name)
            if obj: 
                deep = deepcopy(obj)
                if parent: parent.own(deep)
                return deep
 
        path = f"assets\\prefabs\\{name}"
        if os.path.exists(path):
            with open(path, "rb") as f: # Không đủ lặp lại để tạo hàm mới rút gọn
                obj = pickle.load(f)
                if store: Transform.storage[name] = obj
                deep = deepcopy(obj)
                if parent: parent.own(deep)
                return deep
        raise Exception(f"Did not find {path}")


    def save(self, name: str = ""):
        path = f"assets\\prefabs\\{name if name != '' else self.name}"
        self.parent = None
        
        os.makedirs("assets\\prefabs\\", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        
        print(f"Saved {path}")



class Component:
    '''Class để chạy các chức năng từ vật (Transform)'''

    def __init__(self, attach: Transform):
        self.tf = attach
        attach.coms[self.__class__.mro()[0]] = self
        # Component được gán theo tên trên cùng

    def update_logic(self): pass
    def update_click(self): pass
    def update_render(self): pass