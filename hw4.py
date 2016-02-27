# hw4.py
# Hanzhou Lu / hanzhoul / II
import math
import string

def lookAndSay(a):
    if a==[]: return []
    result=[]
    startIndex=0
    currentNum=a[0]
    for n in range(len(a)):
        if a[n]!=currentNum:             #When number is different, put
            lenth=len(a[startIndex:n])   #new number into currentNum
            result+=[(lenth,currentNum)]
            currentNum=a[n]
            startIndex=n
        if n==len(a)-1:                  #Count the last consecutive numbers
            lenth=len(a[startIndex:])
            result+=[(lenth,currentNum)]
    return result

def inverseLookAndSay(a):
    result=[]
    for n in range(len(a)):
        (x,y)=a[n]
        for m in range(x):                #Append x same nums into result
            result.append(y)
    return result

def solvesCryptarithm(puzzle, solution):
    puzzle=puzzle+'.'       #Make sure that there is a signal after each number
    num=''
    numlist=[]
    for n in puzzle:
        if n.isalpha():
            if solution.find(n)==-1: return False
            num+=str(solution.find(n))
        else:                        #Numlist contains numbers in the equation,
            numlist.append(int(num)) #which the last number is the result
            num=''
    return sum(numlist[:-1])==numlist[-1]

def isSubset(a,b):            #Check if we can spell words with letters in hand
    for letter in string.ascii_lowercase:
        if a.count(letter)>b.count(letter):
            return False
    return True

def calculateScores(letterScores,words): #Calculte score of the words
    score=0
    for letter in words:
        score+=letterScores[ord(letter)-ord('a')]
    return score

def bestScrabbleScore(dictionary, letterScores, hand):
    result=('',0)
    (x,y)=result
    for words in dictionary:
        if isSubset(words,hand):
            score=calculateScores(letterScores,words)
            if y<score:                    #Save current max score,and the word
                x=words
                y=score
            elif y==score:                 #If there is a tie
                if type(x)==str:
                    x=[x,words] 
                else: x=x+[words]
    result=(x,y)
    if x=='':result=None
    return result

def getValues(s,args,L):        #Take values from list 'arg' and 'L'
    if s.startswith('A'):
        return args[int(s[1:])]
    elif s.startswith('L'):
        return L[int(s[1:])]
    else: return int(s)         #If the expression is an integer, return itself

def doOperator(line,args,L,currentLine):
    expr=line.split(' ')
    if len(expr)==2:            #L0 A0 : L0=A0
        L[int(expr[0][1:])]=getValues(expr[1],args,L)
    elif len(expr)==4:
        if expr[1]=='+':        #L0 + A0 1 : L0=A0+1 
            result=getValues(expr[2],args,L)+getValues(expr[3],args,L)
            #Get values of the operands
            L[int(expr[0][1:])]=result
        elif expr[1]=='-':      #L0 - A0 1 : L0=A0-1
            result=getValues(expr[2],args,L)-getValues(expr[3],args,L)
            L[int(expr[0][1:])]=result
    currentLine[0]=currentLine[0]+1  #Move to next line

def doJump(line,args,L,currentLine,lines):
    expr=line.split(' ')
    if len(expr)==2:                                        #JMP [label]
        currentLine[0]=lines.index(expr[1]+':') #Move to the line with [label]:
    if len(expr)==3:
        if expr[0][3]=='0' and getValues(expr[1],args,L)==0:#JMP+[expr][label]
            currentLine[0]=lines.index(expr[2]+':')
        elif expr[0][3]=='+' and getValues(expr[1],args,L)>0:#JMP0[expr][label]
            currentLine[0]=lines.index(expr[2]+':')
        else:currentLine[0]=currentLine[0]+1 #Move to next line

