# hw8.py
# Hanzhou Lu / hanzhoul / II

class Gate(object):
    def __init__(self, gateType):
        self.gateType = gateType
        self.inputValues = None
        self.outputValue = None
        self.outputGates = []
        self.inputGates  = []
        self.placed = False
        self.x = 0
        self.y = 0

    def connectTo(self, other):
        self.outputGates.append(other)
        other.inputGates.append(self)

    def setInputValue(self, key, boolean):
        if self.inputValues == None:
            self.inputValues = dict()
        self.inputValues.update({key : boolean})
        self.setOutputValue()
        for gate in self.outputGates:
            gate.setInputValue(self, self.outputValue)

    def setOutputValue(self):
        if self.gateType == "input":
            self.outputValue = self.inputValues[None]
        if self.gateType == "output":
            for key in self.inputValues:
                self.outputValue = self.inputValues[key]
        if self.gateType == "not":
            for key in self.inputValues:
                boolean = self.inputValues[key]
            self.outputValue = not boolean
        if self.gateType == "and":
            self.outputValue = self.setAndGateValue()
        if self.gateType == "or":
            self.outputValue = self.setOrGateValue()

    def setAndGateValue(self):
        if len(self.inputValues) == 1: return None
        boolean = True
        for key in self.inputValues:
            if self.inputValues[key] == False:
                boolean = False
                break
        return boolean

    def setOrGateValue(self):
        if len(self.inputValues) == 1: return None
        boolean = False
        for key in self.inputValues:
            if self.inputValues[key] == True:
                boolean = True
                break
        return boolean

    def getInputGates(self):
        return self.inputGates

    def getOutputGates(self):
        return self.outputGates

    def getMaxInputGates(self):
        return len(self.inputGates)

    def getMaxOutputGates(self):
        return len(self.outputGates)

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *

def init(data):
    data.width = 1000
    data.height = 500
    data.catalogWidth = 150
    data.gateNum = 5
    data.toolbarHeight = 50
    data.gateHeight = 30
    data.gateWidth  = 40
    data.gateCircleR = 3
    data.gateCircleD = 6
    data.gateLineLen = 20
    data.dotR = 5
    data.margin = 10
    data.buttonHeight = 30
    data.buttonWidth = 80
    data.gateList = []
    data.isPlacingGate = False
    data.isPlacingLine = False
    data.isPowerOn = False

def drawCanvas(canvas, data):
    canvas.create_line(0,data.toolbarHeight,data.width,data.toolbarHeight,
                       width = 2)
    canvas.create_line(data.catalogWidth, data.toolbarHeight,
                       data.catalogWidth, data.height       ,
                       width = 2)
    data.delta = (data.height-data.toolbarHeight)/data.gateNum
    data.y1 =  data.toolbarHeight + data.delta
    data.y2 =  data.y1            + data.delta
    data.y3 =  data.y2            + data.delta
    data.y4 =  data.y3            + data.delta
    data.y5 =  data.y4            + data.delta
    canvas.create_line(0, data.y1, data.catalogWidth, data.y1, width = 2)
    canvas.create_line(0, data.y2, data.catalogWidth, data.y2, width = 2)
    canvas.create_line(0, data.y3, data.catalogWidth, data.y3, width = 2)
    canvas.create_line(0, data.y4, data.catalogWidth, data.y4, width = 2)
    canvas.create_line(0, data.y5, data.catalogWidth, data.y5, width = 2)

def drawLables(canvas, data):
    drawSingleNotGate(canvas,data, data.catalogWidth/3, data.y1-2*data.delta/3)
    drawSingleOrGate(canvas,data, data.catalogWidth/3, data.y2-2*data.delta/3)
    drawSingleAndGate(canvas,data, data.catalogWidth/3, data.y3-2*data.delta/3)
    drawSingleInputGate(canvas,data, data.catalogWidth/2, data.y4-data.delta/2)
    drawSingleOutputGate(canvas,data, data.catalogWidth/2, data.y5-data.delta/2)
    canvas.create_text(data.catalogWidth/2,data.y1,anchor='s',text='NOT Gate')
    canvas.create_text(data.catalogWidth/2,data.y2,anchor='s',text='OR Gate')
    canvas.create_text(data.catalogWidth/2,data.y3,anchor='s',text='AND Gate')
    canvas.create_text(data.catalogWidth/2,data.y4,anchor='s',text='Input')
    canvas.create_text(data.catalogWidth/2,data.y5,anchor='s',text='Output')

