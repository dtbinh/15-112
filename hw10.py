# hw10.py
# Hanzhou Lu / hanzhoul / II

import copy
def computeDimension(area):
    result = []
    for height in range(1, area + 1):
        width = area // height
        if width * height == area:
            result.append((height, width))
    return result

def isLegal(startR, startC, width, height, rectBoard):
    row = len(rectBoard)
    col = len(rectBoard[0])
    if startR < 0            or startC < 0 or\
       startR + height > row or startC + width > col:
        return False
    else:
        for rows in range(startR, startR + height):
            for cols in range(startC, startC + width):
                if rectBoard[rows][cols] != 0:
                    return False
    return True

def modifyRectBoard(startR, startC, width, height, rectBoard):
    for row in range(startR, startR + height):
        for col in range(startC, startC + width):
            rectBoard[row][col] = 1

def solveRectangula(board):
    intPositions = []
    rectBoard = []
    solution = []
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] != 0:
                intPositions.append((row, col, board[row][col]))
    for i in range(rows):
        rectBoard.append([0] * cols)
    def addRectangula(intPositions, rectBoard):
        nonlocal solution
        if intPositions == []:
            return True
        else:
            rect = intPositions[0]
            rectRow = rect[0]
            rectCol = rect[1]
            rectArea = rect[2]
            possibleDimension = computeDimension(rectArea)
            for dimension in possibleDimension:
                height = dimension[0]
                width = dimension[1]
                for startR in range(rectRow - height + 1, rectRow + 1):
                    for startC in range(rectCol - width + 1, rectCol + 1):
                        if isLegal(startR, startC, width, height, rectBoard):
                            tempBorad = copy.deepcopy(rectBoard)
                            modifyRectBoard(startR, startC, 
                                             width, height, rectBoard)
                            result = addRectangula(intPositions[1:], rectBoard)
                            if result == True:
                                solution.append((startR,startC,width,height))
                                return result
                            else: 
                                rectBoard = copy.deepcopy(tempBorad)
            return None
    addRectangula(intPositions, rectBoard)
    if solution != []:
        return solution
    else: return None

###############################################
# ignore_rest
###############################################

# Place these imports in hw10.py below the ignore_rest line!

from hw10_rectangula_tester import testSolveRectangula
from hw10_rectangula_tester import playRectangula

testSolveRectangula(solveRectangula)
playRectangula(solveRectangula)

from tkinter import *
class SpaceShip(object):
    def __init__(self, data):
        self.width = 20
        self.height = 10
        self.x = 100
        self.y = data.height - 50
        self.life = 5
        self.fireSpeed = 15

    def fire(self, data):
        if data.step % 4 == 0:
            data.fireBullet.append([self.x, self.y])
        for i in range(len(data.fireBullet)):
            data.fireBullet[i][1] -= self.fireSpeed

class Monster1(object):
    def __init__(self, location):
        self.y = 50
        self.life = 1
        self.color = 'cyan'
        self.size = 5
        self.location = location
        self.speed = 20

    def makeMove(self, direction):
        self.location += direction * self.speed

    def launchBullet(self, data):
        if data.step % 20 == 0 and self.life > 0:
            data.monsterBullet.append([self.location, self.y])

class Monster2(Monster1):
    def __init__(self, location):
        super().__init__(location)
        self.y = 100
        self.color = 'purple'
        self.size = 10
        self.life = 2

class Monster3(Monster1):
    def __init__(self, location):
        super().__init__(location)
        self.y = 150
        self.color = 'yellow'
        self.size = 10
        self.life = 2

class UFO(Monster1):
    def __init__(self, location):
        super().__init__(location)
        self.y = 25
        self.color = '#66CCFF'
        self.size = 10
        self.life = 1
        self.speed = 25  

class Shield(object):
    def __init__(self, data, location):
        self.location = location
        self.y = data.height - 150
        self.width = data.width / 10
        self.height = data.width / 20
        self.life = 25
        self.color = 'red'
    
