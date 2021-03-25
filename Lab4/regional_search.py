from segment_tree import *
from threaded_binary_tree import *


class RegionalSearch:

    def __init__(self):
        self.tree = None
        self.points = []

    @staticmethod
    def init_func(item):
        tree = ThreadedBinaryTree(lambda p: p.y)
        tree.insert(item)
        return tree

    @staticmethod
    def operation(left, right):
        new_tree = ThreadedBinaryTree(lambda p: p.y)

        values_left = left.get_values()
        values_right = right.get_values()

        i, j = 0, 0
        while i < len(values_left) and j < len(values_right):
            new_tree.insert(values_left[i])
            new_tree.insert(values_right[j])
            i += 1
            j += 1
        if i < len(values_left):
            new_tree.insert(values_left[i])
        elif j < len(values_right):
            new_tree.insert(values_right[j])

        return new_tree

    def add_point(self, point):
        index = self.__find_position(point, 0, len(self.points))
        if index == len(self.points):
            self.points.append(point)
        else:
            self.points.insert(index, point)
        self.tree = SegmentTree(self.points, self.init_func, self.operation, lambda p: p.x)

    def __find_position(self, point, left, right):
        if left == right:
            return left

        mid = left + (right - left) // 2

        if self.points[mid].x > point.x:
            return self.__find_position(point, left, mid)
        else:
            if mid == left:
                return mid + 1
            return self.__find_position(point, mid, right)

    def execute(self, region):
        result = []
        if self.tree is not None:
            subtrees = self.tree.search(region.p1.x, region.p2.x)
            for subtree in subtrees:
                result += subtree.search(region.p1.y, region.p2.y)
        return result
