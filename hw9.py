# hw9.py
# Hanzhou Lu / hanzhoul / II

import os

def findLargestFile(path):
    largestFile = (0,None)
    def addLargestFile(path):             #compare file size with largest size
        nonlocal largestFile
        if (os.path.isdir(path) == False):
            fileSize = os.path.getsize(path)
            if fileSize > largestFile[0]: #replace largest size with curr size
                largestFile = (fileSize, path)
            elif fileSize == largestFile[0]: #tie
                largestFile = (fileSize,(largestFile[1],path))
        else:
            for nestedFile in os.listdir(path):
                addLargestFile(path + '/' + nestedFile)
    addLargestFile(path)
    if largestFile == (0,None): return '' #empty folder
    return(largestFile[1])


def flatten(L):
    if type(L) != list : return L        #base case: deepist list
    elif len(L) == 0: return []          #base case: empty list
    if type(L[0]) != list:
        return [L[0]] + flatten(L[1:])   #recursion: not a list
    else:
        return flatten(L[0]) + flatten(L[1:]) #recursion: list

def isPrime(n, factor=2):
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = round(n**0.5)
    for factor in range(3,maxFactor+1,2):
        if (n % factor == 0):
            return False
    return True


def findRTP(digits, guess = 2):
    if isPrime(guess):
        if len(str(guess)) == digits:       #base case: get the right number
            return guess
    for newNum in range(0,10):              #single number irerates from 0 to 9 
        if isPrime(guess * 10 + newNum):    #if guess is right
            newGuess = findRTP(digits, guess * 10 + newNum)
            if newGuess != None:            #if next guess is right
                return newGuess
    return None

def getCourse(courseCatalog, courseNumber):
    parentCourse = courseCatalog[0]
    if len(courseCatalog) <= 1:
        return None
    elif type(courseCatalog[1]) == list:  #point a list
        subCourse = getCourse(courseCatalog[1], courseNumber)
        if subCourse != None:             #see if next element is courseNumber
            return parentCourse + '.' + subCourse
        else:                             #if not, delete the element
            return getCourse([parentCourse] + courseCatalog[2:], courseNumber)
    elif courseCatalog[1] == courseNumber:#base case: get the couesrNumber
        return parentCourse + '.' + courseNumber
    else:                                 #if not, delete the element
        return getCourse([parentCourse] + courseCatalog[2:], courseNumber)

def noError(f):
    def g(*args):
        try:
            return f(*args)
        except:
            return None
    return g

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testFindLargestFile():
    print("Testing findLargestFile()...", end="")
    assert(findLargestFile("sampleFiles/folderA") ==
                       "sampleFiles/folderA/folderC/giftwrap.txt")
    assert(findLargestFile("sampleFiles/folderB") ==
                       "sampleFiles/folderB/folderH/driving.txt")
    assert(findLargestFile("sampleFiles/folderB/folderF") == "")
    print("Passed. ")

def testFlatten():
    print("Testing flatten()...", end="")
    assert(flatten([1,[2]]) == [1,2])
    assert(flatten([1,2,[3,[4,5],6],7]) == [1,2,3,4,5,6,7])
    assert(flatten(['wow', [2,[[]]], [True]]) == ['wow', 2, True])
    assert(flatten([]) == [])
    assert(flatten([[]]) == [])
    assert(flatten(3) == 3)
    print("Passed. ")

def testFindRTP():
    print("Testing findRTP()...", end="")
    assert(findRTP(2) == 23)
    assert(findRTP(3) == 233)
    assert(findRTP(7) == 2339933)
    assert(findRTP(8) == 23399339)
    print("Passed. ")


def testGetCourse():
    print("Testing getCourse()...", end="")
    courseCatalog = ["CMU",
                        ["CIT",
                            [ "ECE", "18-100", "18-202", "18-213" ],
                            [ "BME", "42-101", "42-201" ],
                        ],
                        ["SCS",
                            [ "CS", 
                              ["Intro", "15-110", "15-112" ],
                              "15-122", "15-150", "15-213"
                            ],
                        ],
                        "99-307", "99-308"
                    ]
    assert(getCourse(courseCatalog, "18-100") == "CMU.CIT.ECE.18-100")
    assert(getCourse(courseCatalog, "15-112") == "CMU.SCS.CS.Intro.15-112")
    assert(getCourse(courseCatalog, "15-213") == "CMU.SCS.CS.15-213")
    assert(getCourse(courseCatalog, "99-307") == "CMU.99-307")
    assert(getCourse(courseCatalog, "15-251") == None)
    print("Passed. ")

def testNoErrorDecorator():
    print("Testing @noError decorator...", end="")

    @noError
    def f(x, y): return x/y
    assert(f(1, 5) == 1/5)
    assert(f(1, 0) == None)

    @noError
    def g(): return 1/0
    assert(g() == None)

    @noError
    def h(n):
        if (n == 0): return 1
        else: return h(n+1)
    assert(h(0) == 1)
    assert(h(-1) == 1)
    assert(h(1) == None)

    print("Passed!")

testNoErrorDecorator()
testFindLargestFile()
testFlatten()
testFindRTP()
testGetCourse()



from tkinter import *

def init(data):
    data.level = 0

def drawSingleHFractal(canvas, x, y, w, h, level):
    if level > -1:
        canvas.create_line(  x,   y,   x, y+h)
        canvas.create_line(x+w,   y, x+w,y+h)
        canvas.create_line(  x, y+h/2,x+w, y+h/2)
        drawSingleHFractal(canvas, x -   w/4, y -   h/4, w/2, h/2, level-1)
        drawSingleHFractal(canvas, x + 3*w/4, y -   h/4, w/2, h/2, level-1)
        drawSingleHFractal(canvas, x -   w/4, y + 3*h/4, w/2, h/2, level-1)
        drawSingleHFractal(canvas, x + 3*w/4, y + 3*h/4, w/2, h/2, level-1)

def keyPressed(event, data):
    if (event.keysym in ["Up", "Right"]):
        data.level += 1
    elif ((event.keysym in ["Down", "Left"]) and (data.level > 0)):
        data.level -= 1

def mousePressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawSingleHFractal(canvas, data.width/4, data.height/4, 
                               data.width/2, data.height/2, data.level)

def run(width=800, height=500):
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

def hFractal():
    run()

hFractal()