def drawButtons(canvas, data):
    data.x1 = data.buttonWidth * 2
    data.x2 = data.buttonWidth * 2 + data.x1
    data.x3 = data.buttonWidth * 2 + data.x2
    data.x4 = data.buttonWidth * 2 + data.x3
    margin = (data.toolbarHeight - data.buttonHeight)/2
    canvas.create_rectangle(data.x1, margin,
                    data.x1 + data.buttonWidth, margin+ data.buttonHeight)
    canvas.create_rectangle(data.x2, margin,
                    data.x2 + data.buttonWidth, margin+ data.buttonHeight)
    canvas.create_rectangle(data.x3, margin,
                    data.x3 + data.buttonWidth, margin+ data.buttonHeight)
    if data.isPowerOn == True:
        canvas.create_rectangle(data.x4, margin,
        data.x4 + data.buttonWidth, margin+ data.buttonHeight, fill = 'red')
    else:
        canvas.create_rectangle(data.x4, margin,
                    data.x4 + data.buttonWidth, margin+ data.buttonHeight)
    canvas.create_text(data.x1 + data.buttonWidth/2, data.toolbarHeight/2,
                    anchor = 'center', text = 'Clear', font = 'Arial 14')
    canvas.create_text(data.x2 + data.buttonWidth/2, data.toolbarHeight/2,
                    anchor = 'center', text = 'Save', font = 'Arial 14')
    canvas.create_text(data.x3 + data.buttonWidth/2, data.toolbarHeight/2,
                    anchor = 'center', text = 'Load', font = 'Arial 14')
    canvas.create_text(data.x4 + data.buttonWidth/2, data.toolbarHeight/2,
                    anchor = 'center', text = 'Power!!!', font = 'Arial 14')
    canvas.create_text(data.x4 + data.buttonWidth*3, data.toolbarHeight/2,
                    anchor = 'center', text = 'All buttons work!! Woohoo!!')

def drawSingleNotGate(canvas, data, x, y):
    canvas.create_polygon(x               , y                  ,
                          x + data.gateWidth - data.gateCircleD, 
                          y+data.gateHeight/2                  ,
                          x               , y+data.gateHeight  , 
                          fill = ''  , outline = 'black')
    canvas.create_oval   (x + data.gateWidth    - data.gateCircleD, 
                          y + data.gateHeight/2 - data.gateCircleR,
                          x + data.gateWidth                      , 
                          y + data.gateHeight/2 + data.gateCircleR,
                          fill = ''  , outline = 'black')
    canvas.create_line   (x + data.gateWidth                       ,
                          y + data.gateHeight/2                    ,
                          x + data.gateWidth + data.gateLineLen/2,
                          y + data.gateHeight/2                    ,
                          fill = 'red')
    canvas.create_line   (x + data.gateWidth   +  data.gateCircleD  ,
                          y + data.gateHeight/2 - data.gateCircleR  ,
                          x + data.gateWidth   +  data.gateCircleD  ,
                          y + data.gateHeight/2 + data.gateCircleR  ,
                          fill = 'red')
    canvas.create_line   (x                     , y + data.gateHeight/2,
                          x - data.gateLineLen/2, y + data.gateHeight/2,
                          fill = 'green')
    canvas.create_line   (x - data.gateCircleD, 
                          y + data.gateHeight/2 - data.gateCircleR,
                          x - data.gateCircleD, 
                          y + data.gateHeight/2 + data.gateCircleR,
                          fill = 'green')

