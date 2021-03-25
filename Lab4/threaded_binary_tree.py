class ThreadedBinaryTree:

    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.left_thread = True
            self.right_thread = True

        def hook_up_left(self, node):
            node.right = self
            node.left = self.left
            self.left = node
            self.left_thread = False

        def hook_up_right(self, node):
            node.left = self
            node.right = self.right
            self.right = node
            self.right_thread = False

        def next(self):
            if self.right_thread:
                return self.right

            current = self.right
            if current is not None:
                while not current.left_thread:
                    current = current.left

            return current

    def __init__(self, get_key=lambda v: v):
        self.root = None
        self.get_key = get_key

    def insert(self, value):
        if self.root is None:
            self.root = self.Node(value)
            return

        current = self.root
        while True:
            if self.get_key(value) < self.get_key(current.value):
                if not current.left_thread:
                    current = current.left
                else:
                    current.hook_up_left(self.Node(value))
                    return
            else:
                if not current.right_thread:
                    current = current.right
                else:
                    current.hook_up_right(self.Node(value))
                    return

    def __find_nearest(self, key):
        current = self.root

        while True:
            if key < self.get_key(current.value):
                if not current.left_thread:
                    current = current.left
                else:
                    break
            elif key > self.get_key(current.value):
                if not current.right_thread:
                    current = current.right
                else:
                    break
            else:
                break

        return current

    def search(self, min_key, max_key):
        result = []
        current = self.__find_nearest(min_key)

        if current is not None and self.get_key(current.value) < min_key:
            current = current.next()
        while current is not None and self.get_key(current.value) <= max_key:
            result.append(current.value)
            current = current.next()

        return result

    def get_values(self):
        result = []
        current = self.root

        if current is not None:
            while current.left is not None:
                current = current.left
            while current is not None:
                result.append(current.value)
                current = current.next()

        return result
