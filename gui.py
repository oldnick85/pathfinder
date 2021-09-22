from typing import Optional, Set, List
import math

from pathfinder.common import Position, PositionDistance, Path
from pathfinder.search import PathSearchContext

from tkinter import Tk, Canvas, Frame, BOTH
 
class GuiPosition(Position):
    def __init__(self, x : int, y : int, passability : float = 1.0) -> None:
        super().__init__()
        self.x : int = x
        self.y : int = y
        self.passability = passability
        self.__adj : Set[PositionDistance] = set()
        return

    def __str__(self) -> str:
        return f"({self.x};{self.y})"

    def __repr__(self) -> str:
        return f"({self.x};{self.y})"

    def add_adj(self, adj : PositionDistance) -> None:
        self.__adj.add(adj)
        return

    def set_adj(self, adj : Set[PositionDistance]) -> None:
        self.__adj = adj
        return

    def draw(self, canvas : Canvas, pd_l : List[PositionDistance], pos1 : Position, pos2 : Position) -> None:
        txt = ""
        c = [0, 0, 0]
        for pd in pd_l:
            i = 0 if (pd.get_position() == pos2) else 1
            d = pd.get_distance()
            c[i] = int(d) % 16
            txt += f"{d:0.2};"
        color = f"#{c[0]:x}{c[1]:x}{c[2]:x}"
        canvas.create_rectangle(self.x*50, self.y*50, self.x*50+50-2, self.y*50+50-2, outline="#fb0", fill=color)
        canvas.create_text(self.x*50+25, self.y*50+25, text=txt, fill="#fff")
        return

    def get_adjacent(self) -> Set[PositionDistance]:
        return self.__adj

class GuiArea:
    def __init__(self) -> None:
        self.positions : List[List[GuiPosition]] = []
        for x in range(10):
            row : List[GuiPosition] = []
            for y in range(10):
                pos = GuiPosition(x, y)
                row.append(pos)
            self.positions.append(row)

        self.positions[3][0].passability = 10
        self.positions[3][1].passability = 10
        self.positions[3][2].passability = 10
        self.positions[3][3].passability = 10
        self.positions[3][4].passability = 10
        self.positions[2][4].passability = 10
        self.positions[1][4].passability = 10
        self.positions[0][4].passability = 2

        for x in range(10):
            for y in range(10):
                pos = self.positions[x][y]
                if (x > 0):
                    pos_adj = self.positions[x-1][y]
                    d = (pos.passability + pos_adj.passability)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (x < 9):
                    pos_adj = self.positions[x+1][y]
                    d = (pos.passability + pos_adj.passability)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (y > 0):
                    pos_adj = self.positions[x][y-1]
                    d = (pos.passability + pos_adj.passability)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (y < 9):
                    pos_adj = self.positions[x][y+1]
                    d = (pos.passability + pos_adj.passability)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (x > 0) and (y > 0):
                    pos_adj = self.positions[x-1][y-1]
                    d = (pos.passability + pos_adj.passability)*math.sqrt(2)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (x > 0) and (y < 9):
                    pos_adj = self.positions[x-1][y+1]
                    d = (pos.passability + pos_adj.passability)*math.sqrt(2)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (x < 9) and (y > 0):
                    pos_adj = self.positions[x+1][y-1]
                    d = (pos.passability + pos_adj.passability)*math.sqrt(2)/2
                    pos.add_adj(PositionDistance(pos_adj, d))
                if (x < 9) and (y < 9):
                    pos_adj = self.positions[x+1][y+1]
                    d = (pos.passability + pos_adj.passability)*math.sqrt(2)/2
                    pos.add_adj(PositionDistance(pos_adj, d))

        self.path_ctx = PathSearchContext()
        self.pos1 = self.positions[1][1]
        self.pos2 = self.positions[9][9]
        self.path = self.path_ctx.find_path(self.pos1, self.pos2, None)
        print(self.path)
        return

    def draw(self, canvas) -> None:
        for x in range(10):
            for y in range(10):
                pd_l = self.path_ctx.calculated_distances(self.positions[x][y])
                self.positions[x][y].draw(canvas, pd_l, self.pos1, self.pos2)
        pos1 = None
        for pos in self.path.steps:
            if (pos1 != None):
                canvas.create_line(pos1.x*50+25, pos1.y*50+25, pos.x*50+25, pos.y*50+25, fill="#fff")
            pos1 = pos
        return
 
class Example(Frame):
    def __init__(self):
        super().__init__()
        self.area = GuiArea()
        self.initUI()
        return
 
    def initUI(self):
        self.master.title("LEE")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        self.area.draw(canvas)
        #canvas.create_rectangle( 30, 10, 120, 80, outline="#fb0", fill="#fb0")
        #canvas.create_rectangle(150, 10, 240, 80, outline="#f50", fill="#f50")
        #canvas.create_rectangle(270, 10, 370, 80, outline="#05f", fill="#05f")
        canvas.pack(fill=BOTH, expand=1)
        return
 
def main():
    root = Tk()
    ex = Example()
    root.geometry("600x600+300+300")
    root.mainloop()
 
 
if __name__ == '__main__':
    main()