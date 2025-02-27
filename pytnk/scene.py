from .header_objects import *
import pickle, os

class Scene:
    folder = "assets\\scenes\\"

    def __init__(self, name: str = ""):
        self.name = name
        self.objects: dict[str, Translite] = {}

    def add(self, name: str, tf: Translite) -> Translite:
        self.objects[name] = tf
        return tf

    def update(self, renderOnly = False):
        '''Cập nhật Scene theo trình tự logic --> render'''
        if not renderOnly:
            for obj in reversed(self.objects.values()):
                obj.click_update()

        for obj in self.objects.values():
            obj.render_update()

    def save(self, path: str):
        full = f"{Scene.folder}{path}"
        os.makedirs(Scene.folder, exist_ok=True)  # Ensure the directory exists
        with open(full, "wb") as f:
            pickle.dump(self.objects, f)
        
        print(f"Saved {full}")

    def try_load(self, path: str) -> bool:
        full = f"{Scene.folder}{path}"
        if os.path.exists(full):
            with open(full, "rb") as f:
                self.objects = pickle.load(f)
            print(f"Load success {full}")
            return True

        print(f"No file {full} existed")
        return False
    
    def serialize(self):
        print("Serial")
        return 0

    @classmethod
    def deserialize(cls, data):
        print("Deserial")