def drawSingleOrGate(canvas, data, x, y):
    canvas.create_arc    (x + 2*data.margin - data.gateWidth, y,
                          x + data.gateWidth, y + data.gateHeight,
                         start = 270, extent = 180, 
                         outline = 'black', style = 'arc')
    canvas.create_arc    (x - data.margin, y, 
                          x + data.margin, y + data.gateHeight,
                         start = 270, extent = 180, style = 'arc')
    canvas.create_line   (x, y, x + data.margin, y)
    canvas.create_line   (x, y + data.gateHeight, 
                          x + data.margin, y + data.gateHeight)
    canvas.create_line   (x + data.gateWidth,
                          y + data.gateHeight/2                    ,
                          x + data.gateWidth + data.gateLineLen/2  ,
                          y + data.gateHeight/2                    ,
                          fill = 'red')
    canvas.create_line   (x + data.gateWidth + 2*data.gateCircleR   ,
                          y + data.gateHeight/2 - data.gateCircleR  ,
                          x + data.gateWidth + 2*data.gateCircleR   ,
                          y + data.gateHeight/2 + data.gateCircleR  ,
                          fill = 'red')
    canvas.create_line   (x + data.gateLineLen/2, y + data.gateHeight/3,
                          x - data.gateLineLen/2, y + data.gateHeight/3,
                          fill = 'green')
    canvas.create_line   (x - data.gateCircleD, 
                          y + data.gateHeight/3 - data.gateCircleR,
                          x - data.gateCircleD, 
                          y + data.gateHeight/3 + data.gateCircleR,
                          fill = 'green')
    canvas.create_line   (x + data.gateLineLen/2, y + 2*data.gateHeight/3,
                          x - data.gateLineLen/2, y + 2*data.gateHeight/3,
                          fill = 'green')
    canvas.create_line   (x - data.gateCircleD, 
                          y + 2*data.gateHeight/3 - data.gateCircleR,
                          x - data.gateCircleD, 
                          y + 2*data.gateHeight/3 + data.gateCircleR,
                          fill = 'green')

def drawSingleAndGate(canvas, data, x, y):
    canvas.create_arc    (x + 2*data.margin - data.gateWidth, y,
                          x + data.gateWidth, y + data.gateHeight,
                         start = 270, extent = 180, style = 'arc')
    canvas.create_line   (x, y, x, y + data.gateHeight)
    canvas.create_line   (x, y, x + data.margin, y)
    canvas.create_line   (x, y + data.gateHeight, 
                          x + data.margin, y + data.gateHeight)
    canvas.create_line   (x + data.gateWidth,
                          y + data.gateHeight/2                    ,
                          x + data.gateWidth + data.gateLineLen/2  ,
                          y + data.gateHeight/2                    ,
                          fill = 'red')
    canvas.create_line   (x + data.gateWidth + 2*data.gateCircleR   ,
                          y + data.gateHeight/2 - data.gateCircleR  ,
                          x + data.gateWidth + 2*data.gateCircleR   ,
                          y + data.gateHeight/2 + data.gateCircleR  ,
                          fill = 'red')
    canvas.create_line   (x                     , y + data.gateHeight/3,
                          x - data.gateLineLen/2, y + data.gateHeight/3,
                          fill = 'green')
    canvas.create_line   (x - data.gateCircleD, 
                          y + data.gateHeight/3 - data.gateCircleR,
                          x - data.gateCircleD, 
                          y + data.gateHeight/3 + data.gateCircleR,
                          fill = 'green')
    canvas.create_line   (x                     , y + 2*data.gateHeight/3,
                          x - data.gateLineLen/2, y + 2*data.gateHeight/3,
                          fill = 'green')
    canvas.create_line   (x - data.gateCircleD,
                          y + 2*data.gateHeight/3 - data.gateCircleR,
                          x - data.gateCircleD, 
                          y + 2*data.gateHeight/3 + data.gateCircleR,
                          fill = 'green')

def drawSingleInputGate(canvas, data, x, y):
    canvas.create_oval(x - data.dotR, y - data.dotR,
                       x + data.dotR, y + data.dotR,
                       fill = 'black', outline = 'purple', width = 2)
    canvas.create_line(x + data.dotR, y, x + data.margin, y, fill = 'purple')

def drawTrueInputGate(canvas, data, x, y):
    canvas.create_oval(x - data.dotR, y - data.dotR,
                       x + data.dotR, y + data.dotR,
                       fill = 'red', outline = 'purple', width = 2)
    canvas.create_line(x + data.dotR, y, x + data.margin, y, fill = 'purple')

