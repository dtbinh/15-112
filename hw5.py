# hw5.py
# Hanzhou Lu / hanzhoul / II
import math
import string

def isGoodSquare(a): #n*n, no-empty, different integers
    rows = len(a)
    if rows == 0: return False
    for row in range(rows):
    #check if it is a 2d-list which length of each row is the same
        if type(a[row]) != list or len(a[0]) != len(a[row]):
            return False
    cols = len(a[0])
    if cols != rows: return False    #check if it is a square
    numList = []
    for i in range(rows):            #check no integer occurs more than once
        for j in range(rows):
            if type(a[i][j]) != int: return False #check all are integers
            numList += [a[i][j]]
    for j in numList:
        if numList.count(j) != 1: return False
    return True

def isMagicSquare(a):
    if not isGoodSquare(a): return False
    rows = len(a)
    addUp = sum(a[0])
    diagonals1 = 0    #sum of nums in each diagonals
    diagonals2 = 0  
    for row in range(rows):
        if sum(a[row]) != addUp: return False    #check each row
        sumOfCol = 0
        for col in range(rows):
            sumOfCol += a[row][col]
        if sumOfCol != addUp: return False       #check each col
        diagonals1 += a[row][row]
        diagonals2 += a[row][-(row+1)]
    if diagonals1 != addUp or diagonals2 !=addUp:#check diagonals
        return False
    return True

def isKingsTour(board):
    rows = len(board)
    cols = rows
    checkbox = [None]*(rows**2+1)    #put loction of each step in this list
    checkbox[0] = False
    for i in range(rows):            #check all are legal number
        for j in range(cols):
            if board[i][j]>rows**2 or checkbox[board[i][j]] != None:
                return False
            else:
                checkbox[board[i][j]] = [i,j]
    for k in range(1,rows**2):       #check if each move is adjacent and step=1
        if abs(checkbox[k][0]-checkbox[k+1][0]) > 1 or\
           abs(checkbox[k][1]-checkbox[k+1][1]) > 1:
            return False
    return True

def areLegalValues(values):
    checkbox = [False]*(len(values)+1)     #1.values are from 1 to N^2
    for i in range(len(values)):           #2.each value(except 0) occurs once
        if values[i] > len(values) or\
        (values[i] != 0 and checkbox[values[i]] != False):
            return False
        checkbox[values[i]] = True
    return True

def isLegalRow(board, row):
    checkRow = board[row]
    return areLegalValues(checkRow)

def isLegalCol(board, col):
    checkCol = []
    for i in range(len(board)):
        checkCol.append(board[i][col])
    return areLegalValues(checkCol)

def isLegalBlock(board, block):
    checkBlock = []                    #blocks are in a n*n cube
    N = round(len(board)**0.5)
    blockLocationX = block // N        #row of the block in n*n cube
    blockLocationY = block %  N        #col of the block in n*n cube
    for row in range(blockLocationX*N,(blockLocationX+1)*N):
        for col in range(blockLocationY*N,(blockLocationY+1)*N):
            checkBlock.append(board[row][col])
    return areLegalValues(checkBlock)

def isLegalSudoku(board):
    for i in range(len(board)):                 #check each row, col, bolck
        if isLegalBlock(board,i) != True or\
           isLegalRow(board,i)   != True or\
           isLegalCol(board,i)   != True:
            return False
    return True

def wordSearch(board, word):
    (rows, cols) = (len(board), len(board[0]))
    for row in range(rows):
        for col in range(cols):
            result = wordSearchFromCell(board, word, row, col)
            if (result != None):
                return result
    return None

def wordSearchFromCell(board, word, startRow, startCol):
    for dir in range(8):
        result = wordSearchFromCellInDirection(board, word,
                                               startRow, startCol, dir)
        if (result != None):
            return result
    return None

def wordSearchFromCellInDirection(board, word, startRow, startCol, dir):
    (rows, cols) = (len(board), len(board[0]))
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    # dirNames = [ "up-left"  ,   "up", "up-right",
    #              "left"     ,         "right",
    #              "down-left", "down", "down-right" ]
    (drow,dcol) = dirs[dir]    
    for i in range(len(word)):
        row = startRow + i*drow
        col = startCol + i*dcol
        if ((row < 0) or (row >= rows) or
            (col < 0) or (col >= cols) or
            (board[row][col] != word[i])):
            return None
    return ([startRow, startCol, dir])

def findBestLocation(board,word):
    bestLocation = [len(word)   ,len(board)  ,len(board)  ,8]
    #              [bestCost    ,bestStartRow,bestStartCol,bestDirection]
    #               set the origin 'best' to the worst state
    for i in range(2**len(word)):          #'0b101010'
        binaryNum = bin(i)[2:]             #  '101010'
        binaryList = ['0']*(len(word)-len(binaryNum)) + list(binaryNum)
        cost = binaryList.count('0')
        testWord = ''
        for j in range(len(word)):         #word'abcd'--> 'a-cd','ab-d'......
            if binaryList[j] == '0':
                testWord += '-'
            else:
                testWord += word[j]
        result = wordSearch(board,testWord)#search test word and chose one
        if result == None: continue        #with least cost,cow,row dir
        elif [cost] + result < bestLocation:
            bestLocation = [cost] + result
    return bestLocation+[word]

