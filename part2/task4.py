import math
from tkinter import *

class KochTriangle:
    def __init__(self):
        window = Tk()
        window.title("Koch Triangle")
        self.width = 200
        self.height = 200
        self.canvas = Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()
        frame1 = Frame(window)
        frame1.pack()
        Label(frame1, text="Enter an order: ").pack(side=LEFT)
        self.order = StringVar()
        enter = Entry(frame1, textvariable=self.order, justify=RIGHT).pack(side=LEFT)
        Button(frame1, text="Display Koch Triangle", command=self.display).pack(side=LEFT)
        window.mainloop()

    def display(self):
        self.canvas.delete("line")
        p1 = [self.width / 2, 25]
        p2 = [25, self.height - 50]
        p3 = [self.width - 25, self.height - 50]
        order = int(self.order.get())
        self.display_koch(order, p1, p2)
        self.display_koch(order, p2, p3)
        self.display_koch(order, p3, p1)

    def display_koch(self, order, p1, p2):
        if order == 0:
            self.draw_line(p1, p2)
        else:
            dx = (p2[0] - p1[0]) / 3
            dy = (p2[1] - p1[1]) / 3
            p1st = [p1[0] + dx, p1[1] + dy]
            p2nd = [p1[0] + 2 * dx, p1[1] + 2 * dy]
            angle = math.radians(60)
            px = p1st[0] + (dx * math.cos(angle) - dy * math.sin(angle))
            py = p1st[1] + (dx * math.sin(angle) + dy * math.cos(angle))
            p3rd = [px, py]
            self.display_koch(order - 1, p1, p1st)
            self.display_koch(order - 1, p1st, p3rd)
            self.display_koch(order - 1, p3rd, p2nd)
            self.display_koch(order - 1, p2nd, p2)

    def draw_line(self, p1, p2):
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], tags="line")

KochTriangle()