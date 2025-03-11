import pickle, os
from typing import Type, cast
from copy import deepcopy
from .engine import *

TCom = TypeVar("TCom", bound="Component")


class Component:
    # e_notStarted: Event['Component'] = Event()

    def _binding(self, go: 'GameObject'):
        self.go = go
        if not isinstance(self, Transform): # Tự nó reference chính nó :skull_emoji:
            self.transf = go.transf
        self.enabled = True

        # Tránh chạy lúc edit
        if App.gameStarted: self.start()
        # else: Component.e_notStarted *= self.start

    def start(self): pass
    def update_logic(self): pass
    def update_click(self): pass
    def update_render(self): pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)



class Transform(Component):
    def __init__(self, pos: tff = ZERO, anchor: tff = CENTER, rot = 0.0, scale = 1, hitbox: tff = ZERO, straight = False):
        self.pos = vec(pos)
        self.rot = rot
        self.scale = vec(scale)
        self.anchor = vec(anchor)
        self.straight = straight
    
        self.l_hitboxSize = vec(hitbox)
        #self.l_hitboxTopleft = vec(ZERO)
        self.g_pos = vec(pos)
        self.g_rot = rot
        self.g_scale = vec(scale)

    def start(self):
        self.parent = self.go.parent.transf if self.go.parent else None

    def update_logic(self):
        if self.parent is None:
            self.g_pos = self.pos
            self.g_rot = self.rot
            self.g_scale = self.scale
            return
        self.g_scale = self.scale.elementwise() * self.parent.g_scale
        rel = self.pos.elementwise() * self.parent.g_scale
        self.g_rot = self.rot + self.parent.g_rot
        rel.rotate_ip(-self.parent.g_rot)
        self.g_pos = self.parent.g_pos + rel



class GameObject:
    '''GameObject dùng để chạy các components, hoạt động như Unity'''
    prefabs: dict[str, 'Transform'] = {}
    e_goCreated: Event['GameObject'] = Event()          # Do nothing
    e_childsChanged: Event['GameObject'] = Event()      # Do nothing
    defaultParent: 'GameObject' = None # type: ignore

    def __init__(self, name = "", parent: No['GameObject'] = None, startEnabled = True, **kwargs):
        self.name = name if name != "" else f"Object {id(self)}"
        
        self.childs: list['GameObject'] = []
        self.coms: dict[type[Component], Component] = {}
        self.parent = parent

        self.transf: 'Transform'
        self += Transform(**kwargs)
        self.transf = self.getComponent(Transform)

        if parent: parent.childs.append(self)
        elif GameObject.defaultParent:
            GameObject.defaultParent.addChildren(self)

        self.enabled = startEnabled
        self.exist = True
        GameObject.e_goCreated(self)

    def __add__(self, com: type[TCom] | Component) -> 'GameObject':
        '''Tạo liên tiếp các components'''
        if isinstance(com, type):
            if not self.tryGetComponent(com):
                obj = com()
                self.coms[com] = obj
                obj._binding(self)
        elif isinstance(com, Component):
            if not self.tryGetComponent(type(com)):
                self.coms[type(com)] = com
                com._binding(self)
        return self

    def __iadd__(self, com: type[TCom] | Component) -> 'GameObject':
        return self + com

    def addComponent(self, com: type[TCom] | Component) -> TCom:
        self += com
        return com if isinstance(com, Component) else self.coms[com] # type: ignore

    def getComponent(self, com: type[TCom]) -> TCom:
        return self.coms[com] # type: ignore

    def tryGetComponent(self, com: type[TCom]) -> TCom | None:
        '''Bạn sợ à?'''
        return self.coms.get(com, None) # type: ignore
    
    def tryGet_parentComponent(self, com: type[TCom]) -> TCom | None:
        '''Tìm component từ parent'''
        return self.parent.tryGetComponent(com) if self.parent else None

    def removeParent(self):
        if self.parent:
            self.parent.removeChildren(self)
            GameObject.e_childsChanged(self)

    def addChildren(self, go: 'GameObject'):
        '''Nhận nuôi GameObject, kết nối parent <---> children'''
        self.childs.append(go)
        go.parent = self
        go.transf.parent = self.transf
        GameObject.e_childsChanged(self)

    def removeChildren(self, go: 'GameObject'):
        '''Jack bỏ con'''
        self.childs.remove(go)
        GameObject.defaultParent.addChildren(go)
        go.transf.parent = GameObject.defaultParent.transf
        GameObject.e_childsChanged(self)

    def update_logic(self):
        if not self.enabled: return
        for com in self.coms.values():
            if com.enabled: com.update_logic()

        for child in self.childs:
            child.update_logic()

    def update_click(self):
        if not self.enabled: return
        for com in reversed(self.coms.values()):
            if com.enabled: com.update_click()

        for child in reversed(self.childs):
            child.update_click()

    def update_render(self):
        if not self.enabled: return
        for com in self.coms.values():
            if com.enabled: com.update_render()

        for child in self.childs:
            child.update_render()

    def restart(self):
        '''Khuyên chỉ dùng sau khi tạo prefab'''
        for com in self.coms.values():
            com.start()

        for child in self.childs:
            child.restart()

    def destroy(self):
        print(f"Destroy {self.name}")
        if self.parent:
            self.parent.childs.remove(self)
        self.enabled = False
        self.exist = False
    
    @staticmethod
    def loadPrefab(name: str, parent: No['GameObject'] = None, pos: No[vec] = None, store = True, edit = False) -> 'GameObject':
        '''Chép hoàn toàn prefab từ bộ nhớ (store), không có thì thử mở'''
        obj = GameObject.prefabs.get(name) if store else None
 
        path = f"assets\\prefabs\\{name}"
        if not obj and os.path.exists(path):
            with open(path, "rb") as f:
                obj = pickle.load(f)
                if store: GameObject.prefabs[name] = obj

        if obj is None:
            raise FileNotFoundError(f"Không tìm thấy prefab {name}")
        
        deep = deepcopy(cast('GameObject', obj))
        if parent: parent.addChildren(deep)
        else: GameObject.defaultParent.addChildren(deep)
        if pos: deep.transf.pos = pos

        if not edit: deep.restart()

        deep.name += f" ({id(deep)})"
        # print(f"Đã tạo {deep.name}")
        return deep


    def savePrefab(self, name: str = "", delete = False, overwrite = True):
        '''Lưu prefab vào assets/prefab'''
        path = f"assets\\prefabs\\{name if name != '' else self.name}"
        old_parent = self.parent # Không lưu parent ngoài
        if not overwrite and os.path.exists(path): 
            # print("Không thể lưu đè (overwrite = False)")
            return
        
        if self.parent:
            self.parent.removeChildren(self)
        
        os.makedirs("assets\\prefabs\\", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        
        print(f"Đã lưu {path}")
        if not delete and old_parent: 
            old_parent.addChildren(self)
        if delete: self.destroy()