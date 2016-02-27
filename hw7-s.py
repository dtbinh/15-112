# hw7.py
# Hanzhou Lu / hanzhoul / II

from tkinter import *
import random
import math

def init(data):
    if data.mode == 1:
        init1(data)
    elif data.mode == 2:
        init2(data)
    elif data.mode == 3:
        init3(data)
    elif data.mode == 4:
        init4(data)

def init1(data):
    data.blackgroundColor = '#66CCFF'
    data.patternRows = 10
    data.patternCols = 10
    data.patterDiameter = 45
    data.timerDelay = 100

def init2(data):
    data.cirleRadios = 4
    data.centerX = data.width/2
    data.centerY = data.height/2
    data.largestR = 200
    data.timerDelay = 1000*10

def init3(data):
    data.rows = 10
    data.cols = 10
    data.margin = 5 # margin around grid
    data.direction = (0, +1) # (drow, dcol)
    data.board = []
    for i in range(data.rows):
        data.board.append([0]*data.cols)
    data.board[5][5] = 1
    placeFood(data)
    data.timerDelay = 250
    data.gameOver = False
    data.paused = True

def init4(data):
    data.scrollX = 0  # amount view is scrolled to the right
    data.scrollMargin = 50 # closest player may come to either canvas edge
    data.playerX = data.scrollMargin # player's left edge
    data.playerY = 0  # player's bottom edge (distance above the base line)
    data.playerWidth = 10
    data.playerHeight = 20
    data.walls = 50
    data.wallPoints = [0]*data.walls
    data.wallWidth = 20
    data.wallHeight = 40
    data.wallSpacing = 90 # wall left edges are at 50, 100, 150,...
    data.currentWallHit = -1 # start out not hitting a wall
    data.speed = 0
    data.deltaSpeed = 2
    data.isDoingJump = False
    data.jumpStep = 0
    data.balloons = []
    data.eyeposition = 5
    data.balloonsRadios = 3
    data.balloonInitSpeed = 5
    data.timerDelay = 100

def drawSinglePattern(canvas,row,col,color,data):
    cx = data.marginX + row * data.patterDiameter + data.patterDiameter/2
    cy = data.marginY + col * data.patterDiameter + data.patterDiameter/2
    r = data.patterDiameter/2
    while r>1:
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
        r /= 1.5

def decidePatternColor(data):
    color = []
    for i in range(data.patternRows):
        color.append([0]*data.patternRows)
    for row in range(data.patternRows):
        for col in range(data.patternCols):
            if (row + col) % 4 == 0:
                color[row][col] = 'red'
            elif col % 3 == 0:
                color[row][col] = 'green'
            elif row % 2 == 1:
                color[row][col] = 'yellow'
            else:
                color[row][col] = 'blue'
    return color

def drawSingleCircle(canvas,data,color,n,originAngle):
    bigR = data.largestR*n/32
    for i in range(28):
        theta = i * (2*math.pi/28) + originAngle[n]
        x0 = data.centerX + math.cos(theta) * bigR
        y0 = data.centerY + math.sin(theta) * bigR
        r = data.cirleRadios
        canvas.create_oval(x0-r, y0-r, x0+r, y0+r, fill=color, outline = color)

def calculateOriginAngle(data):
    originAngle = [0]*32
    deltaX = [0]*32
    deltaY = [0]*32
    assistTheta = math.pi/2-(math.pi/4)/2
    assistCircleR = (data.largestR/2)/math.cos(assistTheta)
    assistCircleX = data.largestR/2
    assistCircleY = (data.largestR/2)*math.tan(assistTheta)
    for i in range(32):
        deltaX[i] = data.largestR*i/32
        deltaY[i] = assistCircleY - (assistCircleR**2-\
            (deltaX[i]-assistCircleX)**2)**0.5
        if deltaX[i] == 0:
            originAngle[i] == 0
        else:
            originAngle[i] = -math.atan(deltaY[i]/deltaX[i])
    return originAngle

def dicideColor():
    color = [0]*32
    (r0,g0,b0) = (255,255,0)            #which is yellow
    (r1,g1,b1) = (128,0,255)            #which is purple
    for i in range(32):
        ri = int((r1-r0)*i/32+r0)
        gi = int((g1-g0)*i/32+g0)
        bi = int((b1-b0)*i/32+b0)
        color[i] = '#%02x%02x%02x' % (ri, gi, bi)
    return color

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