def addWord(board,bestLocation):
    word = bestLocation[-1]          #'4' is the location of word in the list
    if bestLocation[:-1] == [len(word),len(board),len(board),8]:
    #which means word cannot fit the current board
        for i in range(len(board)):
            board[i].append('-')
        board += [['-']*len(board[0])]   #add one row and one col
        bestLocation = [len(word),len(board)-1,0,4,word] 
        #put word in the new row and to the right(dir = 4)
    startRow = bestLocation[1]
    startCol = bestLocation[2]
    direction = bestLocation[3]
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[direction] 
    for j in range(len(word)):               #replace the '-' with word
        board[startRow+drow*j][startCol+dcol*j] = word[j]

def makeWordSearch(wordList, replaceEmpties):
    board = []
    if wordList == []: return None
    for i in range(len(wordList[0])):          #get a n*n square
        board += [['-']*len(wordList[0])]
    for j in range(len(wordList[0])):          #first row = first word
        board[0][j] = wordList[0][j]
    for word in wordList[1:]:                  #add each word in the list
        bestLocation = findBestLocation(board,word)
        addWord(board,bestLocation)
    if replaceEmpties == False:
        return board
    else:
        complementEmptyCell(board)
        return board

def complementEmptyCell(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '-':
                for letter in string.ascii_lowercase:
                    word = '-'+letter
                    if wordSearchFromCell(board, word, i, j) == None:
                        board[i][j] = letter
                        break


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
def testIsGoodSquare():
    print("Testing isGoodSquare()...", end="")
    assert(isGoodSquare([42]) == False)
    assert(isGoodSquare([[42]]) == True)
    assert(isGoodSquare([[1,2],[3,'4']]) == False)
    assert(isGoodSquare([[23,28,21],[22,24,26],[27,25]]) == False)
    assert(isGoodSquare([[23,28,21],[22,24,26],[27,20,25]]) == True)
    print("Passed. ")

def testIsMagicSquare():
    print("Testing isMagicSquare()...", end="")
    assert(isMagicSquare([[2,7,6],[9,5,1],[4,3,8]]) == True)
    assert(isMagicSquare([[7,12,1,14],[2,13,8,11],
                          [16,3,10,5],[9,6,15,4]]) == True)
    assert(isMagicSquare([[1,2],[3,4]]) == False)
    assert(isMagicSquare([[23,28,21],[22,24,26],[27,21,25]]) == False)
    assert(isMagicSquare([[23,28,21],[22,24,26],[27,20,25]]) == True)
    print("Passed. ")

def testIsKingsTour():
    print("Testing isKingsTour()...", end="")
    assert(isKingsTour([[3,2,1],[6,4,9],[5,7,8]]) == True)
    assert(isKingsTour([[1,2,3],[7,4,8],[6,5,9]]) == False)
    assert(isKingsTour([[3,2,1],[6,4,0],[5,7,8]]) == False)
    assert(isKingsTour([[4,3,2],[7,5,10],[6,8,9]]) == False)
    assert(isKingsTour([[1,14,15,16],[13,2,7,6],
                        [12,8,3,5],[11,10,9,4]]) == True)
    print("Passed. ")

def testAreLegalValues():
    print("Testing areLegalValues()...", end="")
    assert(areLegalValues([1,2,3,4,5,6,7,8,9]) == True)
    assert(areLegalValues([1,2,3,4,5,6,10,8,9]) == False)
    assert(areLegalValues([1,2,3,0,5,5,0,8,0]) == False)
    assert(areLegalValues([0,0,0,0,8,0,0,7,9]) == True)
    print("Passed. ")

board=[
  [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
  [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
  [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
  [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
  [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
  [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
  [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
  [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
  [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
]

def testIsLegalRow():
    global board
    print("Testing isLegalRow()...", end="")
    assert(isLegalRow(board,0) == True)
    assert(isLegalRow(board,8) == True)
    assert(isLegalRow([[1,2,3],[4,5,6],[7,8,9]],1) == False)
    assert(isLegalRow([[1,2,3],[4,5,6],[7,8,9]],2) == False)
    print("Passed. ")

def testIsLegalCol():
    global board
    print("Testing isLegalCol()...", end="")
    assert(isLegalCol(board,0) == True)
    assert(isLegalCol(board,8) == True)
    assert(isLegalCol([[1,2,3],[4,5,6],[7,8,9]],1) == False)
    assert(isLegalCol([[1,2,3],[4,5,6],[7,8,9]],2) == False)
    print("Passed. ")

def testIsLegalBlock():
    global board
    print("Testing isLegalBlock()...", end="")
    assert(isLegalBlock(board,0) == True)
    assert(isLegalBlock(board,8) == True)
    assert(isLegalBlock([[1,14,15,16],[13,2,7,6],
                         [12,8,3,5],[11,10,9,4]],1) == False)
    assert(isLegalBlock([[1,14,15,16],[13,2,7,6],
                         [12,8,3,5],[11,10,9,4]],2) == False)
    print("Passed. ")

def testIsLegalSudoku():
    global board
    print("Testing isLegalRow()...", end="")
    assert(isLegalSudoku(board) == True)
    assert(isLegalSudoku([[1,14,15,16],[13,2,7,6],
                        [12,8,3,5],[11,10,9,4]]) == False)
    print("Passed. ")

def testWordSearch():
    print("Testing wordSearch()...", end="")
    board = [ [ 'd', 'o', 'g' ],
              [ 't', 'a', 'c' ],
              [ 'o', 'a', 't' ],
              [ 'u', 'r', 'k' ],
            ]
    assert(wordSearch(board, "dog") == [0, 0, 4])
    assert(wordSearch(board, "cat") == [1, 2, 3])
    assert(wordSearch(board, "tad") == [2,2,0])
    assert(wordSearch(board, "cow") == None)
    print("Passed. ")

def testAddWord():
    board=[['-','-','-'],['-','-','-'],['-','-','-']]
    print("Testing addWord()...", end="")
    addWord(board,[2,0,0,4,'abc'])
    assert(board==[['a','b','c'],['-','-','-'],['-','-','-']])
    addWord(board,[4,3,3,8,'abcd'])
    assert(board==[['a','b','c','-'],['-','-','-','-'],\
        ['-','-','-','-'],['a','b','c','d']])
    print("Passed. ")

def testFindBestLocation():
    print("Testing findBestLocation()...", end="")
    board = [ [ 'd', 'o', '-' ],
              [ 't', '-', '-' ],
              [ '-', 'v', '-' ],
              [ '-', '-', '-' ],
            ]
    assert(findBestLocation(board,'dog')==[1,0,0,4,'dog'])
    assert(findBestLocation(board,'vs')==[1,2,1,1,'vs'])
    print("Passed. ")

def testComplementEmptyCell():
    print("Testing complementEmptyCell()...", end="")
    board = [['a', 'b', 'c'], ['-', '-', '-'], ['-', '-', '-']]
    complementEmptyCell(board)
    assert(board == [['a', 'b', 'c'], ['c', 'd', 'a'], ['a', 'b', 'c']])
    board = [['a', 'b', 'c'], ['d', 'e', '-'], ['c', 'f', 'g']]
    complementEmptyCell(board)
    assert(board == [['a', 'b', 'c'], ['d', 'e', 'a'], ['c', 'f', 'g']])
    print("Passed. ")

def testMakeWordSearch():
    print("Testing makeWordSearch()...", end="")
    board = makeWordSearch([], False)
    assert(board == None)

    board = makeWordSearch(["ab"], False)
    assert(board == [['a', 'b'], ['-', '-'] ])
    board = makeWordSearch(["ab"], True)
    assert(board == [['a', 'b'], ['c', 'd'] ])
    board = makeWordSearch(["ab", "bc", "cd"], False)
    assert(board == [['a', 'b'], ['c', 'd'] ])
    board = makeWordSearch(["ab", "bc", "cd", "de"], False)
    assert(board == [['a', 'b', '-'], ['c', 'd', '-'], ['d', 'e', '-']])
    board = makeWordSearch(["ab", "bc", "cd", "de"], True)
    assert(board == [['a', 'b', 'a'], ['c', 'd', 'c'], ['d', 'e', 'a']])

    board = makeWordSearch(["abc"], False)
    assert(board == [['a', 'b', 'c'], ['-', '-', '-'], ['-', '-', '-']])
    board = makeWordSearch(["abc"], True)
    assert(board == [['a', 'b', 'c'], ['c', 'd', 'a'], ['a', 'b', 'c']])

    board = makeWordSearch(["abc", "adc", "bd", "bef", "gfc"], False)
    assert(board == [['a', 'b', 'c'], ['d', 'e', '-'], ['c', 'f', 'g']])
    board = makeWordSearch(["abc", "adc", "bd", "bef", "gfc"], True)
    assert(board == [['a', 'b', 'c'], ['d', 'e', 'a'], ['c', 'f', 'g']])

    print("Passed.")


testIsGoodSquare()
testIsMagicSquare()
testIsKingsTour()
testAreLegalValues()
testIsLegalRow()
testIsLegalCol()
testIsLegalBlock()
testIsLegalSudoku()
testAddWord()
testFindBestLocation()
testComplementEmptyCell()
testWordSearch()
testMakeWordSearch()