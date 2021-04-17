import graphics
import entities
from simple_polygon_hull_builder import SimplePolygonHullBuilder


class Main:
    width = 1000
    height = 700
    win = graphics.GraphWin("Convex hull of a simple polygon", width, height)
    points = []
    points_entered = False

    @staticmethod
    def on_mouse_right_click(event):
        if Main.points_entered:
            return
        point = entities.Point(event.x, event.y)
        if any(point.x == p.x and point.y == p.y for p in Main.points):
            return

        if len(Main.points) != 0:
            edge = graphics.Line(graphics.Point(Main.points[-1].x, Main.points[-1].y), graphics.Point(point.x, point.y))
            edge.setWidth(2)
            edge.setFill("black")
            edge.setOutline("black")
            edge.draw(Main.win)

        Main.points.append(point)
        point.draw(Main.win)

    @staticmethod
    def on_mouse_left_click(event):
        if Main.points_entered or len(Main.points) < 3:
            return
        Main.points_entered = True

        for item in Main.win.items:
            item.undraw()
        Main.points.reverse()

        polygon = entities.Polygon(Main.points)
        polygon.draw(Main.win, "black")
        hull = SimplePolygonHullBuilder.execute(polygon)
        hull.draw(Main.win, "red")

    @staticmethod
    def main():
        Main.win.bind('<Button-1>', Main.on_mouse_right_click)
        Main.win.bind('<Button-3>', Main.on_mouse_left_click)
        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