def takeStep(data):
    (drow, dcol) = data.direction
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == 1:
                headRow = row
                headCol = col
    (newRow, newCol) = (headRow+drow, headCol+dcol)
    if ((newRow < 0) or (newRow >= data.rows) or
        (newCol < 0) or (newCol >= data.cols) or
        (data.board[newRow][newCol] > 0)):
        data.gameOver = True
    else:
        maxNumInBoard = 0
        for row in range(data.rows):
            for col in range(data.cols):
                if data.board[row][col] > maxNumInBoard:
                    maxNumInBoard = data.board[row][col]
                    tailRow = row
                    tailCol = col
                if data.board[row][col] > 0:
                    data.board[row][col] += 1
        if data.board[newRow][newCol] == -1:
            placeFood(data)
            data.board[newRow][newCol] = 1
        else:
            # didn't eat, so remove old tail (slither forward)
            data.board[newRow][newCol] = 1
            data.board[tailRow][tailCol] = 0

def placeFood(data):
    row0 = random.randint(0, data.rows-1)
    col0 = random.randint(0, data.cols-1)
    for drow in range(data.rows):
        for dcol in range(data.cols):
            row = (row0 + drow) % data.rows
            col = (col0 + dcol) % data.cols
            if data.board[row][col] == 0:
                data.board[row][col] = -1
                return

def getPlayerBounds(data):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = (data.playerX, data.height/2 - data.playerY)
    (x1, y0) = (x0 + data.playerWidth, y1 - data.playerHeight)
    return (x0, y0, x1, y1)

def getWallBounds(wall, data):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = ((1+wall) * data.wallSpacing, data.height/2)
    (x1, y0) = (x0 + data.wallWidth, y1 - data.wallHeight)
    return (x0, y0, x1, y1)

def getBalloonBounds(balloon, data):
    cx = data.balloons[balloon][0]
    cy = data.balloons[balloon][1]
    r = data.balloonsRadios
    (x0, y0) = (cx-r , cy-r)
    (x1, y1) = (cx+r , cy+r)
    return (x0, y0, x1, y1)

def getWallHit(data):
    # return wall that player is currently hitting
    # note: this should be optimized to only check the walls that are visible
    # or even just directly compute the wall without a loop
    playerBounds = getPlayerBounds(data)
    for wall in range(data.walls):
        if data.wallPoints[wall] != None:
            wallBounds = getWallBounds(wall, data)
            if (boundsIntersect(playerBounds, wallBounds) == True):
                data.speed = 0
                data.jumpStep = 0
                data.isDoingJump = False
                data.playerY = 0
                data.playerX = wallBounds[0] - data.playerWidth
                return wall
    return -1

def getBalloonHitWall(balloon, data):
    balloonBounds = getBalloonBounds(balloon, data)
    for wall in range(data.walls):
        if data.wallPoints[wall] != None:
            wallBounds = getWallBounds(wall, data)
            if (boundsIntersect(balloonBounds, wallBounds) == True):
                return wall
    return -1

