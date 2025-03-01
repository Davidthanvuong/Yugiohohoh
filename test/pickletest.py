import pickle  # Or use pickle if pickle isn't needed
import pygame

class GameObject:
    def __init__(self, name, position, components, surface):
        self.name = name
        self.position = position  # (x, y)
        self.components = components  # Dict of game components
        self._surface = surface  # Pygame surface (non-serializable)

    def __getstate__(self):
        """Custom serialization: Ignore _surface and only save essential data."""
        state = self.__dict__.copy()
        state.pop("_surface", None)  # Remove non-serializable attributes
        return state

    def __setstate__(self, state):
        """Custom deserialization: Restore state without _surface."""
        self.__dict__.update(state)
        self._surface = None  # Placeholder, can be regenerated later

# Example usage
pygame.init()
surface = pygame.Surface((100, 100))
obj = GameObject("Player", (50, 75), {"health": 100}, surface)

# Serialize with pickle (or pickle)
serialized_data = pickle.dumps(obj)

print(obj._surface)

# Deserialize
loaded_obj = pickle.loads(serialized_data)

print(loaded_obj.name)       # Output: Player
print(loaded_obj.position)   # Output: (50, 75)
print(loaded_obj._surface)   # Output: None (avoids crashing)