def doReturn(line,args,L):
    expr=line.split(' ')
    if len(expr)==2:
        return getValues(expr[1],args,L)
    if len(expr)==4:
        if expr[1]=='+':        #RTN + A0 1 
            result=getValues(expr[2],args,L)+getValues(expr[3],args,L)
            #Add values of the operands
        elif expr[1]=='-':      #RTN - A0 1
            result=getValues(expr[2],args,L)-getValues(expr[3],args,L)
            #Subtract values of the operands
        return result

def runSimpleProgram(program, args):
    L=[0]*999
    currentLine=[0]
    lines=program.splitlines()
    for n in range(len(lines)):
        lines[n]=lines[n].strip()
    while True:
        if lines[currentLine[0]].startswith('!'):           #! comment
            currentLine[0]=currentLine[0]+1
        elif lines[currentLine[0]].startswith('L'):         #L[N] [expr] 
            doOperator(lines[currentLine[0]],args,L,currentLine)
        elif lines[currentLine[0]].startswith('JMP'):       #JMP [label]
            doJump(lines[currentLine[0]],args,L,currentLine,lines)
        elif lines[currentLine[0]].islower():               #[label]:
            currentLine[0]=currentLine[0]+1
        elif lines[currentLine[0]].startswith('RTN'):       #RTN [expr]
            return doReturn(lines[currentLine[0]],args,L)

def approximate(a):          #Round number to four decimal places
    result=()
    for i in a:
        i=float('%0.4f' % i)
        result+=(i,)
    return result

def linearRegression(a):
    X,Y=[],[]
    SSxx,SSxy,SSdev,SSres=0,0,0,0
    for i in a:
        (x,y)=i
        X.append(x)
        Y.append(y)
    avgX=sum(X)/len(a)
    avgY=sum(Y)/len(a)
    for j in range(len(a)):
        SSxx+=(X[j]-avgX)**2          #SSxx = ∑(xi - avgx)^2
        SSxy+=(X[j]-avgX)*(Y[j]-avgY) #SSxy = ∑(xi - avgx)(yi - avgy)
    resulta=SSxy/SSxx                 #a=SSxy / SSxx
    resultb=avgY-resulta*avgX         #ŷ = ax + b
    for k in range(len(a)):
        SSdev+=(Y[k]-avgY)**2                   #SSdev = ∑(yi - avgy)^2
        SSres+=(Y[k]-resulta*X[k]-resultb)**2   #SSres = ∑(yi - ŷi)^2
    resultz=((SSdev-SSres)/SSdev)**0.5          #R^2 = (SSdev - SSres) / SSdev
    return approximate((resulta,resultb,resultz))

#Here is my bonus2. I am sooo sorry that I have no time to write enough comments
#and test function for my methods. Please don't score my style of the function 
#below. 

def calculateStDev(List):    
    total=0
    avg=sum(List)/len(List)
    for n in range(len(List)):
        total+=(List[n]-avg)**2
    result=(total/len(List))**0.5
    return result

def whichDateWrong(nomalizedDates,stdevOfThisPlayer):#Decide delete which num
    bestDev=stdevOfThisPlayer                        #can get the smallest dev
    for n in range(len(nomalizedDates)):  #Then the num must be wrong
        currentDev=calculateStDev(nomalizedDates[:n]+nomalizedDates[(n+1):])
        if currentDev<bestDev:
            bestDev=currentDev
            wrongPosition=n
    return wrongPosition+5     #The 5th element is 'atBats'