class OopyInvaders(object):
    totalGamesPlayed = 0
    def __init__(self):
        self.score = 0
        OopyInvaders.totalGamesPlayed += 1

    def init(self, data):
        data.step = 0
        data.ufoStep = 0
        data.bulletSize = 5
        data.moveDelay = 20
        data.monsterList = []
        data.spaceShip = SpaceShip(data)
        data.fireBullet = []
        data.monsterBullet = []
        data.shieldList = []
        data.gameover = False
        data.lifeBarWidth = 20
        data.lifeBarHeight = 5
        data.margin = 20
        data.shipSpeed = 5
        data.monsterFireSpeed = 50
        for i in range(10):
            data.monsterList.append(Monster1(i*data.width/10 + data.width/20)) 
        for j in range(10):
            data.monsterList.append(Monster2(j*data.width/10 + data.width/20))
        for k in range(10):
            data.monsterList.append(Monster3(k*data.width/10 + data.width/20))
        for l in range(5):
            data.shieldList.append(Shield(data,l*data.width/5+ data.width/10))
        data.monsterList.append(UFO(i*data.width/10 + data.width/20))

    def checkIfHitMonster(self, data):
        for bullet in data.fireBullet:
            for monster in data.monsterList:
                if monster.location - monster.size <= bullet[0]\
                <= monster.location + monster.size and \
                   monster.y - monster.size <= bullet[1]\
                <= monster.y + monster.size and monster.life > 0:
                    monster.life -= 1
                    self.score += 1
                    data.fireBullet.pop(data.fireBullet.index(bullet))
            for shield in data.shieldList:
                if shield.location - shield.width/2 <= bullet[0]\
                <= shield.location + shield.width/2 and\
                   shield.y - shield.height/2 <= bullet[1]\
                <= shield.y and shield.life > 0:
                    shield.life -= 1
                    data.fireBullet.pop(data.fireBullet.index(bullet))
        index = 0
        while index < len(data.monsterBullet):
            monsterBullet = data.monsterBullet[index]
            for shield in data.shieldList:
                if shield.location - shield.width/2 <= monsterBullet[0]\
                <= shield.location + shield.width/2 and\
                   shield.y - shield.height/2 <= monsterBullet[1]\
                <= shield.y and shield.life > 0:
                    shield.life -= 1
                    Num = data.monsterBullet.index(monsterBullet)
                    data.monsterBullet.pop(Num)
                    index -= 1
            if data.spaceShip.x - data.spaceShip.width/2 <= monsterBullet[0] \
            <= data.spaceShip.x + data.spaceShip.width/2 and\
               data.spaceShip.y - data.spaceShip.height/2 <= monsterBullet[1]\
            <= data.spaceShip.y + data.spaceShip.height/2:
                data.spaceShip.life -= 1
                if data.spaceShip.life < 1: data.gameover = True
            index += 1
    
    def monsterFire(self, data):
        for monster in data.monsterList:
            if type(monster) == Monster1 or type(monster) == UFO:
                monster.launchBullet(data)
        for i in range(len(data.monsterBullet)):
            data.monsterBullet[i][1] += data.monsterFireSpeed

    def changeColor(self, data):
        for shield in data.shieldList:
            ri = int(255 * shield.life / 25)
            shield.color = '#%02x%02x%02x' % (ri,  0,  0)

    def drawBackground(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = 'black')

    def drawMonster(self, canvas, data):
        for monster in data.monsterList:
            if monster.life > 0:
                canvas.create_oval(monster.location - monster.size,
                                   monster.y - monster.size, 
                                   monster.location + monster.size,
                                   monster.y + monster.size, 
                                   fill = monster.color)

    def drawSpaceShip(self, canvas, data):
        canvas.create_rectangle(data.spaceShip.x - data.spaceShip.width  / 2,
                                data.spaceShip.y - data.spaceShip.height / 2,
                                data.spaceShip.x + data.spaceShip.width  / 2,
                                data.spaceShip.y + data.spaceShip.height / 2,
                                fill = '#66CCFF')

    def drawBullet(self, canvas, data):
        for bullet in data.fireBullet:
            canvas.create_oval(bullet[0] - data.bulletSize,
                               bullet[1] - data.bulletSize,
                               bullet[0] + data.bulletSize,
                               bullet[1] + data.bulletSize, fill = 'white')
        for monsterBullet in data.monsterBullet:
            canvas.create_oval(monsterBullet[0] - data.bulletSize,
                               monsterBullet[1] - data.bulletSize,
                               monsterBullet[0] + data.bulletSize,
                               monsterBullet[1] + data.bulletSize,
                               fill = 'grey')

    def drawShield(self, canvas, data):
        for shield in data.shieldList:
            if shield.life > 0:
                canvas.create_arc(shield.location - shield.width /2,
                                  shield.y        - shield.height/2,
                                  shield.location + shield.width /2,
                                  shield.y        + shield.height/2,
                                  start = 0, extent = 180, fill = shield.color)
    
    def drawGameover(self, canvas, data):
        canvas.create_text(data.width/2, data.height/2, text="Game over!",
                           font="Arial 26 bold", fill = 'white')

    def drawScore(self, canvas, data):
        canvas.create_text(data.width, data.height, 
                           text="Score:" + str(self.score),
                           anchor = 'se', font="Arial 16", fill = 'white')
    
    def drawLife(self, canvas, data):
        for i in range(data.spaceShip.life):
            canvas.create_rectangle(i * data.lifeBarWidth + data.margin * 4,
                                data.height - data.margin - data.lifeBarHeight,
                                (i + 1) * data.lifeBarWidth + data.margin*4,
                                data.height - data.margin, fill = 'cyan')
        canvas.create_text(data.margin, 
                           data.height - data.margin - data.lifeBarHeight/2,
                           anchor = 'w', text = 'Energy:', fill = 'white',
                           font="Arial 12")

    def moveAllMonster(self, data):
        data.ufoStep = (data.ufoStep + 1) % (data.moveDelay * 2)
        data.step = (data.step + 1) % data.moveDelay
        for monster in data.monsterList[:-1]:
            if data.step == 0:
                monster.makeMove(1)
            if data.step == data.moveDelay / 2:
                monster.makeMove(-1)
        ufo = data.monsterList[-1]
        if data.ufoStep < data.moveDelay:
            ufo.makeMove(-1)
        else:
            ufo.makeMove(1)

    def redrawAll(self, canvas, data):
        self.drawBackground(canvas, data)
        self.drawMonster(canvas, data)
        self.drawSpaceShip(canvas, data)
        self.drawBullet(canvas, data)
        self.drawShield(canvas, data)
        self.drawScore(canvas, data)
        self.drawLife(canvas,data)
        if data.gameover == True:
            self.drawGameover(canvas, data)

    def mousePressed(self, event, data):
        pass

    def keyPressed(self, event, data):
        if data.spaceShip.x <= data.width - data.spaceShip.width:
            if (event.keysym == "Right"): data.spaceShip.x += data.shipSpeed
            elif (event.keysym == "Down"):  data.spaceShip.x += data.shipSpeed
        if data.spaceShip.x >= data.spaceShip.width:
            if (event.keysym == "Up"):      data.spaceShip.x -= data.shipSpeed
            elif (event.keysym == "Left"):  data.spaceShip.x -= data.shipSpeed
            

    def timerFired(self, data):
        if data.gameover == True:
            return
        else:
            self.moveAllMonster(data)
            self.monsterFire(data)
            data.spaceShip.fire(data)
            self.checkIfHitMonster(data)
            self.changeColor(data)

    def getFinalScore(self):
        return self.score

    def run(self, width=600, height=500):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            self.redrawAll(canvas, data)
            canvas.update()    

        def mousePressedWrapper(event, canvas, data):
            self.mousePressed(event, data)
            redrawAllWrapper(canvas, data)

        def keyPressedWrapper(event, canvas, data):
            self.keyPressed(event, data)
            redrawAllWrapper(canvas, data)

        def timerFiredWrapper(canvas, data):
            self.timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 100 # milliseconds
        self.init(data)
        # create the root and the canvas
        root = Tk()
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



game1 = OopyInvaders()
game1.run()
print(game1.getFinalScore())

game2 = OopyInvaders()
game2.run()
print(game2.getFinalScore())

assert(OopyInvaders.totalGamesPlayed == 2)