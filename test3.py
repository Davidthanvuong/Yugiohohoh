class Node:
    _ROOT_SENTINEL = object()  # Unique sentinel value for root nodes

    def __new__(cls, parent=None):
        if parent is None:
            instance = super().__new__(cls)
            instance.parent = cls._ROOT_SENTINEL  # Assign sentinel for root node
            return instance
        return super().__new__(cls)

    def __init__(self, parent=None):
        if parent is not None:
            self.parent = parent

    @property
    def is_root(self):
        return self.parent is self._ROOT_SENTINEL  # Fast identity check

# Usage
root = Node()       # Implicit root node
child = Node(root)  # Child node

print(root.is_root)  # True
print(child.is_root) # False
