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


    def get(self, com: type[T]) -> T:
        return cast(T, self.coms[com])
    

    def own(self, tf: 'Transform'):
        self.childrens.append(tf)


    def logic_update(self):
        if not self.enable: return
        for com in self.coms.values():
            com.logic_update()
        self.update_global()

        for child in self.childrens:
            child.logic_update()


    def click_update(self): # Click update / Hitbox update trên cùng trước
        if not self.enable: return
        for com in reversed(self.coms.values()):
            com.click_update()

        for child in reversed(self.childrens):
            child.click_update()


    def render_update(self):
        if not self.enable: return
        for com in self.coms.values():
            com.render_update()

        for child in self.childrens:
            child.render_update()


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


    @staticmethod
    def exist_prefab(name: str, store = True) -> bool:
        if store and Transform.storage.get(name):
            return True
 
        path = f"assets\\prefabs\\{name}"
        return os.path.exists(path)
    

    @staticmethod
    def prefab(name: str, store = True) -> 'Transform':
        if store:
            obj = Transform.storage.get(name)
            if obj: return deepcopy(obj)
 
        path = f"assets\\prefabs\\{name}"
        if os.path.exists(path):
            with open(path, "rb") as f:
                obj = pickle.load(f)
                if store: Transform.storage[name] = obj
                return deepcopy(obj)
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

    def logic_update(self): pass
    def click_update(self): pass
    def render_update(self): pass