def bogusDataFinder(csvData):
    result=[]
    dateName=csvData.splitlines()[0].split(',')
    playerDate=csvData.splitlines()[1:]  #These are numbers calculated by excel
    avg=[2.812999474,0.325511967,0.673103259,0.13139149,0.01395318,0.082777645,\
    0.303924479,0.043262869,0.016248568,0.227486895,0.673206128,0.237396104]
    stdev=[0.895415672,0.163636,0.3140323,0.081937566,0.024036212,0.100295785,\
    0.180830264,0.066968342,0.023717614,0.142648775,0.281033374,0.054329877]
    for checkLine in playerDate:
        deltaDates,nomalizedDates=[],[]
        checkLine=checkLine.split(',')
        dates=checkLine[5:]        #The 5th element is atBats
        for n in range(len(dates)):
            dates[n]=float(dates[n])/int(checkLine[4]) #The 4th element is games
            deltaDates.append(dates[n]-avg[n])   #(X-avgX)
            nomalizedDates.append(deltaDates[n]/stdev[n])  #(X-avgX)/devX
        strongOrWeek=sum(nomalizedDates)/len(nomalizedDates)
        stdevOfThisPlayer=calculateStDev(nomalizedDates)
        if (stdevOfThisPlayer>2.1) or not (-1.81<strongOrWeek<1.65):
        #check if this player is TOO STRONG!:strongOrWeek > 1.65
        #      or this player is TOO WEAK!  :strongOrWeek <-1.81
        #      or this player's ability varies TOO MUCH!：stdevOfThisPlayer>2.1
            wrongDate=dateName[whichDateWrong(nomalizedDates,stdevOfThisPlayer)]
            result=[(checkLine[0],wrongDate)]+result
    return result

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testLookAndSay():
    print("Testing lookAndSay()...", end="")
    assert(lookAndSay([]) == [])
    assert(lookAndSay([1,1,1]) == [(3,1)])
    assert(lookAndSay([-1,2,7]) == [(1,-1),(1,2),(1,7)])
    assert(lookAndSay([3,3,8,-10,-10,-10]) == [(2,3),(1,8),(3,-10)])
    print("Passed. ")

def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
    assert(inverseLookAndSay(lookAndSay([-1,2,7])) == [-1,2,7])
    assert(inverseLookAndSay(lookAndSay([]))==[])
    print("Passed. ")

def testSolvesCryptarithm():
    print("Testing solvesCryptarithm()...", end="")
    assert(solvesCryptarithm("SEND+MORE=MONEY","OMY--ENDRS")==True)
    assert(solvesCryptarithm("D+D=V","-DV-------")==True)
    assert(solvesCryptarithm("D+D=V","-D-V------")==False)
    print("Passed. ")

def testIsSubset():
    print("Testing isSubset()...", end="")
    assert(isSubset('python',['p','y','t','h','o','n']) == True)
    assert(isSubset('pythonn',['p','y','t','h','o','n']) == False)
    print("Passed. ")

def testCalculateScores():
    print("Testing calculateScores()...", end="")
    letterScores=[
   #  a, b, c, d, e, f, g, h, i, j, k, l, m
      1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 10, 3,
   #  n, o, p, q, r, s, t, u, v, w, x, y, z
      1, 1, 3,10, 1, 1, 1, 1, 4, 4, 8, 4,10
   ]
    assert(calculateScores(letterScores,'aaa')==3)
    assert(calculateScores(letterScores,'abcd')==9)
    assert(calculateScores(letterScores,'qrs')==12)
    print("Passed. ")

