import math
import operator
import numpy as np
from tkinter import *
import winsound
import time

def startSound(filename, async=True, loop=True):  #cited from 15-112 S-15
    flags = winsound.SND_FILENAME
    if (async == True): flags |= winsound.SND_ASYNC
    if (loop == True):  flags |= winsound.SND_LOOP
    winsound.PlaySound(filename, flags)

def stopSound():
    winsound.PlaySound(None, 0)

class Cube(object):
    def __init__(self, style):
        self.style = style
        if style == 'hill':
            self.color = ['green','lime green','green yellow']
        elif style == 'water':
            self.color = ['royal blue', 'dodger blue', 'deep sky blue']
        elif style == 'title':
            self.color = ['red', 'yellow', 'orange']

class Node(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.connection = []
        self.switchOn = False

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def connectTo(self, other, material):
        self.connection.append([other, material])

    def addToStiffnessMatrix(self, data):
        node1 = data.nodeList.index(self) * 2
        for nextNode in self.connection:
            other = nextNode[0]
            AE = nextNode[1]
            node2 = data.nodeList.index(other) * 2
            deltaX = other.x - self.x
            deltaY = other.y - self.y
            l = (deltaX ** 2 + deltaY ** 2) ** .5
            k = AE / l
            s = deltaY / l
            c = deltaX / l
            k1 = round(k * c ** 2, 4)
            k2 = round(k * c * s , 4)
            k3 = round(k * s ** 2, 4)
            data.stiffnessMatrix[node1     ][node1     ] += k1
            data.stiffnessMatrix[node1     ][node1 + 1 ] += k2
            data.stiffnessMatrix[node1 + 1 ][node1     ] += k2
            data.stiffnessMatrix[node1 + 1 ][node1 + 1 ] += k3
            data.stiffnessMatrix[node2     ][node1     ] -= k1
            data.stiffnessMatrix[node2     ][node1 + 1 ] -= k2
            data.stiffnessMatrix[node2 + 1 ][node1     ] -= k2
            data.stiffnessMatrix[node2 + 1 ][node1 + 1 ] -= k3
            data.stiffnessMatrix[node1     ][node2     ] -= k1
            data.stiffnessMatrix[node1     ][node2 + 1 ] -= k2
            data.stiffnessMatrix[node1 + 1 ][node2     ] -= k2
            data.stiffnessMatrix[node1 + 1 ][node2 + 1 ] -= k3
            data.stiffnessMatrix[node2     ][node2     ] += k1
            data.stiffnessMatrix[node2     ][node2 + 1 ] += k2
            data.stiffnessMatrix[node2 + 1 ][node2     ] += k2
            data.stiffnessMatrix[node2 + 1 ][node2 + 1 ] += k3

def init(data):
    data.margin = 20
    data.toolBoxWidth = 100
    data.toolBoxHeight = 180
    data.barForceHeight = 550
    data.barForceLeftMargin = 325
    data.barForceWidth = 15
    data.progressBarWidth = 150
    data.progressBarHeight = 20
    data.resultBarMarginL = 280
    data.resultBarMarginU = 340
    data.isPlayingBGM = True
    data.deepth = 3
    data.row = 20
    data.col = 60
    data.pace = 0
    data.theta0 = math.pi / 2
    data.deltaTheta = math.pi / 90
    data.theta  = data.theta0 - math.pi / 2
    data.sinTheta = math.sin(data.theta)
    data.cosTheta = math.cos(data.theta)
    data.pixelLength = 12
    data.width1 = round(data.pixelLength * data.cosTheta, 4)
    data.width2 = round(data.pixelLength * data.sinTheta, 4)
    data.x0 = data.width  / 2
    data.y0 = data.height / 2
    data.x12 = data.width1 * (12 - data.col/2) + data.x0 + data.width2 * 4
    data.y12 = data.pixelLength * (12 - data.row/2) + data.y0 + \
               data.width2 * (12 - data.col/2) - data.width1 * 4
    data.dotR = 5
    data.carNameList = ['Anonymous', 'Tank     ', 'F1       ',
                        'Bus      ', 'UFO      ']
    data.carName = data.carNameList[data.carNum]
    data.carWeightList = [40, 80, 30, 60, 100]
    data.carWeight = data.carWeightList[data.carNum]
    data.carSize = 0.5
    data.carX = 9
    data.carSpeed = 1/4
    data.barSize = data.pixelLength / 2
    data.barForceList = []
    data.largestBarForce = []
    data.board = []
    data.nodeList = [Node(0, 0, data), Node( 36, 0, data)]
    data.stiffnessMatrix = []
    data.deflMatrix = [0] * 50
    data.currMaterial = 0 
    # 0 = wood1, 1 = wood2, 2 = wood3, 3 = iron, 4 = Pittsburgh Steel
    data.materialColor = [['BurlyWood2'     , 'BurlyWood3'     ],
                          ['Wheat3'         , 'Wheat4'         ],
                          ['Tan3'           , 'Tan4'           ],
                          ['SlateGray2'     , 'SlateGray3'     ],
                          ['LightSteelBlue3', 'LightSteelBlue4']]
    data.AE = [50, 75, 100, 150, 300]
    data.maxForceRatio = 6
    data.isPlacingBar = False
    data.isRemovingBar = False
    for d in range(data.deepth):
        data.board.append([])
        for r in range(data.row):
            data.board[d].append([])
            for c in range(data.col):
                data.board[d][r].append(None)
    data.board[0][19][0] = Cube('hill')
    for i in range(data.deepth):
        for j in range(data.row):
            for k in range(j):
                l = data.col - k -1
                if not ((7 <= j <= 11) and (i == 1)):
                    data.board[i][j][k] = data.board[0][19][0]
                    data.board[i][j][l] = data.board[0][19][0]
    data.board[0][19][30] = Cube('water')
    for i in range(data.deepth):
        for j in range(data.row):
            for k in range(data.col):
                if (k >= j and k + j < 60):
                    if j >= 16:
                        data.board[i][j][k] = data.board[0][19][30]
                    if j == 15 and k % 4 == 0:
                        data.board[i][j][k] = data.board[0][19][30]
                    if j == 16 and (k+2) % 4 == 0:
                        data.board[i][j][k] = None
    backgroundColor(data)
    #start interface
    if data.gameMode == 'start':
        titleBoard = \
        [[0,0,0,1,1,1,1,0,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,0,1,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1],
         [1,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
         [1,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0],
         [1,1,1,1,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,0],
         [1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,0,0,0],
         [1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0],
         [1,1,1,1,0,0,1,0,0,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1]]
        for row in range(len(titleBoard)):
            for col in range(len(titleBoard[0])):
                if titleBoard[row][col] == 1:
                    data.board[1][row][13 + col] = Cube('title')

def bridgeDemo(data):
    data.nodeList = [Node(0, 0, data), Node( 36, 0, data)]    #0, 1
    data.nodeList.append(Node(10,  0, data))                  #2
    data.nodeList.append(Node(18,  0, data))                  #3
    data.nodeList.append(Node(26,  0, data))                  #4
    data.nodeList.append(Node(10, 10, data))                  #5
    data.nodeList.append(Node(18, 10, data))                  #6
    data.nodeList.append(Node(26, 10, data))                  #7
    for i in range(len(data.nodeList) * 2):
        data.stiffnessMatrix.append([0] * (len(data.nodeList) * 2))
    data.nodeList[0].connectTo(data.nodeList[2], data.AE[1])
    data.nodeList[0].connectTo(data.nodeList[5], data.AE[1])
    data.nodeList[2].connectTo(data.nodeList[5], data.AE[1])
    data.nodeList[2].connectTo(data.nodeList[3], data.AE[1])
    data.nodeList[5].connectTo(data.nodeList[3], data.AE[1])
    data.nodeList[5].connectTo(data.nodeList[6], data.AE[1])
    data.nodeList[6].connectTo(data.nodeList[3], data.AE[1])
    data.nodeList[6].connectTo(data.nodeList[7], data.AE[1])
    data.nodeList[3].connectTo(data.nodeList[7], data.AE[1])
    data.nodeList[3].connectTo(data.nodeList[4], data.AE[1])
    data.nodeList[4].connectTo(data.nodeList[7], data.AE[1])
    data.nodeList[4].connectTo(data.nodeList[1], data.AE[1])
    data.nodeList[7].connectTo(data.nodeList[1], data.AE[1])
    for node in data.nodeList:
        node.addToStiffnessMatrix(data)


def drawAllCube(canvas,data):
    if data.theta0 >= math.pi / 2:                    #look from right side
        for index1 in range(data.row):                #from bottom to top
            row = data.row - 1 - index1
            for col in range(data.col):               #from left to right
                for index2 in range(data.deepth):
                    deepth = data.deepth - 1 - index2 #from back to front
                    if data.board[deepth][row][col] != None:
                        color = data.board[deepth][row][col].color
                        drawSingleCubeR(canvas, data, row, col, deepth, color)
    if data.theta0 < math.pi / 2:                     #look from left side
        for index1 in range(data.row):                #from bottom to top
            row = data.row - 1 - index1
            for index2 in range(data.col):            #from right to left
                col = data.col - 1 - index2
                for index3 in range(data.deepth):     #from back to front
                    deepth = data.deepth - 1 - index3
                    if data.board[deepth][row][col] != None:
                        color = data.board[deepth][row][col].color
                        drawSingleCubeL(canvas, data, row, col, deepth, color)

def drawSingleCubeR(canvas, data, row, col, deepth, color):
    draw = [0, 0, 0]
    #drawFront
    if deepth == 0 or data.board[deepth - 1][row][col] == None:
        draw[0] = 1
    #drawRight
    if col == data.col - 1 or data.board[deepth][row][col + 1] == None:
        draw[1] = 1
    #drawTop
    if row == 0 or data.board[deepth][row - 1][col] == None:
        draw[2] = 1
    if draw == [0, 0, 0]: return
    x0 = data.width2 * (4 * deepth) + \
         data.width1 * (col - data.col/2) + data.x0
    y0 = data.pixelLength * (row - data.row/2) + data.y0 + \
         data.width2 * (col - data.col/2) - data.width1 * 4 * deepth
    height = data.pixelLength
    width1 = data.width1
    width2 = data.width2
    if draw[0] == 1:        #drawFront
        canvas.create_polygon(x0         , y0                   ,\
                              x0 + width1, y0 + width2          ,\
                              x0 + width1, y0 + height + width2 ,\
                              x0         , y0 + height          ,\
                              fill = color[0])
    if draw[1] == 1:        #drawRight
        canvas.create_polygon(x0+width1         , y0+width2                ,\
                              x0+width1+4*width2, y0+width2-4*width1       ,\
                              x0+width1+4*width2, y0+width2-4*width1+height,\
                              x0+width1         , y0+width2+height         ,\
                              fill = color[1])
    if draw[2] == 1:        #drawTop
        canvas.create_polygon(x0                    , y0                    ,\
                              x0 + width1           , y0 + width2           ,\
                              x0 + width1 + 4*width2, y0 + width2 - 4*width1,\
                              x0 +          4*width2, y0          - 4*width1,\
                              fill = color[2])

def drawSingleCubeL(canvas, data, row, col, deepth, color):
    draw = [0, 0, 0]
    if col == 0 or data.board[deepth][row][col - 1] == None:         #drawLeft
        draw[0] = 1
    if deepth == 0 or data.board[deepth - 1][row][col] == None:      #drawFront
        draw[1] = 1
    if row == 0 or data.board[deepth][row - 1][col] == None:         #drawTop
        draw[2] = 1
    if draw == [0, 0, 0]: return
    x0 = data.width2 * (4 * deepth) + \
         data.width1 * (col - data.col/2) + data.x0
    y0 = data.pixelLength * (row - data.row/2) + data.y0 + \
         data.width2 * (col - data.col/2) - data.width1 * 4 * deepth
    height = data.pixelLength
    width1 = data.width1
    width2 = data.width2
    if draw[0] == 1:          #drawLeft
        canvas.create_polygon(x0             , y0                      ,\
                              x0 + 4 * width2, y0 - 4 * width1         ,\
                              x0 + 4 * width2, y0 + height - 4 * width1,\
                              x0             , y0 + height             ,\
                              fill = color[1])
    if draw[1] == 1:          #drawFront
        canvas.create_polygon(x0         , y0                   ,\
                              x0 + width1, y0 + width2          ,\
                              x0 + width1, y0 + height + width2 ,\
                              x0         , y0 + height          ,\
                              fill = color[0])
    if draw[2] == 1:          #drawTop
        canvas.create_polygon(x0                    , y0                    ,\
                              x0 + width1           , y0 + width2           ,\
                              x0 + width1 + 4*width2, y0 + width2 - 4*width1,\
                              x0 +          4*width2, y0          - 4*width1,\
                              fill = color[2])

def moveWave(data):
    data.pace += 1
    for i in range(data.deepth):
        for j in range(data.row):
            for k in range(data.col):
                if (k >= j and k + j < 60):
                    if j >= 16:
                        data.board[i][j][k] = data.board[0][19][30]
                    if j == 15:
                        if (k + data.pace) % 4 == 0:
                            data.board[i][j][k] = data.board[0][19][30]
                        else:
                            data.board[i][j][k] = None
                    if j == 16 and (k + 2 + data.pace) % 4 == 0:
                        data.board[i][j][k] = None

def calculateDefl(data):
    nodeMap = dict()
    data.forceMat = [0] * (len(data.nodeList) * 2)
    if data.carX <= 11:
        data.deflMatrix = [0] * (len(data.nodeList) * 2)
    else:
        for node in data.nodeList:
            if node.y == 0:
                nodeMap[node.x + 11] = data.nodeList.index(node)
        sortedMap = sorted(nodeMap.items(), key = operator.itemgetter(0))
        data.sortedMap = sortedMap
        for i in range(len(sortedMap) - 1):
            if sortedMap[i][0] < data.carX <= sortedMap[i + 1][0]:
                length = - sortedMap[i][0] + sortedMap[i + 1][0]
                data.forceMat[sortedMap[i    ][1] * 2 + 1] -= \
                data.carWeight * (sortedMap[i + 1][0] - data.carX) / length
                data.forceMat[sortedMap[i + 1][1] * 2 + 1] -= \
                data.carWeight * (data.carX - sortedMap[i][0]) / length
        mat = []
        for i in range(4, len(data.nodeList) * 2):
            mat.append(data.stiffnessMatrix[i][4:])

        stiffnessMatrix = np.mat(mat)
        forceMatrix = np.mat(data.forceMat[4:])
        forceMatrix = forceMatrix.reshape((len(mat),1))

        deflMatrix = np.linalg.solve(stiffnessMatrix,forceMatrix)
        data.deflMatrix = [0] * 4 + list(np.array(deflMatrix).reshape(-1,))
        for i in range(len(data.deflMatrix)):
            data.deflMatrix[i] = round(data.deflMatrix[i], 4)

def calculateBarForce(data):
    data.barForceList = []
    for node1 in data.nodeList:
        for nextNode in node1.connection:
            node2 = nextNode[0]
            index1 = data.nodeList.index(node1)
            index2 = data.nodeList.index(node2)
            i1 = index1 * 2
            i2 = index1 * 2 + 1
            i3 = index2 * 2
            i4 = index2 * 2 + 1
            barStiffnessMat = \
            [[data.stiffnessMatrix[i1][i1], data.stiffnessMatrix[i1][i2],
              data.stiffnessMatrix[i1][i3], data.stiffnessMatrix[i1][i4]],
             [data.stiffnessMatrix[i2][i1], data.stiffnessMatrix[i2][i2],
              data.stiffnessMatrix[i2][i3], data.stiffnessMatrix[i2][i4]],
             [data.stiffnessMatrix[i3][i1], data.stiffnessMatrix[i3][i2],
              data.stiffnessMatrix[i3][i3], data.stiffnessMatrix[i3][i4]],
             [data.stiffnessMatrix[i4][i1], data.stiffnessMatrix[i4][i2],
              data.stiffnessMatrix[i4][i3], data.stiffnessMatrix[i4][i4]]]
            barDeflMat = [[data.deflMatrix[i1]], [data.deflMatrix[i2]],
                          [data.deflMatrix[i3]], [data.deflMatrix[i4]]]
            barDeflMat = np.mat(barDeflMat)
            barForceMat = barStiffnessMat * barDeflMat
            barForce = list(np.array(barForceMat).reshape(-1,))
            barForce = (barForce[0] ** 2 + barForce[1] ** 2) ** 0.5
            barForce = round(barForce, 2)
            data.barForceList.append((barForce, nextNode[1],
                                      min(node1.x, node2.x), node1, node2))
    if data.largestBarForce == []:
        for i in range(len(data.barForceList)):
            data.largestBarForce.append(data.barForceList[i][0])
    else:
        for j in range(len(data.barForceList)):
            data.largestBarForce[j] = max(data.largestBarForce[j], 
                                          data.barForceList[j][0])

def textColor(barForce, maxForce):
    (r0, g0, b0) = (0  , 204,   0)            #which is green
    (r1, g1, b1) = (255,   0,   0)            #which is red
    ratio = barForce / maxForce if barForce <= maxForce else 1
    ri = int((r1 - r0) * ratio + r0)
    gi = int((g1 - g0) * ratio + g0)
    bi = int((b1 - b0) * ratio + b0)
    color = '#%02x%02x%02x' % (ri, gi, bi)
    return color

def drawDeck(canvas, data, index1, index2, AE):
    color = data.materialColor[data.AE.index(AE)]
    node1 = data.nodeList[index1]
    node2 = data.nodeList[index2]
    width1 = data.width1
    width2 = data.width2
    if data.gameMode == 'run':
        defl11 = data.deflMatrix[index1 * 2]
        defl12 = data.deflMatrix[index1 * 2 + 1]
        defl21 = data.deflMatrix[index2 * 2]
        defl22 = data.deflMatrix[index2 * 2 + 1]
    else:
        defl11, defl12, defl21, defl22 = 0, 0, 0, 0
    x0 = data.x12 + defl11 + node1.x * width1
    y0 = data.y12 - defl12 - node1.y  * width2 + node1.x * width2
    x1 = data.x12 + defl21 + node2.x * width1
    y1 = data.y12 - defl22 - node2.y  * width2 + node2.x * width2
    canvas.create_polygon(x0, y0, x1, y1, x1, y1 + 1.5 * data.barSize,\
                          x0 , y0 + 1.5 * data.barSize, fill = color[1],
                          outline = 'black')
    x2 = x0 + width2 * 4
    y2 = y0 - width1 * 4
    x3 = x1 + width2 * 4
    y3 = y1 - width1 * 4
    canvas.create_polygon(x0, y0, x1, y1, x3, y3, x2 , y2, \
                          fill = color[0], outline = 'black')

def drawBackBar1(canvas, data, index1, index2, AE):
    color = data.materialColor[data.AE.index(AE)]
    node1 = data.nodeList[index1]
    node2 = data.nodeList[index2]
    width1 = data.width1
    width2 = data.width2
    if node1.y > node2.y:
        temp1, temp2  = node1, index1
        node1, index1 = node2, index2
        node2, index2 = temp1, temp2
    if data.gameMode == 'run':
        defl11 = data.deflMatrix[index1 * 2]
        defl12 = data.deflMatrix[index1 * 2 + 1]
        defl21 = data.deflMatrix[index2 * 2]
        defl22 = data.deflMatrix[index2 * 2 + 1]
    else:
        defl11, defl12, defl21, defl22 = 0, 0, 0, 0
    x0 = data.x12 + defl11 + width2 * 3.5 + node1.x  * width1 + width1 / 4
    y0 = data.y12 - defl12 - width1 * 3.5 +\
         node1.x  * width2 - node1.y * data.pixelLength - data.barSize / 2
    x1 = data.x12 + defl21 + width2 * 3.5 + node2.x  * width1 + width1 / 4
    y1 = data.y12 - defl22 - width1 * 3.5 +\
         node2.x  * width2 - node2.y * data.pixelLength + data.barSize / 2
    canvas.create_polygon(x0 - width1 / 2, y0 + data.barSize,
                          x1 - width1 / 2, y1, x1, y1,
                          x0, y0 + data.barSize, fill = color[1],
                          outline = 'black')
    if data.theta0 >= math.pi/2:
        canvas.create_polygon(x0, y0, x1, y1, x1 + width2/2, y1 - width1/2,
                              x0 + width2/2, y0 - width1/2,
                              fill = color[0], outline = 'black')
    else:
        canvas.create_polygon(x0 - width1 / 2, y0 - width2 / 2,
                              x1 - width1 / 2, y1 - width2 / 2,
                              x1 + width2 / 2 - width1 / 2,
                              y1 - width1 / 2 - width2 / 2,
                              x0 + width2 / 2 - width1 / 2,
                              y0 - width1 / 2 - width2 / 2,
                              fill = color[0], outline = 'black')

def drawBackBar2(canvas, data, index1, index2, AE):
    color = data.materialColor[data.AE.index(AE)]
    node1 = data.nodeList[index1]
    node2 = data.nodeList[index2]
    width1 = data.width1
    width2 = data.width2
    deltax = node1.x - node2.x
    deltay = node1.y - node2.y
    barHeight = data.barSize * (deltax ** 2 + deltay ** 2) ** 0.5 / abs(deltax)
    if barHeight >= 1.5 * data.barSize: barHeight = 1.5 * data.barSize
    if data.gameMode == 'run':
        defl11 = data.deflMatrix[index1 * 2]
        defl12 = data.deflMatrix[index1 * 2 + 1]
        defl21 = data.deflMatrix[index2 * 2]
        defl22 = data.deflMatrix[index2 * 2 + 1]
    else:
        defl11, defl12, defl21, defl22 = 0, 0, 0, 0
    x0 = data.x12 + defl11 + node1.x * width1 + width2 * 3.5
    y0 = data.y12 - defl12 +\
         node1.x  * width2 - node1.y * data.pixelLength - width1 * 3.5
    x1 = data.x12 + defl21 + node2.x * width1 + width2 * 3.5
    y1 = data.y12 - defl22 +\
         node2.x  * width2 - node2.y * data.pixelLength - width1 * 3.5
    canvas.create_polygon(x0, y0, x1, y1, x1, y1 + barHeight,
                          x0, y0 + barHeight, fill = color[1],
                          outline = 'black')
    canvas.create_polygon(x0, y0, x1, y1, x1 + width2/2, y1 - width1/2,
                          x0 + width2/2, y0 - width1/2,
                          fill = color[0], outline = 'black')

def drawFrontBar1(canvas, data, index1, index2, AE):
    color = data.materialColor[data.AE.index(AE)]
    node1 = data.nodeList[index1]
    node2 = data.nodeList[index2]
    width1 = data.width1
    width2 = data.width2
    if node1.y > node2.y:
        temp1, temp2  = node1, index1
        node1, index1 = node2, index2
        node2, index2 = temp1, temp2
    if data.gameMode == 'run':
        defl11 = data.deflMatrix[index1 * 2]
        defl12 = data.deflMatrix[index1 * 2 + 1]
        defl21 = data.deflMatrix[index2 * 2]
        defl22 = data.deflMatrix[index2 * 2 + 1]
    else:
        defl11, defl12, defl21, defl22 = 0, 0, 0, 0
    x0 = data.x12 + defl11 + node1.x  * width1 + width1 / 4
    y0 = data.y12 - defl12 +\
         node1.x  * width2 - node1.y * data.pixelLength - data.barSize / 2
    x1 = data.x12 + defl21 + node2.x  * width1 + width1 / 4
    y1 = data.y12 - defl22 +\
         node2.x  * width2 - node2.y * data.pixelLength + data.barSize / 2
    canvas.create_polygon(x0 - width1 / 2, y0 + 2 * data.barSize,
                          x1 - width1 / 2, y1, x1, y1,
                          x0, y0 + 2 * data.barSize, fill = color[1], 
                          outline = 'black')
    if data.theta0 >= math.pi/2:
        canvas.create_polygon(x0, y0, x1, y1, x1 + width2/2, y1 - width1/2,
                              x0 + width2/2, y0 - width1/2,
                              fill = color[0], outline = 'black')
    else:
        canvas.create_polygon(x0 - width1 / 2, y0 - width2 / 2,
                              x1 - width1 / 2, y1 - width2 / 2,
                              x1 + width2 / 2 - width1 / 2,
                              y1 - width1 / 2 - width2 / 2,
                              x0 + width2 / 2 - width1 / 2,
                              y0 - width1 / 2 - width2 / 2,
                              fill = color[0], outline = 'black')

def drawFrontBar2(canvas, data, index1, index2, AE):
    color = data.materialColor[data.AE.index(AE)]
    node1 = data.nodeList[index1]
    node2 = data.nodeList[index2]
    width1 = data.width1
    width2 = data.width2
    deltax = node1.x - node2.x
    deltay = node1.y - node2.y
    barHeight = data.barSize * (deltax ** 2 + deltay ** 2) ** 0.5 / abs(deltax)
    if barHeight >= 1.5 * data.barSize: barHeight = 1.5 * data.barSize
    if data.gameMode == 'run':
        defl11 = data.deflMatrix[index1 * 2]
        defl12 = data.deflMatrix[index1 * 2 + 1]
        defl21 = data.deflMatrix[index2 * 2]
        defl22 = data.deflMatrix[index2 * 2 + 1]
    else:
        defl11, defl12, defl21, defl22 = 0, 0, 0, 0
    x0 = data.x12 + defl11 + node1.x * width1
    y0 = data.y12 - defl12 + node1.x  * width2 - node1.y * data.pixelLength
    x1 = data.x12 + defl21 + node2.x * width1
    y1 = data.y12 - defl22 + node2.x  * width2 - node2.y * data.pixelLength
    canvas.create_polygon(x0, y0, x1, y1, x1, y1 + barHeight,
                          x0, y0 + barHeight, fill = color[1],
                          outline = 'black')
    canvas.create_polygon(x0, y0, x1, y1, x1 + width2/2, y1 - width1/2,
                          x0 + width2/2, y0 - width1/2,
                          fill = color[0], outline = 'black')

def drawBridge(canvas, data):
    for node1 in data.nodeList:                     #draw bars below 0
        for node2 in node1.connection:              #back bar 1
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and node1.x == node2.x:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar1(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #back bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and\
                node1.x != node2.x and node1.y == node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar2(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #back bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and\
                node1.x != node2.x and node1.y != node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar2(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 1
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and node1.x == node2.x:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar1(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and\
                node1.x != node2.x and node1.y == node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar2(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y < 0 or node2.y < 0) and\
                node1.x != node2.x and node1.y != node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar2(canvas, data, index1, index2, AE)

    for node1 in data.nodeList:
        for node2 in node1.connection:              #bridge deck
            AE = node2[1]
            node2 = node2[0]
            if node1.y == 0 and node2.y == 0:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawDeck(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:                     #draw bars above 0
        for node2 in node1.connection:              #back bar 1
            AE = node2[1]
            node2 = node2[0]
            if node1.x == node2.x and (not (node1.y < 0 or node2.y < 0)):
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar1(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #back bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y > 0 or node2.y > 0) and\
                node1.x != node2.x and node1.y != node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar2(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #back bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y > 0 or node2.y > 0) and\
                node1.x != node2.x and node1.y == node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawBackBar2(canvas, data, index1, index2, AE)
    drawCar(canvas, data)                           #car
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 1
            AE = node2[1]
            node2 = node2[0]
            if node1.x == node2.x and (not (node1.y < 0 or node2.y < 0)):
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar1(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y > 0 or node2.y > 0) and\
                node1.x != node2.x and node1.y != node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar2(canvas, data, index1, index2, AE)
    for node1 in data.nodeList:
        for node2 in node1.connection:              #front bar 2
            AE = node2[1]
            node2 = node2[0]
            if (node1.y > 0 or node2.y > 0) and\
                node1.x != node2.x and node1.y == node2.y:
                index1 = data.nodeList.index(node1)
                index2 = data.nodeList.index(node2)
                drawFrontBar2(canvas, data, index1, index2, AE)

def chooseCar(data, num):
    if num == 0:
        a = 'red'
        b = 'red'
        c = 'black'
        d = 'wheat'
        data.car = [[[0,0,0,0,0,0],[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]],
                    [[0,0,0,0,0,0],[0,a,a,a,0,0], [b,b,b,b,b,d], [0,c,0,0,c,0]],
                    [[0,0,0,0,0,0],[0,a,a,a,0,0], [b,b,b,b,b,b], [0,0,0,0,0,0]],
                    [[0,0,0,0,0,0],[0,a,a,a,0,0], [b,b,b,b,b,d], [0,c,0,0,c,0]],
                    [[0,0,0,0,0,0],[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]]]
    elif num == 1:
        a = 'Black'
        b = 'SeaGreen'
        c = 'DarkGreen'
        data.car = \
    [[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[a,a,a,a,a,a,0],[a,a,a,a,a,a,0]],
     [[0,b,0,0,0,0,0],[0,b,b,b,0,0,0],[0,b,b,b,b,0,0],[0,0,0,0,0,0,0]],
     [[0,b,c,c,c,c,c],[0,b,b,b,0,0,0],[0,b,b,b,b,0,0],[0,0,0,0,0,0,0]],
     [[0,b,0,0,0,0,0],[0,b,b,b,0,0,0],[0,b,b,b,b,0,0],[0,0,0,0,0,0,0]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[a,a,a,a,a,a,0],[a,a,a,a,a,a,0]]]
    elif num == 2:
        c = 'Black'
        b = 'white'
        a = 'red'
        data.car = \
    [[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[a,0,0,0,0,0,0],[b,c,0,0,0,c,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[a,0,0,0,0,0,0],[b,b,b,b,b,b,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[a,0,0,0,0,0,0],[b,c,0,0,0,c,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]]
    elif num == 3:
        a = 'yellow'
        b = 'cyan'
        c = 'black'
        data.car = \
    [[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
     [[a,a,a,a,a,a,a],[a,a,a,a,a,a,b],[a,a,a,a,a,a,a],[0,c,0,0,0,c,0]],
     [[a,a,a,a,a,a,a],[a,a,a,a,a,a,a],[a,a,a,a,a,a,a],[0,0,0,0,0,0,0]],
     [[a,a,a,a,a,a,a],[a,a,a,a,a,a,b],[a,a,a,a,a,a,a],[0,c,0,0,0,c,0]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]]
    elif num == 4:
        a = 'gray'
        b = 'lightgray'
        c = 'white'
        data.car = \
    [[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,b,a,a,a,b,0]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[b,a,a,a,a,a,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,b,0,0,0,0],[b,a,a,a,a,a,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[b,a,a,a,a,a,b]],
     [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,b,a,a,a,b,0]]]


def drawCar(canvas, data):
    chooseCar(data, data.carNum)
    data.carDeepth = len(data.car)
    data.carRow = len(data.car[0])
    data.carCol = len(data.car[0][0])
    if data.carX <= 11 or data.carX > 47:
        row0 = 11
    else:
        sortedMap = data.sortedMap
        for i in range(len(sortedMap) - 1):
            if sortedMap[i][0] < data.carX <= sortedMap[i + 1][0]:
                length = sortedMap[i + 1][0] - sortedMap[i][0]
                index1 = sortedMap[i    ][1]
                index2 = sortedMap[i + 1][1]
                row0 = -((data.deflMatrix[index2 * 2 + 1] - \
                         data.deflMatrix[index1 * 2 + 1]) * \
                        (data.carX - sortedMap[i][0]) / length +\
                         data.deflMatrix[index1 * 2 + 1])/data.pixelLength + 11
    col0 = data.carX
    data.carx0 = data.width2 * 4 * (data.deepth / 2 - data.carSize / 8) + \
                 data.width1 * (col0 - data.col / 2) + data.x0
    data.cary0 = data.pixelLength * (row0 - data.row / 2) + data.y0 + \
                 data.width2 * (col0 - data.col / 2) - \
                 data.width1 * 4 * (data.deepth / 2 - data.carSize / 8)
    height = data.pixelLength * data.carSize
    width1 = data.width1 * data.carSize
    width2 = data.width2 * data.carSize
    if data.theta0 >= math.pi / 2:                       #look from right side
        for index1 in range(data.carRow):                #from bottom to top
            row = data.carRow - 1 - index1
            for col in range(data.carCol):               #from left to right
                for index2 in range(data.carDeepth):
                    deepth = data.carDeepth - 1 - index2 #from back to front
                    if data.car[deepth][row][col] != 0:
                        color = data.car[deepth][row][col]
                        drawSingleCarCubeR(canvas, data, row,
                                           col, deepth, color)
    if data.theta0 < math.pi / 2:                        #look from left side
        for index1 in range(data.carRow):                #from bottom to top
            row = data.carRow - 1 - index1
            for index2 in range(data.carCol):            #from right to left
                col = data.carCol - 1 - index2
                for index3 in range(data.carDeepth):     #from back to front
                    deepth = data.carDeepth - 1 - index3
                    if data.car[deepth][row][col] != 0:
                        color = data.car[deepth][row][col]
                        drawSingleCarCubeL(canvas, data, row,
                                           col, deepth, color)

def drawSingleCarCubeR(canvas, data, row, col, deepth, color):
    height = data.pixelLength * data.carSize
    width1 = data.width1 * data.carSize
    width2 = data.width2 * data.carSize
    x0 = width2 * (deepth - 2) + \
         width1 * (col - data.carCol/2) + data.carx0
    y0 = height * (row - data.carRow/2) + data.cary0 + \
         width2 * (col - data.carCol/2) - width1 * deepth
    if deepth == 0 or data.car[deepth - 1][row][col] == 0:
        #drawFront
        canvas.create_polygon(x0         , y0                   ,
                              x0 + width1, y0 + width2          ,
                              x0 + width1, y0 + height + width2 ,
                              x0         , y0 + height          ,
                              fill = color, outline = 'black')
    if col == data.carCol - 1 or data.car[deepth][row][col + 1] == 0:
        #drawRight
        canvas.create_polygon(x0 + width1         ,y0 + width2                 ,
                              x0 + width1 + width2,y0 + width2 - width1        ,
                              x0 + width1 + width2,y0 + width2 - width1 +height,
                              x0 + width1         ,y0 + width2 + height        ,
                              fill = color, outline = 'black')
    if row == 0 or data.car[deepth][row - 1][col] == 0:
        #drawTop
        canvas.create_polygon(x0                  , y0                  ,
                              x0 + width1         , y0 + width2         ,
                              x0 + width1 + width2, y0 + width2 - width1,
                              x0 +          width2, y0          - width1,
                              fill = color, outline = 'black')

def drawSingleCarCubeL(canvas, data, row, col, deepth, color):
    height = data.pixelLength * data.carSize
    width1 = data.width1 * data.carSize
    width2 = data.width2 * data.carSize
    x0 = width2 * (deepth - 2) + \
         width1 * (col - data.carCol/2) + data.carx0
    y0 = height * (row - data.carRow/2) + data.cary0 + \
         width2 * (col - data.carCol/2) - width1 * deepth
    if col == 0 or data.car[deepth][row][col - 1] == 0:
        # drawLeft
        canvas.create_polygon(x0         , y0                  ,\
                              x0 + width2, y0 - width1         ,\
                              x0 + width2, y0 + height - width1,\
                              x0         , y0 + height         ,\
                              fill = color, outline = 'black')
    if deepth == 0 or data.car[deepth - 1][row][col] == 0:
        #drawFront
        canvas.create_polygon(x0         , y0                   ,
                              x0 + width1, y0 + width2          ,
                              x0 + width1, y0 + height + width2 ,
                              x0         , y0 + height          ,
                              fill = color, outline = 'black')
    if row == 0 or data.car[deepth][row - 1][col] == 0:
        #drawTop
        canvas.create_polygon(x0                  , y0                  ,
                              x0 + width1         , y0 + width2         ,
                              x0 + width1 + width2, y0 + width2 - width1,
                              x0 +          width2, y0          - width1,
                              fill = color, outline = 'black')


def backgroundColor(data):
    (r0, g0, b0) = (  0, 206, 209)
    (r1, g1, b1) = (255, 250, 205)
    data.backgroundColor = [0] * 14
    for i in range(14):
        ratio = i / 13
        ri = int((r1 - r0) * ratio + r0)
        gi = int((g1 - g0) * ratio + g0)
        bi = int((b1 - b0) * ratio + b0)
        color = '#%02x%02x%02x' % (ri, gi, bi)
        data.backgroundColor[i] = color
    data.backgroundColor = data.backgroundColor + data.backgroundColor[-1::-1]


def drawStartGrid(canvas, data):
    row = data.row / 4
    width1 = data.width1 * 4
    width2 = data.width2 * 4
    data.backgroundColor = data.backgroundColor[1:] + [data.backgroundColor[1]]
    for deepth in range(-12, 15):
        x0 = width2 * (deepth) + \
             width1 * (-7 - data.col / 8) + data.x0
        y0 = 4 * data.pixelLength * (row - data.row / 8) + data.y0 + \
             width2 * (-7 - data.col / 8) - width1 * deepth
        x1 = width2 * (deepth) + \
             width1 * (23 - data.col / 8) + data.x0
        y1 = 4 * data.pixelLength * (row - data.row / 8) + data.y0 + \
             width2 * (23 - data.col / 8) - width1 * deepth 
        canvas.create_polygon(x0                  , y0                  ,\
                              x1 + width1         , y1 + width2         ,\
                              x1 + width1 + width2, y1 + width2 - width1,\
                              x0 +          width2, y0          - width1,\
                              fill = data.backgroundColor[deepth + 12])


def drawText(canvas, data):
    canvas.create_text(data.width/2, data.height*5/6,
                       text = 'Press "Space" to start!',
                       font = "fixedsys 26 bold", 
                       fill = 'gray' + str((data.pace + 1) * 15 % 99))

def drawBarForce(canvas, data):
    height = [0] * 40
    canvas.create_text(data.width / 2 -  10, data.barForceHeight - 20,
                       text = 'Bar Forces', anchor = 'c', font = 'fixedsys')
    for i in range(len(data.barForceList)):
        maxForce = data.barForceList[i][1] * data.maxForceRatio
        position = round(data.barForceList[i][2] / 9) * 9
        if position >= 27: position = 27
        color = textColor(data.barForceList[i][0], maxForce)
        canvas.create_text(data.barForceLeftMargin + \
                           position * data.barForceWidth, 
                           data.barForceHeight + 20 * height[position],
                           anchor = 'e',
                           text = str(data.barForceList[i][0]) +\
                                  '/' + str(maxForce),
                           fill = color, font = 'fixedsys')
        if data.barForceList[i][0] > maxForce:
            canvas.create_text(data.barForceLeftMargin + \
                               position * data.barForceWidth, 
                               data.barForceHeight + 20 * height[position],
                               anchor = 'w',
                               text = ' !!!!', fill = color, font = 'fixedsys')
        height[position] += 1

def drawResultInterface(canvas, data):
    canvas.create_rectangle(data.width / 4 - 50, data.height / 4,
                            3 * data.width / 4 + 50, 4 * data.height / 5,
                            fill = 'white', dash = (4,3), width = 2)
    canvas.create_text(data.width / 2, data.height / 4 + 10, anchor = 'n',
                       text = 'Result', font = 'fixedsys 26 bold')
    canvas.create_text(data.width / 3, 4 * data.height / 5 - 20, anchor = 's',
                       text = 'Remodel your bridge', font = 'fixedsys 15')
    canvas.create_text(2 * data.width / 3, 4 * data.height / 5 - 20,
                       anchor = 's',
                       text = 'Build new bridge', font = 'fixedsys 15')
    height = [0] * 40
    for i in range(len(data.largestBarForce)):
        maxForce = data.barForceList[i][1] * data.maxForceRatio
        position = round(data.barForceList[i][2] / 9) * 9 
        if position >= 27: position = 27
        color = textColor(data.largestBarForce[i], maxForce)
        canvas.create_text(data.barForceLeftMargin + \
                           position * data.barForceWidth, 
                           390 + 20 * height[position],
                           anchor = 'e',
                           text = str(data.largestBarForce[i]) +\
                                  '/' + str(maxForce),
                           fill = color, font = 'fixedsys')
        if data.largestBarForce[i] > maxForce:
            canvas.create_text(data.barForceLeftMargin + \
                               position * data.barForceWidth, 
                               390 + 20 * height[position],
                               anchor = 'w',
                               text = ' !!!!', fill = color, font = 'fixedsys')
        height[position] += 1
        canvas.create_line(data.resultBarMarginL + \
                           data.barForceList[i][3].x * data.pixelLength,
                           data.resultBarMarginU - \
                           data.barForceList[i][3].y * data.pixelLength,
                           data.resultBarMarginL + \
                           data.barForceList[i][4].x * data.pixelLength,
                           data.resultBarMarginU - \
                           data.barForceList[i][4].y * data.pixelLength,
                           fill = color, width = 3)

def drawInstruction(canvas, data):
    if data.isPlayingBGM == True:
        text = ' Music On' +\
               '\n Car: ' + data.carName +\
               '    Car weight: ' + str(data.carWeight) +\
               '\n\n Press "Up" or "Down" to change car' +\
               '\n Press "<--" or "-->" to rotate' +\
               '\n Press "r" to try an already built bridge demo' +\
               '\n Press "f" build a new bridge'
    else:
        text = ' Music Off' +\
               '\n Car: ' + data.carName +\
               '    Car weight: ' + str(data.carWeight) +\
               '\n\n Press "Up" or "Down" to change car' +\
               '\n Press "<--" or "-->" to rotate' +\
               '\n Press "r" to try an already built bridge demo' +\
               '\n Press "f" build a new bridge'
    canvas.create_text(0, data.height, anchor = 'sw',
                       text = text, font = 'fixedsys')
    canvas.create_text(data.width, data.height, anchor = 'se',
                       text = '    Maretial Strength'
                       '\nWood1           : *'+
                       '\nWood2           : **'+
                       '\nWood3           : ***'+
                       '\nIron            : *****'+
                       '\nPittsburgh Steel: ******* ', font = 'fixedsys')

def drawGoArrow(canvas, data):
    canvas.create_text(data.width / 2, 3 * data.height / 4 + 100, anchor = 'c',
                       text = '''\


------\\
       \\
       /
------/ 
''', font = 'fixedsys 15')
    canvas.create_text(data.width / 2, 3 * data.height / 4 + 100, text = 'GO!', 
                       anchor = 'n', font = 'fixedsys 15')

def drawGrid(canvas, data):
    x0 = data.x0 + data.width2 * 4
    y0 = data.y0 - data.width1 * 4
    width1 = data.width1
    width2 = data.width2
    height = data.pixelLength
    for i in range(-8, 8, 2):
        canvas.create_line(x0 - (data.col / 2 - i - 10) * width1,
                           y0 + i * height - (data.col / 2 - i - 10 ) * width2,
                           x0 + (data.col / 2 - i - 10) * width1,
                           y0 + i * height + (data.col / 2 - i - 10) * width2,
                           fill = 'Dim Gray')
    for j in range(2, 16, 2):
        canvas.create_line(x0 - (data.col / 2) * width1 + j * width1,
                           y0 - 8 * height - (data.col / 2 - j) * width2,
                           x0 - (data.col / 2) * width1 + j * width1,
                           y0 - (10 - j) * height - (data.col / 2 - j) * width2,
                           fill = 'Dim Gray')
    for j in range(16, 45, 2):
        canvas.create_line(x0 - (data.col / 2) * width1 + j * width1,
                           y0 - 8 * height - (data.col / 2 - j) * width2,
                           x0 - (data.col / 2) * width1 + j * width1,
                           y0 + 6 * height - (data.col / 2 - j) * width2,
                           fill = 'Dim Gray')
    for j in range(46, 60, 2):
        canvas.create_line(x0 - (data.col / 2) * width1 + j * width1,
                           y0 - 8 * height - (data.col / 2 - j) * width2,
                           x0 - (data.col / 2) * width1 + j * width1,
                           y0 + (50 - j) * height - (data.col / 2 - j) * width2,
                           fill = 'Dim Gray')

def drawNode(canvas, data):
    color = 'wheat'
    x0 = data.x0 + data.width2 * 4
    y0 = data.y0 - data.width1 * 4
    width1 = data.width1
    width2 = data.width2
    height = data.pixelLength
    r1 = data.dotR * data.cosTheta
    r2 = data.dotR
    for node in data.nodeList:
        col = node.x - 18
        row = -node.y + 2 
        canvas.create_oval(x0 + col * width1 - r1,
                           y0 + row * height + col * width2 - r2,
                           x0 + col * width1 + r1, 
                           y0 + row * height + col * width2 + r2, fill = color)

def drawToolBox(canvas, data):
    canvas.create_rectangle(data.width - data.margin - data.toolBoxWidth,
                            data.margin,
                            data.width - data.margin / 2, 
                            data.margin + data.toolBoxHeight)
    canvas.create_text(data.width - data.margin - data.toolBoxWidth / 2,
                       data.margin * 2, anchor = 's', text = 'Tool Box',
                       font = 'fixedsys')
    canvas.create_text(data.width - data.toolBoxWidth - 2 * data.margin / 3,
                       data.margin * 3, anchor = 'sw', text = 'Material',
                       font = 'fixedsys')
    color = ['black'] * 5
    if data.isRemovingBar == False:
        i = data.currMaterial
        color[i] = 'red'
    canvas.create_text(data.width - data.toolBoxWidth + data.margin / 3,
                       data.margin * 4, anchor = 'sw', text = 'Wood1',
                       font = 'fixedsys', fill = color[0])
    canvas.create_text(data.width - data.toolBoxWidth + data.margin / 3,
                       data.margin * 5, anchor = 'sw', text = 'Wood2',
                       font = 'fixedsys', fill = color[1])
    canvas.create_text(data.width - data.toolBoxWidth + data.margin / 3,
                       data.margin * 6, anchor = 'sw', text = 'Wood3',
                       font = 'fixedsys', fill = color[2])
    canvas.create_text(data.width - data.toolBoxWidth + data.margin / 3,
                       data.margin * 7, anchor = 'sw', text = 'Iron',
                       font = 'fixedsys', fill = color[3])
    canvas.create_text(data.width - data.toolBoxWidth + data.margin / 3,
                       data.margin * 8, anchor = 'w', text ='Pittsburgh\nSteel',
                       font = 'fixedsys', fill = color[4])
    c = 'red' if data.isRemovingBar == True else 'black'
    canvas.create_text(data.width - data.toolBoxWidth - 2 * data.margin / 3,
                       data.margin * 10, anchor = 'sw', text = 'Remove Bar',
                       font = 'fixedsys', fill = c)
    canvas.create_rectangle(data.width - data.toolBoxWidth - 2*data.margin / 3,
                            data.margin * 3.25,
                            data.width - data.toolBoxWidth,
                            data.margin * 3.75, fill = data.materialColor[0][0])
    canvas.create_rectangle(data.width - data.toolBoxWidth - 2*data.margin / 3,
                            data.margin * 4.25,
                            data.width - data.toolBoxWidth,
                            data.margin * 4.75, fill = data.materialColor[1][0])
    canvas.create_rectangle(data.width - data.toolBoxWidth - 2*data.margin / 3,
                            data.margin * 5.25,
                            data.width - data.toolBoxWidth,
                            data.margin * 5.75, fill = data.materialColor[2][0])
    canvas.create_rectangle(data.width - data.toolBoxWidth - 2*data.margin / 3,
                            data.margin * 6.25,
                            data.width - data.toolBoxWidth,
                            data.margin * 6.75, fill = data.materialColor[3][0])
    canvas.create_rectangle(data.width - data.toolBoxWidth - 2*data.margin / 3,
                            data.margin * 7.25,
                            data.width - data.toolBoxWidth,
                            data.margin * 7.75, fill = data.materialColor[4][0])

def drawProgressBar(canvas, data):
    if data.carX <= 11:
        progress = 0
    elif data.carX >= 47:
        progress = 100
    else:
        progress = math.floor((data.carX - 11) / 0.36)
    canvas.create_rectangle(data.width - data.margin - data.progressBarWidth,
                            data.margin,
                            data.width - data.margin, 
                            data.margin + data.progressBarHeight)
    for i in range(progress):
        canvas.create_rectangle(data.width - data.margin - \
                                data.progressBarWidth * (100 - i) / 100,
                                data.margin + 3,
                                data.width - data.margin - \
                                data.progressBarWidth * (99 - i) / 100, 
                                data.margin + data.progressBarHeight - 3, 
                                fill = 'black',outline = '')
    num = round((data.carX - 11) / 0.36)
    if num < 0: num = 0
    if num > 100: num = 100
    text = str(num) + '%'
    canvas.create_text(data.width - data.margin - data.progressBarWidth / 2,
                       data.margin + data.progressBarHeight / 2,
                       anchor = 'c', text = text, fill = 'gray50',
                       font = 'fixedsys')
    canvas.create_text(data.width - data.margin - data.progressBarWidth / 2,
                       data.margin + data.progressBarHeight + 10,
                       anchor = 'c', text = 'Progress bar', font = 'fixedsys')

def updataData(data):
    data.theta  = data.theta0 - math.pi / 2
    data.sinTheta = math.sin(data.theta)
    data.cosTheta = math.cos(data.theta)
    data.width1 = round(data.pixelLength * data.cosTheta, 4)
    data.width2 = round(data.pixelLength * data.sinTheta, 4)
    data.x12 = data.width1 * (12 - data.col/2) + data.x0 + data.width2 * 4
    data.y12 = data.pixelLength * (12 - data.row/2) + data.y0 + \
               data.width2 * (12 - data.col/2) - data.width1 * 4

def drawingInterfaceMousePressed(event, data):
    if 600 <= event.y <= 680 and 450 <= event.x <= 550:
        data.stiffnessMatrix = []
        for i in range(len(data.nodeList) * 2):
            data.stiffnessMatrix.append([0] * (len(data.nodeList) * 2))
        for node in data.nodeList:
            node.addToStiffnessMatrix(data)
        data.carX = 10
        calculateDefl(data)
        data.largestBarForce = []
        data.isPlacingBar = False
        data.gameMode = 'run'
    elif data.isRemovingBar == False and event.y <= 530:
        x0 = data.x12
        y0 = data.y12
        x = 2 * round((event.x - x0) / (2 * data.width1))
        y = 2 * round((y0 + x * data.width2 - event.y) / (2 * data.pixelLength))
        if data.isPlacingBar == False:
            if Node(x, y, data) in data.nodeList:
                index1 = data.nodeList.index(Node(x, y, data))
                data.node1 = data.nodeList[index1]
            else:
                data.node1 = Node(x, y, data)
                data.nodeList.append(data.node1)
            data.isPlacingBar = True
        else:
            if Node(x, y, data) in data.nodeList:
                index2 = data.nodeList.index(Node(x, y, data))
                data.node2 = data.nodeList[index2]
            else:
                data.node2 = Node(x, y, data)
                data.nodeList.append(data.node2)
            if not data.node1 == data.node2:
                data.node1.connectTo(data.node2, data.AE[data.currMaterial])
                data.isPlacingBar = False
    else:
        data.isPlacingBar = False
        for node1 in data.nodeList:
            for nextNode in  node1.connection:
                node2 = nextNode[0]
                x0 = data.x12
                y0 = data.y12
                x = (event.x - x0) / data.width1
                y = (y0 + x * data.width2 - event.y) / data.pixelLength
                deltax1 = x - node1.x
                deltay1 = y - node1.y
                deltax2 = x - node2.x
                deltay2 = y - node2.y
                if deltax1 * deltax2 <= 0 and deltay1 * deltay2 <= 0:
                    if abs(math.atan(deltax1 / deltay1) - \
                           math.atan(deltax2 / deltay2)) <= math.pi / 15:
                        node1.connection.remove(nextNode)
                elif node1.x == node2.x and deltay1 * deltay2 <= 0:
                    if deltay1 == 0 or deltay2 == 0 or\
                      (abs(math.atan(deltax1 / deltay1)) <= math.pi / 15 and\
                       abs(math.atan(deltax2 / deltay2)) <= math.pi / 15):
                        node1.connection.remove(nextNode)
                elif node1.y == node2.y and deltax1 * deltax2 <= 0:
                    if deltay1 == 0 or deltay2 == 0 or\
                      (abs(math.atan(deltax1 / deltay1)) >= 13*math.pi / 30 and\
                       abs(math.atan(deltax2 / deltay2)) >= 13*math.pi / 30):
                        node1.connection.remove(nextNode)

def drawingInterfaceToolBoxClicked(event, data):
    if data.margin * 3 <= event.y <= data.margin * 4:
        data.currMaterial = 0
    elif data.margin * 4 < event.y <= data.margin * 5:
        data.currMaterial = 1
    elif data.margin * 5 < event.y <= data.margin * 6:
        data.currMaterial = 2
    elif data.margin * 6 < event.y <= data.margin * 7:
        data.currMaterial = 3
    elif data.margin * 7 < event.y <= data.margin * 9:
        data.currMaterial = 4
    data.isRemovingBar = False
    if data.margin * 9 < event.y <= data.margin * 11:
        data.isRemovingBar = not data.isRemovingBar

def resultInterfaceClicked(event, data):
    if 3 * data.height / 5 + 50 <= event.y <= 4 * data.height / 5:
        if data.width / 4 - 50 <= event.x <= data.width / 2:
            data.gameMode = 'draw'
            data.carX = 10
        elif data.width / 2 <= event.x <= 3 * data.width / 4 + 50:
            data.gameMode = 'draw'
            init(data)


def redrawAll(canvas, data):
    drawStartGrid(canvas, data)
    if data.gameMode == 'start':
        updataData(data)
        drawAllCube(canvas, data)
        drawText(canvas, data)
    elif data.gameMode == 'draw':
        updataData(data)
        drawAllCube(canvas, data)
        drawBridge(canvas, data)
        drawInstruction(canvas, data)
        drawGoArrow(canvas, data)
        drawGrid(canvas, data)
        drawNode(canvas, data)
        drawToolBox(canvas, data)
    elif data.gameMode == 'result':
        updataData(data)
        drawAllCube(canvas, data)
        drawBridge(canvas, data)
        # drawBarForce(canvas, data)
        drawInstruction(canvas, data)
        drawProgressBar(canvas, data)
        drawResultInterface(canvas, data)
    else:
        updataData(data)
        drawAllCube(canvas, data)
        drawBridge(canvas, data)
        drawBarForce(canvas, data)
        drawInstruction(canvas, data)
        drawProgressBar(canvas, data)

def timerFired(data):
    if data.gameMode == 'result':
        moveWave(data)
    if data.gameMode == 'start':
        moveWave(data)
    if data.gameMode == 'draw':
        pass
    else:
        moveWave(data)
        if 50 >= data.carX > 9:
            data.carX += data.carSpeed
        calculateDefl(data)
        calculateBarForce(data)
    if data.carX >= 50:
        data.gameMode = 'result'
    for k in range(len(data.largestBarForce)):
        if data.barForceList[k][0] >= 10000:
            data.gameMode = 'result'
            data.carX = 9

def mousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y
    if data.gameMode == 'draw':
        if event.x <= data.width - data.margin - data.toolBoxWidth:
            drawingInterfaceMousePressed(event, data)
        else:
            drawingInterfaceToolBoxClicked(event, data)
    if data.gameMode == 'result':
        resultInterfaceClicked(event, data)
    if 0 <= event.x <= 80 and 580 <= event.y <= 610:
        if data.isPlayingBGM == True:
            stopSound()
            data.isPlayingBGM = False
        else:
            startSound("DownTheRoad.wav", async=True, loop=True)
            data.isPlayingBGM = True

def mouseDragged(event, data):
    if data.gameMode != 'draw':
        if event.x - data.mouseX >= 5:
            data.theta0 -= data.deltaTheta
        if event.x - data.mouseX <= -5:
            data.theta0 += data.deltaTheta
        data.mouseX = event.x
    if data.theta0 >= math.pi:
        data.theta0 = math.pi
    elif data.theta0 <= 0:
        data.theta0 = 0


def keyPressed(event, data):
    if event.char == 'm':
        startSound("DownTheRoad.wav", async=True, loop=True)
    if data.gameMode == 'start':
        if (event.char == ' '):
            data.gameMode = 'draw'
            init(data)
            calculateDefl(data)
    elif data.gameMode != 'start':
        if event.char == 'r':
            data.gameMode = 'run'
            init(data)
            bridgeDemo(data)
            data.carX += 1
        elif event.char == 'b':
            data.gameMode = 'draw'
            data.carX = 10
        elif event.char == 'f': 
            data.gameMode = 'draw'
            init(data)
        elif event.char == 't':
            data.stiffnessMatrix = []
            for i in range(len(data.nodeList) * 2):
                data.stiffnessMatrix.append([0] * (len(data.nodeList) * 2))
            for node in data.nodeList:
                node.addToStiffnessMatrix(data)
            data.carX = 10
            calculateDefl(data)
            data.largestBarForce = []
            data.isPlacingBar = False
            data.gameMode = 'run'
    if   (event.keysym == "Left"):  data.theta0 += data.deltaTheta
    elif (event.keysym == "Right"): data.theta0 -= data.deltaTheta
    if   (event.keysym == "Up"):
        data.carNum = (data.carNum + 1) % 5
        data.carName = data.carNameList[data.carNum]
        data.carWeight = data.carWeightList[data.carNum]
    elif (event.keysym == "Down"):
        data.carNum = (data.carNum - 1) % 5
        data.carName = data.carNameList[data.carNum]
        data.carWeight = data.carWeightList[data.carNum]
    if data.theta0 >= math.pi:
        data.theta0 = math.pi
    elif data.theta0 <= 0:
        data.theta0 = 0

def run(width = 1000, height = 700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseDraggedWrapper(event, canvas, data):
        mouseDragged(event, data)
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
    data.gameMode = 'start'
    data.carNum = 0
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                            mouseDraggedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    startSound("DownTheRoad.wav", async=True, loop=True)
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    stopSound()
    print("bye!")

run()