def drawSingleOutputGate(canvas, data, x, y):
    canvas.create_oval(x - data.dotR, y - data.dotR,
                       x + data.dotR, y + data.dotR,
                       fill = 'black', outline = 'green', width = 2)
    canvas.create_line(x - data.dotR, y, x - data.margin, y, fill = 'green')

def drawTrueOutputGate(canvas, data, x, y):
    canvas.create_oval(x - data.dotR, y - data.dotR,
                       x + data.dotR, y + data.dotR,
                       fill = 'red', outline = 'green', width = 2)
    canvas.create_line(x - data.dotR, y, x - data.margin, y, fill = 'green')

def drawAllGates(canvas, data):
    for i in range(len(data.gateList)):
        currentGate = data.gateList[i]
        if currentGate.placed == False:
            continue
        if currentGate.gateType == 'not':
            drawSingleNotGate(canvas, data, currentGate.x, currentGate.y)
        elif currentGate.gateType == 'or':
            drawSingleOrGate(canvas, data, currentGate.x, currentGate.y)
        elif currentGate.gateType == 'and':
            drawSingleAndGate(canvas, data, currentGate.x, currentGate.y)
        elif currentGate.gateType == 'input':
            if currentGate.outputValue == True:
                drawTrueInputGate(canvas, data, currentGate.x, currentGate.y)
            else:
                drawSingleInputGate(canvas, data, currentGate.x, currentGate.y)
        elif currentGate.gateType == 'output':
            if currentGate.outputValue == True:
                drawTrueOutputGate(canvas, data, currentGate.x, currentGate.y)
            else:
                drawSingleOutputGate(canvas, data, currentGate.x, currentGate.y)

def drawAllLines(canvas, data):
    for gate in data.gateList:
        if gate.gateType == 'input':
            startX = gate.x + 2 * data.dotR
            startY = gate.y
        elif gate.gateType == 'output':
            startX = gate.x - 2 * data.dotR
            startY = gate.y
        else:
            startX = gate.x + data.gateWidth + 2*data.gateCircleR
            startY = gate.y + data.gateHeight/2
        for outputGate in gate.getOutputGates():
            if outputGate.gateType == 'and' or outputGate.gateType == 'or':
                if outputGate.inputGates[0] == gate:
                    endY = outputGate.y + data.gateHeight/3
                else:
                    endY = outputGate.y + 2*data.gateHeight/3
            elif outputGate.gateType == 'not':
                endY = outputGate.y + data.gateHeight/2
            else:endY = outputGate.y
            endX = outputGate.x - data.gateCircleD
            if gate.outputValue == True:
                canvas.create_line(startX, startY,
                               endX  , endY, fill = 'red')
            else:canvas.create_line(startX, startY,
                               endX  , endY)

def saveFile(data):
    information = ''
    for index in range(len(data.gateList)):
        information += (str(index)+data.gateList[index].gateType+':')
        information += str(data.gateList[index].x)+','\
                      +str(data.gateList[index].y)
        for gate in data.gateList[index].outputGates:
            information += (','+str(data.gateList.index(gate))+gate.gateType)
        information += '\n'
    information = information[0:-1]
    with open('information.txt', "wt") as f:
        f.write(information)


def readFile(data):
    init(data)
    with open('information.txt', "rt") as f:
        info = f.read()
    lines = info.split('\n')
    data.gateList = [None] * len(lines)
    for linei in lines:
        gate = linei.split(':')[0]
        gateInfo = linei.split(':')[1].split(',')
        addressX = gateInfo[0]
        addressY = gateInfo[1]
        data.gateList[int(gate[0])] = Gate(gate[1:])
        data.gateList[int(gate[0])].x = int(addressX)
        data.gateList[int(gate[0])].y = int(addressY)
    for linej in lines:
        gate = linej.split(':')[0]
        gateInfo = linej.split(':')[1].split(',')
        if len(gateInfo) == 2: outputGates = []
        else:outputGates = gateInfo[2:]
        for outputGate in outputGates:
            data.gateList[int(gate[0])].\
            connectTo(data.gateList[int(outputGate[0])])
    for gate in data.gateList:
        gate.placed = True

