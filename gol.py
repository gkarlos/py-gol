
from Tkinter import *

##SETTINGS##
X_SQUARES = 80
Y_SQUARES = 50
SQUARE_WIDTH = 12
SQUARE_HEIGHT = 12
WINDOW_WIDTH = SQUARE_WIDTH * X_SQUARES + SQUARE_WIDTH*2
WINDOW_HEIGHT = SQUARE_HEIGHT * Y_SQUARES + SQUARE_HEIGHT*2
SPEED = 150
CELL_ALIVE = "OliveDrab1"
CELL_DEAD = "snow3"
#############

class Cell:
    def __init__(self, x, y, i, j):
        self.isAlive = False
        self.change = False
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        
    def doChange(self):
        self.isAlive = not self.isAlive
    
class Board(object):
    
    def __init__(self):
        self.root = Tk()
        self.root.resizable(0,0)
        self.cells = [[]]
        self.rectangles = [[]]
        self.canStart = False
        self.__init()
    
    def __init(self):
        self.root.title("Conway's Game of Life")
        self.frame = Frame(self.root, width = WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.__grid()
        self.__options()
    
    def __grid(self):
        x,y = SQUARE_WIDTH,SQUARE_HEIGHT
        xs = [x+SQUARE_WIDTH*i for i in range( X_SQUARES + 1)]
        ys = [y+SQUARE_HEIGHT*i for i in range( Y_SQUARES + 1)]
        self.rectangles = [[self.canvas.create_rectangle(xs[j], ys[i], xs[j+1], ys[i+1], fill=CELL_DEAD) for j in range(X_SQUARES)] for i in range(Y_SQUARES)]
        self.cells = [[Cell(xs[j],ys[i],i,j) for j in range(X_SQUARES)] for i in range(Y_SQUARES)]

    def __options(self):
        pass #TODO
        
    def toggleColor(self, event):
        self.canStart = True
        x, y = self.coordsOf(event)
        i,j = y / SQUARE_HEIGHT- 1, x / SQUARE_WIDTH - 1
        if i < 0 or j < 0:
            return
        self.canvas.itemconfig(self.rectangles[i][j], fill=CELL_DEAD if self.cells[i][j].isAlive else CELL_ALIVE)
        self.cells[i][j].doChange()

            
        
    
    def coordsOf(self, event):
        return (event.x - event.x % SQUARE_WIDTH, event.y - event.y % SQUARE_HEIGHT )
    

    
    def countAliveNeighbors(self, cell):
        aliveNeighbors = 0
        x, y = cell.i, cell.j
   
        neighbors = [(x-1, y-1), (x-1,y), (x-1, y+1), (x, y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1, y+1)]
        for neighbor in neighbors:
            try:
                if(neighbor[0] < 0):
                    continue
                elif(neighbor[1] < 0):
                    continue
                elif self.cells[neighbor[0]][neighbor[1]].isAlive:
                    aliveNeighbors += 1
            except IndexError:
                continue
        return aliveNeighbors
                
#             
    def tryUpdateCell(self, cell):
 
        aliveNeighbors = self.countAliveNeighbors(cell)

        if cell.isAlive and (aliveNeighbors < 2 or aliveNeighbors > 3):
            cell.change = True
            return True
        elif not cell.isAlive and aliveNeighbors == 3:
            cell.change = True
            return True
        else:
            return False
    
    def nextGeneration(self):
        keepGoing = False
        for row in self.cells:
            for cell in row:
                if self.tryUpdateCell(cell):
                    keepGoing = True
        if not keepGoing:
            self.canStart = False
        else:
            self.updateBoard()
        if self.canStart:
            self.root.after(SPEED, self.nextGeneration)
        else:
            self.resetGol(None)
    
    def updateBoard(self):
        for row in self.cells:
            for cell in row:
                if cell.change:
                    self.canvas.itemconfig(self.rectangles[cell.i][cell.j], fill =CELL_DEAD if cell.isAlive else CELL_ALIVE)
                    cell.doChange()     #    
                    cell.change = False # Prepare for next round

    
    def resetGol(self, event):
        self.canStart = False
        self.canvas.bind("<Button-1>", self.toggleColor)
        self.root.bind("<Return>", self.startGol)
        self.clearBoard()
    
    def clearBoard(self):
        for row in self.cells:
            for cell in row:
                self.canvas.itemconfig(self.rectangles[cell.i][cell.j], fill =CELL_DEAD)
                cell.isAlive = False
                cell.change = False
    
    def startGol(self, event):
        self.canStart = True
        self.canvas.unbind("<Button-1>")
        self.root.unbind("<Return>")
        self.nextGeneration()
    
    def start(self):
        self.canvas.bind("<Button-1>", self.toggleColor)
        self.root.bind("<Return>", self.startGol)
        self.root.bind("<space>", self.resetGol)
        self.root.mainloop()
        
if __name__ == '__main__':
    Board().start()
    