def boundsIntersect(boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def movePlayer(dx, dy, data):
    data.playerX += dx
    data.playerY += dy
    # scroll to make player visible as needed
    if (data.playerX < data.scrollX + data.scrollMargin):
        data.scrollX = data.playerX - data.scrollMargin
    if (data.playerX > data.scrollX + data.width - data.scrollMargin):
        data.scrollX = data.playerX - data.width + data.scrollMargin
    # and check for a new wall hit
    wall = getWallHit(data)
    if (wall != data.currentWallHit):
        data.currentWallHit = wall
        if (wall >= 0) and data.wallPoints[wall] > 0:
            data.wallPoints[wall] -= 1
    # check if jump over a wall
    for wallNum in range(data.walls):
        if data.wallPoints[wallNum] != None:
            playerBounds = getPlayerBounds(data)
            wallBounds = getWallBounds(wallNum,data)
            if ((playerBounds[0] >= wallBounds[2]) ==
                (playerBounds[0] -dx < wallBounds[2])):
                data.wallPoints[wallNum] += 1

def moveBalloons(data):
    #move the balloons
    if data.balloons != []:
        i = 0
        while i < len(data.balloons):
            (x0, y0 ,speed) = data.balloons[i]
            x0 += speed * data.deltaSpeed
            data.balloons[i] = (x0, y0 ,speed)
            if x0 >= data.width + data.scrollX:
                data.balloons.pop(i)
            else:
                i += 1
    #check if hit the wall
    j = 0
    while j < len(data.balloons):
        wall = getBalloonHitWall(j,data)
        if wall != -1:
            data.wallPoints[wall] = None
            data.balloons.pop(j)
        else:
            j += 1

def createOneBalloon(data):
    def deAlias(a):
        return a
    playerBounds = getPlayerBounds(data)
    if data.speed >= 0:
        speed = data.balloonInitSpeed + deAlias(data.speed)
        x0 = playerBounds[2]
    else:
        speed = -data.balloonInitSpeed + deAlias(data.speed)
        x0 = playerBounds[0]
    data.balloons.append((x0,playerBounds[1] + data.eyeposition,speed))

def doJump(data):
    jumpHeightList = [data.wallHeight/1, data.wallHeight/1,
                      data.wallHeight/4, data.wallHeight/4,
                      data.wallHeight/8,                 0,
                                      0,-data.wallHeight/8,
                     -data.wallHeight/4,-data.wallHeight/4,
                     -data.wallHeight/1,-data.wallHeight/1]
    return jumpHeightList[data.jumpStep]

def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            canvas.create_rectangle(x0, y0, x1, y1, fill="white")

def drawSnake(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] > 0: 
                (x0, y0, x1, y1) = getCellBounds(row, col, data)
                canvas.create_oval(x0, y0, x1, y1, fill="blue")

def drawFood(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == -1: 
                (x0, y0, x1, y1) = getCellBounds(row, col, data)
                canvas.create_oval(x0, y0, x1, y1, fill="green")

def drawGameOver(canvas, data):
    if (data.gameOver):
        canvas.create_text(data.width/2, data.height/2, text="Game over!",
                           font="Arial 26 bold")

def redrawAll(canvas, data):
    if data.mode == 1:
        redrawAll1(canvas, data)
    elif data.mode == 2:
        redrawAll2(canvas, data)
    elif data.mode == 3:
        redrawAll3(canvas, data)
    elif data.mode == 4:
        redrawAll4(canvas, data)
    elif data.mode == 0:
        redrawAll0(canvas, data)

def redrawAll0(canvas, data):
    msg1 = "Press 1 to play drawCirclePattern"
    msg2 = "Press 2 to play drawSpiral"
    msg3 = "Press 3 to play adaptedSnake"
    msg4 = "Press 4 to play betterSideScroller"
    msg5 = "Press Escape to return to main screen"
    canvas.create_text(data.width/2, data.height*1/6, \
                       text=msg1 ,font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height*2/6, \
                       text=msg2 ,font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height*3/6, \
                       text=msg3 ,font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height*4/6, \
                       text=msg4 ,font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height*5/6, \
                       text=msg5 ,font = "Arial 15 bold")
    canvas.create_text(data.width*8/10, data.height*1/20, \
                       text='Hanzhou Lu/hanzhoul' ,font = "Arial 15 bold") 
    canvas.create_text(data.width*8/10, data.height*2/20, \
                       text='15112 hw7' ,font = "Arial 15 bold") 

def redrawAll1(canvas, data):
    data.marginX = (data.width - data.patternRows*data.patterDiameter)/2
    data.marginY = (data.height - data.patternCols*data.patterDiameter)/2
    canvas.create_rectangle(data.marginX,
                            data.marginY,
                            data.width - data.marginX,
                            data.height - data.marginY,
                            fill=data.blackgroundColor)
    colorBox = decidePatternColor(data)
    for row in range(data.patternRows):
        for col in range(data.patternCols):
            color = colorBox[row][col]
            drawSinglePattern(canvas,row,col,color,data)

def redrawAll2(canvas,data):
    originAngle = calculateOriginAngle(data)
    colorList = dicideColor()
    for i in range(0,32):
        color = colorList[i]
        drawSingleCircle(canvas,data,color,i,originAngle)

def redrawAll3(canvas, data):
    drawBoard(canvas, data)
    drawSnake(canvas, data)
    drawFood(canvas, data)
    drawGameOver(canvas, data)

def redrawAll4(canvas, data):
    # draw the base line
    lineY = data.height/2
    lineHeight = 5
    canvas.create_rectangle(0, lineY, data.width, lineY+lineHeight,fill="black")

    # draw the walls
    # (Note: should optimize to only consider walls that can be visible now!)
    sx = data.scrollX
    for wall in range(data.walls):
        if data.wallPoints[wall]!=None:
            (x0, y0, x1, y1) = getWallBounds(wall, data)
            fill = "orange" if (wall == data.currentWallHit) else "pink"
            canvas.create_rectangle(x0-sx, y0, x1-sx, y1, fill=fill)
            (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
            canvas.create_text(cx, cy, text=str(data.wallPoints[wall]))
            cy = lineY + 5
            canvas.create_text(cx, cy, text=str(wall), anchor=N)

    # draw the player
    (x0, y0, x1, y1) = getPlayerBounds(data)
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill="cyan")

    # draw the balloons
    for i in range(len(data.balloons)):
        (bx0, by0 ,bspeed) = data.balloons[i]
        bx0 = bx0 - data.scrollX
        (bx, by) = (data.balloonsRadios, data.balloonsRadios)
        canvas.create_oval(bx0 - bx, by0 - by,
                           bx0 + bx, by0 + by, fill="blue")

    # draw the instructions
    msg = "Use arrows to move, hit walls to score"
    canvas.create_text(data.width/2, 20, text=msg)    

def keyPressed(event, data, canvas):
    if event.keysym == "Escape":
        data.mode = 0
    if data.mode == 1:
        keyPressed1(event, data)
    elif data.mode == 2:
        keyPressed2(event, data)
    elif data.mode == 3:
        keyPressed3(event, data)
    elif data.mode == 4:
        keyPressed4(event, data)
    elif data.mode == 0:
        if   (event.keysym == "1"):  data.mode = 1
        elif (event.keysym == "2"):  data.mode = 2
        elif (event.keysym == "3"):  data.mode = 3
        elif (event.keysym == "4"):  data.mode = 4
        init(data)
    redrawAll(canvas, data)

def keyPressed1(event, data):
    if (event.keysym == "Up"):
        data.patternRows += 1
        data.patternCols += 1
    if (event.keysym == "Down"):
        if data.patternRows == 1:
            pass
        else:
            data.patternRows -= 1
            data.patternCols -= 1

def keyPressed2(event, data):
    if (event.keysym == "Up"):
        data.largestR *= 1.1
        data.cirleRadios *= 1.1
    if (event.keysym == "Down"):
        data.largestR = data.largestR*10/11
        data.cirleRadios = data.cirleRadios*10/11

def keyPressed3(event, data):
    if (event.keysym == "p"): data.paused = True; return
    elif (event.keysym == "r"): init(data); return
    if (data.paused or data.gameOver): return
    if (event.keysym == "Up"):      data.direction = (-1, 0)
    elif (event.keysym == "Down"):  data.direction = (+1, 0)
    elif (event.keysym == "Left"):  data.direction = (0, -1)
    elif (event.keysym == "Right"): data.direction = (0, +1)

def keyPressed4(event, data):
    if   (event.keysym == "Left"):  data.speed -= 1
    elif (event.keysym == "Right"): data.speed += 1
    elif (event.keysym == "Up"):
        data.isDoingJump = True
    elif (event.keysym == "Down"):  movePlayer(0, -data.deltaSpeed, data)
    elif (event.char   == "t"):
        createOneBalloon(data)

def mousePressed(event, data):
    if data.mode == 1:
        pass
    elif data.mode == 2:
        pass
    elif data.mode == 3:
        data.paused = False
    elif data.mode == 4:
        pass

def timerFired(data):
    if data.mode == 1:
        pass
    elif data.mode == 2:
        pass
    elif data.mode == 3:
        if (data.paused or data.gameOver): return
        takeStep(data)
    elif data.mode == 4:
        timerFired4(data)

def timerFired4(data):
    #Do vertical move
    if data.isDoingJump == True:
        if data.jumpStep == 12:               #Jumping procedure have 12 steps
            data.isDoingJump = False 
            data.jumpStep = 0
        else:
            movePlayer(0 ,doJump(data),data)
            data.jumpStep = data.jumpStep + 1
    #Do horizontal move
    movePlayer(data.deltaSpeed*data.speed,0,data)
    #Throw balloons
    moveBalloons(data)

def mainWindow(width=300, height=300):

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, canvas)
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
    data.timerDelay1 = 100
    data.mode = 0
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

mainWindow(600,600)