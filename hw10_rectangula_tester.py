# hw10_rectangula_tester.py

from tkinter import *
from tkinter import messagebox
import copy


###############################################
# Rectangula tester
###############################################

def solvesRectangula(board, solution):
    # verify that every integer on the board is inside
    # a rectangle of that area in the solution, and that
    # every rectangle in the solution contains exactly
    # one integer on the board
    board = copy.deepcopy(board)
    (rows, cols) = (len(board), len(board[0]))
    for rect in solution:
        (row0, col0, width, height) = rect
        (row1, col1) = (row0 + height - 1, col0 + width - 1)
        # verify we are on the board
        if ((row0 < 0) or (row1 >= rows) or
            (col0 < 0) or (col1 >= cols)):
            return False
        # verify there is exactly one nonzero board value
        # in this rectangle, and set that to zero here
        foundNonZeroValue = False
        for row in range(row0, row1+1):
            for col in range(col0, col1+1):
                if (board[row][col] != 0):
                    if (foundNonZeroValue): return False
                    foundNonZeroValue = True
                    board[row][col] = 0
        if (not foundNonZeroValue): return False
    # Now verify the board has no remaining nonzero values
    for row in range(rows):
        for col in range(cols):
            if (board[row][col] != 0): return False
    return True

def testSolveRectangula(solveRectangulaFn):
    global solveRectangula
    solveRectangula = solveRectangulaFn
    print("Testing solveRectangula()...", end="")
    goodBoards = [
                [[0, 2, 0],
                 [3, 2, 0],
                 [0, 0, 2]],

                [[3, 0, 0, 0],
                 [0, 3, 0, 0],
                 [2, 4, 0, 0],
                 [0, 0, 0, 0]],
             ]
    for board in goodBoards:
        solution = solveRectangula(board)
        assert(solvesRectangula(board, solution))

    badBoards = [
                [[0, 2, 0],
                 [3, 2, 0],
                 [0, 0, 3]],

                [[3, 0, 0, 0],
                 [0, 3, 0, 0],
                 [2, 4, 0, 0],
                 [2, 0, 0, 0]],
             ]
    for board in badBoards:
        solution = solveRectangula(board)
        assert(solution == None)
    print("Passed!")

# testSolveRectangula()

###############################################
# Rectangula UI
###############################################

# To easily turn on/off db output
def db(*args):
    dbOn = False
    if (dbOn): print(*args)

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

def init(data, rows=4, cols=4):
    data.rows = rows
    data.cols = cols
    data.margin = 5 # margin around grid
    data.selectedRow = 0
    data.selectedCol = 0
    data.solution = None
    data.board = make2dList(rows, cols)

def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    data.solution = None # clear solution on each key press
    if (event.keysym == "Up"):
        if (data.selectedRow-1 >= 0): data.selectedRow -= 1
    elif (event.keysym == "Down"):
        if (data.selectedRow+1 < data.rows): data.selectedRow += 1
    elif (event.keysym == "Left"):
        if (data.selectedCol-1 >= 0): data.selectedCol -= 1
    elif (event.keysym == "Right"):
        if (data.selectedCol+1 < data.cols): data.selectedCol += 1
    elif (event.keysym == "plus"):
        init(data, rows=data.rows+1, cols=data.cols+1)
    elif (event.keysym == "minus"):
        if (min(data.rows, data.cols) > 1):
            init(data, rows=data.rows-1, cols=data.cols-1)
    elif (event.keysym in ["Delete", "BackSpace", "0"]):
        data.board[data.selectedRow][data.selectedCol] = 0
    elif (event.keysym.isdigit()):
        data.board[data.selectedRow][data.selectedCol] = int(event.keysym)
    elif (event.keysym == "s"):
        runSolver(data)

def showMessageBox(data, message, title="Info box"):
    messagebox.showinfo(title, message, parent=data.root)

def runSolver(data):
    data.solution = solveRectangula(data.board)
    db(data.board)
    db(data.solution)
    if (data.solution == None):
        showMessageBox(data, "No solution found!")
    elif (data.solution == [ ]):
        showMessageBox(data, "Empty solution (no rectangles needed!)")

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawDirections(canvas, data)
    if (data.solution == None):
        drawGrid(canvas, data, True)
    else:
        drawGrid(canvas, data, False)
        drawSolution(canvas, data)

def drawGrid(canvas, data, highlightSelection=True):
    (srow, scol) = (data.selectedRow, data.selectedCol)
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = "cyan"
            if (highlightSelection and ((srow, scol) == (row, col))):
                fill = "orange"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            if (data.board[row][col] != 0):
                canvas.create_text((x0+x1)/2, (y0+y1)/2,
                                   text=str(data.board[row][col]))

def drawSolution(canvas, data):
    for rect in data.solution:
        (row0, col0, width, height) = rect
        (row1, col1) = (row0 + height - 1, col0 + width - 1)
        (x0, y0, _, _) = getCellBounds(row0, col0, data)
        (_, _, x1, y1) = getCellBounds(row1, col1, data)
        canvas.create_rectangle(x0, y0, x1, y1, fill=None, width=4)

def drawDirections(canvas, data):
    msgs = ["Rectangula!",
            "Use +/- keys to change grid size",
            "Use arrow keys to select cells",
            "Use 1-9 keys to set cell values",
            "Use 0 or Delete keys to clear cell values",
            "Use s key to solve the puzzle"
           ]
    for i in range(len(msgs)):
        canvas.create_text(data.width/2,
                           data.height + (i+1)*20,
                           text=msgs[i])

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = width # so grid is width x width
    data.fullHeight = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    data.root = root # for showMessageBox parent
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playRectangula(solveRectangulaFn):
    global solveRectangula
    solveRectangula = solveRectangulaFn
    run(300, 435)