def mousePressedButton(event, data):
    if data.x1 < event.x < data.x1 + data.buttonWidth:
        init(data)
    elif data.x2 < event.x < data.x2 + data.buttonWidth:
        saveFile(data)
    elif data.x3 < event.x < data.x3 + data.buttonWidth:
        readFile(data)
    elif data.x4 < event.x < data.x4 + data.buttonWidth:
        data.isPowerOn = not data.isPowerOn
        for gate in data.gateList:
            if gate.gateType == 'input':
                gate.setInputValue(None, False)

def mousePressedCatalog(event, data):
    if data.isPlacingGate == True:
        data.gateList.pop()
    if data.toolbarHeight < event.y < data.y1:
        data.gateList.append(Gate('not'))
    elif data.y1 < event.y < data.y2:
        data.gateList.append(Gate('or'))
    elif data.y2 < event.y < data.y3:
        data.gateList.append(Gate('and'))
    elif data.y3 < event.y < data.y4:
        data.gateList.append(Gate('input'))
    elif data.y4 < event.y:
        data.gateList.append(Gate('output'))
    data.isPlacingGate = True

def mousePressedCanvas(event, data):
    data.gateList[-1].x = event.x
    data.gateList[-1].y = event.y
    if data.gateList[-1].gateType == 'input': 
        data.gateList[-1].x = data.catalogWidth + data.dotR
    if data.gateList[-1].gateType == 'output': 
        data.gateList[-1].x = data.width - data.dotR
    data.gateList[-1].placed = True
    data.isPlacingGate = False

def mousePressedItem1(event, data):
    for gate in data.gateList:
        if gate.x-data.margin<event.x<gate.x+data.gateWidth+data.margin and\
           gate.y-data.margin<event.y<gate.y+data.gateHeight+data.margin:
           data.isPlacingLine = True
           data.lineStart = gate

def mousePressedItem2(event, data):
    for gate in data.gateList:
        if gate.x-data.margin<event.x<gate.x+data.gateWidth+data.margin and\
           gate.y-data.margin<event.y<gate.y+data.gateHeight+data.margin:
            data.isPlacingLine = False
            data.lineEnd = gate
            data.lineStart.connectTo(data.lineEnd)
        else:
            data.isPlacingLine = False

def mousePressedSwitch(event, data):
    for gate in data.gateList:
        if gate.gateType == 'input':
            if gate.x - data.margin < event.x < gate.x + data.margin and\
               gate.y - data.margin < event.y < gate.y + data.margin:
                if gate.outputValue == True:
                    gate.setInputValue(None, False)
                else:
                    gate.setInputValue(None, True)

def mousePressed(event, data):
    if 0 < event.y < data.toolbarHeight:
        mousePressedButton(event, data)
    if 0 < event.x < data.catalogWidth and data.isPowerOn == False:
        mousePressedCatalog(event, data)
    if data.catalogWidth  < event.x < data.width  and\
       data.toolbarHeight < event.y < data.height and data.isPowerOn == False:
        if data.isPlacingGate == True:
            mousePressedCanvas(event, data)
        elif data.isPlacingLine == False:
            mousePressedItem1(event, data)
        elif data.isPlacingLine == True:
            mousePressedItem2(event, data)
    if data.isPowerOn == True:
        mousePressedSwitch(event, data)



def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawCanvas(canvas, data)
    drawLables(canvas, data)
    drawButtons(canvas, data)
    drawAllGates(canvas, data)
    drawAllLines(canvas, data)


def run(width=1000, height=500):
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