def testBestScrabbleScore():
    dictionary=(list(string.ascii_lowercase))
    letterScores=[
   #  a, b, c, d, e, f, g, h, i, j, k, l, m
      1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 10, 3,
   #  n, o, p, q, r, s, t, u, v, w, x, y, z
      1, 1, 3,10, 1, 1, 1, 1, 4, 4, 8, 4,10
   ]
    hand=('a','b','c','l','q','z')
    print("Testing bestScrabbleScore()...", end="")
    assert(bestScrabbleScore(dictionary,letterScores,hand)==(['l','q','z'],10))
    assert(bestScrabbleScore(['a', 'b', 'c'], [1, 1, 1, 1, 1, 1, 1,\
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ['z'])==None)
    assert(bestScrabbleScore(['xyz', 'zxy', 'zzy', 'yy', 'yx', 'wow'], \
    [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1,\
     2, 3, 4, 5, 1], ['w', 'x', 'z'])==None)
    print("Passed. ")

def testGetValues():
    print("Testing getValues()...", end="")
    args=[1,2,3,4]
    L=[11,12,13,14]
    assert(getValues('A3',args,L)==4)
    assert(getValues('L2',args,L)==13)
    assert(getValues('123',args,L)==123)
    print("Passed. ")

def testDoOperator():
    print("Testing doOperator()...", end="")
    args=[1,2,3,4]
    L=[11,12,13,14]
    currentLine=[4]
    doOperator('L1 + A1 1',args,L,currentLine)
    assert(L[1]==args[1]+1)
    assert(currentLine==[5])
    print("Passed. ")

def testDoJump():
    print("Testing doJump()...", end="")
    args=[1,2,3,4]
    L=[11,12,13,14]
    currentLine=[2]
    lines=['! largest: Returns max(A0, A1)', 'L0 - A0 A1',\
     'JMP+ L0 a0', 'RTN A1', 'a0:', 'RTN A0']
    doJump('JMP+ L0 a0',args,L,currentLine,lines)
    assert(currentLine==[4])
    print("Passed. ")

def testDoReturn():
    print("Testing doReturn()...", end="")
    args=[1,2,3,4]
    L=[11,12,13,14]
    assert(doReturn('RTN L1',args,L,)==12)
    assert(doReturn('RTN - L1 42',args,L,)==-30)
    print("Passed. ")

def testRunSimpleProgram():
    print("Testing runSimpleProgram()...", end="")
    largest = """! largest: Returns max(A0, A1)
                   L0 - A0 A1
                   JMP+ L0 a0
                   RTN A1
                   a0:
                   RTN A0"""
    assert(runSimpleProgram(largest, [5, 6]) == 6)
    assert(runSimpleProgram(largest, [6, 5]) == 6)
    sumToN = """! SumToN: Returns 1 + ... + A0
                ! L0 is a counter, L1 is the result
                L0 0
                L1 0
                loop:
                L2 - L0 A0
                JMP0 L2 done
                L0 + L0 1
                L1 + L1 L0
                JMP loop
                done:
                RTN L1"""
    assert(runSimpleProgram(sumToN, [5]) == 1+2+3+4+5)
    assert(runSimpleProgram(sumToN, [10]) == 10*11//2)
    assert(runSimpleProgram('RTN + 42 L42', []) == 42)
    print("Passed.")

def testApproximate():
    print("Testing approximate()...", end="")
    assert(approximate((1.2,1.111111111,3.999999))==(1.2,1.1111,4.0))
    assert(approximate((0,12,3.99946))==(0,12,3.9995))
    print("Passed.")

def testLinearRegression():
    print("Testing linearRegression()...", end="")
    assert(linearRegression([(1,3), (2,5), (4,8)]) == (1.6429, 1.5, 0.9972))
    assert(linearRegression([(1,3), (2,4), (3,5)]) == (1, 2, 1))
    print("Passed.")

def testBogusDataFinder():
    print("Testing bogusDataFinder()...", end="")
    bogusData = """\
playerID,nameFirst,nameLast,teamID,games,atBats,runs,hits,doubles,triples,\
homeRuns,runsBattedIn,stolenBases,caughtStealing,Walks,StrikeOuts,battingAverage
abreujo02,Jose,Abreu,CHA,145,5560,80,176,35,2,36,107,3,1,51,131,0.317
almonzo01,Zoilo,Almonte,NYA,13,36,2,5,0,0,1,3,1,0,0,14,0.139
abreubo01,Bobby,Abreu,NYN,78,133,120,33,9,0,1,14,1,0,20,21,0.248"""
    assert(bogusDataFinder(bogusData) == [("abreubo01", "runs"),("abreujo02", \
        "atBats")])
    print("Passed.")


testLookAndSay()
testInverseLookAndSay()
testSolvesCryptarithm()
testIsSubset()
testCalculateScores()
testGetValues()
testDoOperator()
testDoReturn()
testDoJump()
testBestScrabbleScore()
testRunSimpleProgram()
testApproximate()
testLinearRegression()
testBogusDataFinder()