class Translite:
    def __init__(self, name: str):
        self.name = name
        self.components = {}

class Component:
    """Base class for all components."""
    def __init__(self, tf: Translite):
        self.tf = tf
        topmost_class = self._get_topmost_class()  # Find the correct key
        tf.components[topmost_class] = self  # ✅ Avoid overwrites

    def _get_topmost_class(self):
        """Finds the highest class in the hierarchy (excluding `Component`)."""
        for base in reversed(self.__class__.mro()):  # Traverse inheritance chain
            if base is not Component and issubclass(base, Component):
                return base
        return self.__class__  # Fallback

class Transform(Component):
    def __init__(self, tf: Translite, x: float = 0, y: float = 0):
        super().__init__(tf)
        self.x = x
        self.y = y

class Rigidbody(Component):
    def __init__(self, tf: Translite, mass: float = 1.0):
        super().__init__(tf)
        self.mass = mass

# ✅ Now multiple components don't overwrite each other
obj = Translite(name="Player")
Transform(obj, x=10, y=20)
Rigidbody(obj, mass=5.0)

print(obj.components)  # ✅ Both Transform and Rigidbody exist!
print(obj.components[Transform].x)  # 10
print(obj.components[Rigidbody].mass)  # 5.0
