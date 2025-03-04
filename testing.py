from abc import ABC, abstractmethod
from typing import Any, Dict

class Component(ABC):
    #"""Base class for components that collects defaults via MRO."""
    @classmethod
    def get_defaultKeys(cls) -> Dict[str, Any]:
        """Lấy từ MRO các `Component`"""
        keys = {}
        for base in reversed(cls.__mro__):
            keys.update({
                key: value for key, value in base.__dict__.items()
                if (not key[0] == '_') and (not key[0].isupper()) and (not callable(value))
            })
        return keys


    def __init__(self, go: 'GameObject'):
        self.go = go
        for key, value in self.get_defaultKeys().items():
            setattr(self, key, value)


    @abstractmethod
    def start(self) -> None:
        """Execute dependency-related code only (e.g., get other components)."""
        pass

    def update(self) -> None:
        """Optional method for per-frame updates."""
        pass


class InputField(Component):#
    # Default class variables
    MAX_LENGTH = 20
    CURSOR_COLOR = (255, 255, 255)  # White
    TEXT_PADDING = 5

    def start(self) -> None:
        """Only handle dependencies, like getting other components."""
        self.text_component = self.go.get_component('Text')
        if not self.text_component:
            raise ValueError("InputField requires a Text component.")
        self.input_text = ""  # Initialize runtime state

    def update(self) -> None:
        """Use defaults directly as instance attributes."""
        if len(self.input_text) < self.MAX_LENGTH:
            # Add input handling logic here
            pass
        self.text_component.text = self.input_text


class GameObject:
    def __init__(self):
        self.components = []

    def add(self, component: 'Component') -> 'Component':
        """Add a component and return it."""
        component = component(self)
        self.components.append(component)
        return component

    def start(self):
        """Call start on all components for dependency setup."""
        for component in self.components:
            component.start()

    def get_component(self, component_type: str) -> 'Component':
        """Get a component by its type name."""
        for component in self.components:
            if component.__class__.__name__ == component_type:
                return component
        raise Exception("Gay")
    
# Create a GameObject
go = GameObject()

# Add components
go.add(Text)  # Assume Text is another component class
input_field = go.add(InputField)

# Override a default if needed
input_field.MAX_LENGTH = 30  # Changes the instance attribute

# Start all components
go.start()

# Use the component
print(input_field.MAX_LENGTH)  # 30
print(input_field.CURSOR_COLOR)  # (255, 255, 255)