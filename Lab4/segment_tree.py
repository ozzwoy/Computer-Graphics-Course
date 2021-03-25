class SegmentTree:

    class Node:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.value = None
            self.left = None
            self.right = None

    def __init__(self, array, init_func, operation, get_key=lambda v: v):
        self.array = array
        self.init_func = init_func
        self.operation = operation
        self.get_key = get_key
        self.root = self.__build_node(0, len(array))

    def __build_node(self, start, end):
        if start >= end:
            return None
        node = self.Node(start, end)

        if start + 1 == end:
            node.value = self.init_func(self.array[start])
        else:
            node.left = self.__build_node(start, start + (end - start) // 2)
            node.right = self.__build_node(start + (end - start) // 2, end)
            node.value = self.operation(node.left.value, node.right.value)

        return node

    def search(self, min_key, max_key):
        if self.root is None:
            return []
        return self.__search(min_key, max_key, self.root)

    def __search(self, min_key, max_key, node):
        if self.get_key(self.array[node.start]) > max_key or self.get_key(self.array[node.end - 1]) < min_key:
            return []

        if self.get_key(self.array[node.start]) >= min_key and self.get_key(self.array[node.end - 1]) <= max_key:
            return [node.value]

        return self.__search(min_key, max_key, node.left) + self.__search(min_key, max_key, node.right)