def testGateClass1_inputToOutput():
    # Connect and input gate to an output gate
    in1 = Gate("input")
    out1 = Gate("output")
    in1.connectTo(out1);
    assert(in1.getInputGates() == [ ])
    assert(in1.getMaxInputGates() == 0)
    assert(in1.getOutputGates() == [ out1 ])
    assert(out1.getInputGates() == [ in1 ])
    assert(out1.getMaxInputGates() == 1)
    assert(out1.getOutputGates() == [ ])
    assert(in1.inputValues == None)
    assert(in1.outputValue == None)
    assert(out1.inputValues == None)
    assert(out1.outputValue == None)
    # now set the input to True
    in1.setInputValue(None, True)
    assert(in1.inputValues == { None:True})
    assert(in1.outputValue == True)
    assert(out1.inputValues == { in1:True})
    assert(out1.outputValue == True)
    # and set the input to False
    in1.setInputValue(None, False)
    assert(in1.inputValues == { None:False})
    assert(in1.outputValue == False)
    assert(out1.inputValues == { in1:False})
    assert(out1.outputValue == False)

def testGateClass2_oneNotGate():
    in1 = Gate("input")
    out1 = Gate("output")
    not1 = Gate("not")
    in1.connectTo(not1)
    not1.connectTo(out1)
    assert(out1.outputValue == None)
    in1.setInputValue(None, False)
    assert(not1.inputValues == { in1:False })
    assert(out1.inputValues == { not1:True })
    assert(out1.outputValue == True)
    in1.setInputValue(None, True)
    assert(not1.inputValues == { in1:True })
    assert(out1.inputValues == { not1:False })
    assert(out1.outputValue == False)

def testGateClass3_oneAndGate():
    in1 = Gate("input")
    in2 = Gate("input")
    out1 = Gate("output")
    and1 = Gate("and")
    in1.connectTo(and1)
    in2.connectTo(and1)
    and1.connectTo(out1)
    assert(out1.outputValue == None)
    in1.setInputValue(None, False)
    assert(and1.inputValues == { in1:False })
    assert(and1.outputValue == None) # not ready, need both inputs
    in2.setInputValue(None, False)
    assert(and1.inputValues == { in1:False, in2:False })
    assert(and1.outputValue == False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    assert(and1.inputValues == { in1:True, in2:False })
    assert(out1.outputValue == False)

    in2.setInputValue(None, True)
    assert(and1.inputValues == { in1:True, in2:True })
    assert(out1.outputValue == True)

def testGateClass4_oneOrGate():
    in1 = Gate("input")
    in2 = Gate("input")
    out1 = Gate("output")
    or1 = Gate("or")
    in1.connectTo(or1)
    in2.connectTo(or1)
    or1.connectTo(out1)
    assert(out1.outputValue == None)
    in1.setInputValue(None, False)
    assert(or1.inputValues == { in1:False })
    assert(or1.outputValue == None) # not ready, need both inputs
    in2.setInputValue(None, False)
    assert(or1.inputValues == { in1:False, in2:False })
    assert(or1.outputValue == False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    assert(or1.inputValues == { in1:True, in2:False })
    assert(out1.outputValue == True)

    in2.setInputValue(None, True)
    assert(or1.inputValues == { in1:True, in2:True })
    assert(out1.outputValue == True)

def testGateClass5_xor():
    in1 = Gate("input")
    in2 = Gate("input")
    out1 = Gate("output")
    and1 = Gate("and")
    and2 = Gate("and")
    not1 = Gate("not")
    not2 = Gate("not")
    or1 = Gate("or")
    in1.connectTo(and1)
    in1.connectTo(not1)
    in2.connectTo(and2)
    in2.connectTo(not2)
    not1.connectTo(and2)
    not2.connectTo(and1)
    and1.connectTo(or1)
    and2.connectTo(or1)
    or1.connectTo(out1)

    in1.setInputValue(None, False)
    in2.setInputValue(None, False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    in2.setInputValue(None, False)
    assert(out1.outputValue == True)

    in1.setInputValue(None, False)
    in2.setInputValue(None, True)
    assert(out1.outputValue == True)

    in1.setInputValue(None, True)
    in2.setInputValue(None, True)
    assert(out1.outputValue == False)

def testGateClass():
    print("Testing Gate class... ", end="")
    testGateClass1_inputToOutput()
    testGateClass2_oneNotGate()
    testGateClass3_oneAndGate()
    testGateClass4_oneOrGate()
    testGateClass5_xor()
    print("Passed!")

testGateClass()
run()