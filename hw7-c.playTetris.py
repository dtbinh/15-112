# tetris-after-step-2.py
# fall-2015 version

from tkinter import *
import random

def init(data):
    # set board dimensions and margin
    data.rows = 15
    data.cols = 10
    data.margin = 20
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    # pre-load a few cells with known colors for testing purposes
    data.isGameOver = False
    data.isPause = False
    data.score = 0
    creatPieces(data)
    newFallingPiece(data)

def creatPieces(data):
    #Seven "standard" pieces (tetrominoes)
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],[ True, True,  True]]
    lPiece = [[ False, False, True],
              [  True,  True,  True]] 
    oPiece = [[ True, True],
              [ True, True]]
    sPiece = [[ False, True, True],
              [ True,  True, False ]]
    tPiece = [[ False, True, False ],
              [ True,  True, True]]
    zPiece = [[ True,  True, False ],
              [ False, True, True]]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", \
                          "pink", "cyan", "green", "orange" ]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def newFallingPiece(data):
    newPieceShape = random.randint(0, len(data.tetrisPieces)-1)
    newPieceColor = random.randint(0, len(data.tetrisPieceColors)-1)
    data.fallingPieceShape = data.tetrisPieces[newPieceShape]
    data.fallingPieceColor = data.tetrisPieceColors[newPieceColor]
    data.fallingPieceRow   = 0
    data.fallingPieceCol   = data.cols//2 - len(data.fallingPieceShape[0])//2

def moveFallingPiece(data, drow, dcol):
    tempRow = data.fallingPieceRow
    tempCol = data.fallingPieceCol
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if  not fallingPieceIsLegal(data):
        data.fallingPieceRow = tempRow
        data.fallingPieceCol = tempCol
        return False
    return True

def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPieceShape)):
        for col in range(len(data.fallingPieceShape[0])):
            if data.fallingPieceShape[row][col] == True and\
              (data.fallingPieceRow + row not in range(data.rows) or
               data.fallingPieceCol + col not in range(data.cols) or
               data.board[data.fallingPieceRow+row][data.fallingPieceCol+col]
                                               != data.emptyColor):
                return False
    return True

def rotateFallingPiece(data):
    oldRows = len(data.fallingPieceShape)
    oldCols = len(data.fallingPieceShape[0])
    tempPieceShape = data.fallingPieceShape
    tempRow = data.fallingPieceRow
    tempCol = data.fallingPieceCol
    data.fallingPieceShape = [([0] * oldRows) for col in range(oldCols)]
    for row in range(oldRows):
        for col in range(oldCols):
            data.fallingPieceShape[oldCols-col-1][row]=tempPieceShape[row][col]
    oldCenterRow = tempRow + (oldRows-1)//2
    oldCenterCol = tempCol + (oldCols-1)//2
    data.fallingPieceRow = oldCenterRow - (oldCols-1)//2
    data.fallingPieceCol = oldCenterCol - (oldRows-1)//2
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow   = tempRow
        data.fallingPieceCol   = tempCol
        data.fallingPieceShape = tempPieceShape

def placeFallingPiece(data):
    for row in range(len(data.fallingPieceShape)):
        for col in range(len(data.fallingPieceShape[0])):
            if data.fallingPieceShape[row][col] == True:
                data.board[data.fallingPieceRow + row]\
                          [data.fallingPieceCol + col]\
                           = data.fallingPieceColor

def removeFullRows(data):
    newBoard = []
    count = 0
    for i in range(len(data.board)):
        row = data.board[data.rows-i-1]
        if data.emptyColor in row:
            count += 1
            newBoard.append(row)
    for j in range(len(data.board)-count):
        newBoard.append([data.emptyColor] * data.cols)
    data.score += (len(data.board)-count)**2
    data.board = newBoard[::-1]


def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if   (event.keysym == "Left"):  moveFallingPiece(data, 0, -1)
    elif (event.keysym == "Right"): moveFallingPiece(data, 0, +1)
    elif (event.keysym == "Down"):  moveFallingPiece(data, 1, 0)
    elif (event.keysym == "Up"):    rotateFallingPiece(data)
    elif (event.keysym == "r"): init(data); return
    elif (event.keysym == "p"): data.isPause = not data.isPause

def timerFired(data):
    if (data.isPause or data.isGameOver): return
    elif moveFallingPiece(data,+1,0) == False:
        placeFallingPiece(data)
        newFallingPiece(data)
        if fallingPieceIsLegal(data) == False:
            data.isGameOver = True
            data.fallingPieceShape = [data.fallingPieceShape[1]]
    removeFullRows(data)

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPieceShape)):
        for col in range(len(data.fallingPieceShape[0])):
            if data.fallingPieceShape[row][col] == True:
                drawCell(canvas, data, data.fallingPieceRow + row,
                                       data.fallingPieceCol + col,
                                       data.fallingPieceColor)

def drawCell(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def drawGameOver(canvas, data):
    if (data.isGameOver):
        canvas.create_text(data.width/2, data.height/2, text="Game over!",
                           font="Arial 26 bold", fill = 'white')

def drawPause(canvas, data):
    if (data.isPause):
        canvas.create_text(data.width/2, data.height/2, text="Pause",
                           font="Arial 26 bold", fill = 'white')

def drawScore(canvas, data):
    msg = 'score:'+str(data.score)
    canvas.create_text(data.width/2, data.margin/2, text=msg,
                           font="Arial 10 bold", fill = 'white')

def redrawAll(canvas, data):
    drawGame(canvas, data)
    drawFallingPiece(canvas, data)
    drawGameOver(canvas, data)
    drawPause(canvas, data)
    drawScore(canvas, data)

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
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
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

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()