import graphics
from regional_search import *


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pict = graphics.Circle(graphics.Point(x, y), 3)
        self.pict.setFill("black")
        self.pict.setOutline("black")

    def set_color(self, color):
        self.pict.setFill(color)
        self.pict.setOutline(color)

    def draw(self, window):
        self.pict.draw(window)

    def undraw(self):
        self.pict.undraw()


class Region:

    def __init__(self, p1, p2):
        self.p1 = Point(p1.x, p1.y)
        self.p2 = Point(p2.x, p2.y)

        if p1.x > p2.x:
            self.p1.x, self.p2.x = p2.x, p1.x
        if p1.y > p2.y:
            self.p1.y, self.p2.y = p2.y, p1.y

        self.lines = [graphics.Line(graphics.Point(p1.x, p1.y), graphics.Point(p1.x, p2.y)),
                      graphics.Line(graphics.Point(p1.x, p2.y), graphics.Point(p2.x, p2.y)),
                      graphics.Line(graphics.Point(p2.x, p2.y), graphics.Point(p2.x, p1.y)),
                      graphics.Line(graphics.Point(p2.x, p1.y), graphics.Point(p1.x, p1.y))]

        for line in self.lines:
            line.setWidth(2)
            line.setFill("red")
            line.setOutline("red")

    def draw(self, window):
        for line in self.lines:
            line.draw(window)

    def undraw(self):
        for line in self.lines:
            line.undraw()


class Main:
    win = graphics.GraphWin("Regional Search", 1000, 700)
    regional_search = RegionalSearch()
    region = None
    temp_region = None
    isRegionBeingDrawn = False
    firstRegionPoint = None
    painted_points = []

    @staticmethod
    def clear_region():
        Main.firstRegionPoint = None

        if Main.region is not None:
            Main.region.undraw()
            Main.region = None
            for p in Main.painted_points:
                p.undraw()
                p.set_color("black")
                p.draw(Main.win)
        elif Main.temp_region is not None:
            Main.temp_region.undraw()
            Main.temp_region = None

    @staticmethod
    def on_mouse_left_click(event):
        Main.clear_region()
        present = any(p.x == event.x and p.y == event.y for p in Main.regional_search.points)

        if not present:
            if Main.region is not None:
                Main.clear_region()
            new_point = Point(event.x, event.y)
            new_point.draw(Main.win)
            Main.regional_search.add_point(new_point)

    @staticmethod
    def on_mouse_right_click(event):
        if Main.firstRegionPoint is None:
            if Main.region is not None:
                Main.clear_region()
            Main.firstRegionPoint = Point(event.x, event.y)
        else:
            Main.temp_region.undraw()
            Main.temp_region = None

            Main.region = Region(Main.firstRegionPoint, Point(event.x, event.y))
            Main.firstRegionPoint = None
            Main.region.draw(Main.win)

            Main.painted_points = Main.regional_search.execute(Main.region)
            for p in Main.painted_points:
                p.undraw()
                p.set_color("red")
                p.draw(Main.win)

    @staticmethod
    def on_mouse_move(event):
        if Main.firstRegionPoint is not None:
            if Main.temp_region is not None:
                Main.temp_region.undraw()
            Main.temp_region = Region(Main.firstRegionPoint, Point(event.x, event.y))
            Main.temp_region.draw(Main.win)

    @staticmethod
    def main():
        Main.win.bind('<Button-1>', Main.on_mouse_left_click)
        Main.win.bind('<Button-3>', Main.on_mouse_right_click)
        Main.win.bind('<Motion>', Main.on_mouse_move)
        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
