import entities
import utils


class SimplePolygonHullBuilder:

    class StraightStrategy:
        @staticmethod
        def get_fake_point(p):
            return entities.Point(p.x, p.y - 1)

    class InvertedStrategy:
        @staticmethod
        def get_fake_point(p):
            return entities.Point(p.x, p.y + 1)

    @staticmethod
    def execute(polygon):
        min_point = min(polygon.points)
        max_point = max(polygon.points)

        points = SimplePolygonHullBuilder.__build_chain(min_point, max_point, polygon.points,
                                                      SimplePolygonHullBuilder.StraightStrategy) + \
               SimplePolygonHullBuilder.__build_chain(max_point, min_point, polygon.points,
                                                      SimplePolygonHullBuilder.InvertedStrategy)
        return entities.Polygon(points)

    @staticmethod
    def __build_chain(start_point, end_point, points, strategy):
        start_index = points.index(start_point)
        end_index = points.index(end_point)

        seq_len = end_index - start_index
        if start_index > end_index:
            seq_len = len(points) - start_index + end_index

        points_queue = [points[(start_index + i + 1) % len(points)] for i in range(seq_len)]
        points_queue.reverse()

        fake_point = strategy.get_fake_point(start_point)
        chain = [fake_point, start_point]
        prev_to_vertex = fake_point

        while len(points_queue) != 0:
            current = points_queue.pop()

            if utils.ccw(chain[-2], chain[-1], current) >= 0:
                # field 2
                while utils.ccw(chain[-2], chain[-1], current) > 0:
                    chain.pop()
                chain.append(current)
            else:
                if utils.ccw(prev_to_vertex, chain[-1], current) >= 0:
                    # field 1
                    while utils.ccw(chain[-1], chain[-2], points_queue[-1]) >= 0:
                        points_queue.pop()
                else:
                    if utils.ccw(end_point, chain[-1], current) > 0:
                        # field 4
                        while utils.ccw(end_point, chain[-1], points_queue[-1]) > 0:
                            points_queue.pop()
                    else:
                        # field 3
                        chain.append(current)

            if chain[-1] != start_point:
                prev_to_vertex = points[points.index(chain[-1]) - 1]

        chain.pop(0)
        return chain
