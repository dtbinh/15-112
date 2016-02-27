# hw3.py
# Hanzhou Lu / hanzhoul / II
import math
import string
def patternedMessage(message, pattern):
    result=''
    newMessage=''
    counter=0
    for messageLetter in message:
        if  not messageLetter.isspace():
            newMessage+=messageLetter   #Remove the whitespace in the message
    for n in pattern:
        if n.isspace():                 #Preserve the whitespace in the pattern
            result+=n
        else:
            result+=newMessage[counter%len(newMessage)]#Add letter to result
            counter+=1                                 #with pattern's format
    if result.startswith('\n'):
        result=result[1:]
    if result.endswith('\n'):
        result=result[0:-1]
    return result

def encodeRightLeftCipher(message, rows):
    result=''
    columns=math.ceil(len(message)/rows)
    totalNum=columns*rows
    compensatoryLetter=string.ascii_lowercase[-1:-(totalNum-len(message)+1):-1]
    #Fill the blank in grid with string starting with z and going in reverse
    message+=compensatoryLetter
    for n in range(rows):
        if (n%2==0):                         #For row1,3,5...read to the right 
            for x in range(totalNum):
                if x%rows==n:
                    result+=message[x]
        if (n%2==1):                         #For row2,4,6...read to the left
            for y in range(totalNum-1,-1,-1):
                if y%rows==n:
                    result+=message[y]
    result=str(rows)+result
    return result

def decodeRightLeftCipher(encodedMessage):
    message=''
    for x in range(len(encodedMessage)):
        if not encodedMessage[x].isdigit():
            rowDigits=x
            break
    rows=int(encodedMessage[:x])             #Separate the rows and codes
    encodedMessage=encodedMessage[x:]
    columns=round(len(encodedMessage)/rows)
    for C in range(columns):                 #Search for the character
        for R in range(rows):
            if (R%2==0):
                message+=encodedMessage[R*columns+C]
            if (R%2==1):
                message+=encodedMessage[(R+1)*columns-C-1]
    result=''
    for n in message:
        if n.isupper(): result+=n
    return result

def bestStudentAndAvg(gradebook):
    lines=gradebook.splitlines()
    numOflines=len(lines)
    bestGrade=-101
    for n in lines:
        if (not n.startswith("#")) and (not n==''):
        #Ignore empty lines and comments
            sumOfGrade=0               
            listOfGrade=n+','          #Treat ',' as separator between grades
            name=n[:n.find(',')]
            numOfGrades=listOfGrade.count(',')-1
            for m in range(numOfGrades):
                listOfGrade=listOfGrade[listOfGrade.find(',')+1:]
                sumOfGrade+=int(listOfGrade[:listOfGrade.find(',')])
                avg=round(sumOfGrade/numOfGrades)
            if (avg>bestGrade):        #Compare average grades between students
                bestGrade=avg
                bestStudent=name
    return bestStudent+':'+str(bestGrade)

def deleteComments(code,start,end):
    commentStart=code.find(start)
    commentEnd=code[commentStart+1:].find(end)+commentStart+1
    if start!='#':    
        code=code[:commentStart]+code[commentEnd+1:]
    else:
        code=code[:commentStart]+code[commentEnd:]
    return code

def topLevelFunctionNames(code):
    result=''
    count=0
    while count!=len(code):
        n=code[count]
        if n=="'":                          #Ignore the comments start with '
            code=deleteComments(code,"'","'")
            count-=1
        if n=='"':                          #Ignore the comments start with "
            code=deleteComments(code,'"','"')
            count-=1
        if n=='#':                          #Ignore the comments start with #
            code=deleteComments(code,"#","\n")
        count+=1
    for x in range(code.count('\n')):       #Find the function name
        if code.splitlines()[x].startswith('def '):
            line=code.splitlines()[x]
            functionName=line[4:line.find("(")]
            if not functionName in result.split("."):result+=functionName+"."
    result=result[:-1]
    return result

def findTwoOperands(s,operator):      #Find the integers beside the operator
    count1=0
    count2=0
    for n in s[s.find(operator)-1::-1]:
        if not n.isdigit(): break
        count1+=1
    for m in s[s.find(operator)+len(operator):]:
        if not m.isdigit(): break
        count2+=1
    return s[s.find(operator)-count1:s.find(operator)+len(operator)+count2]

def nextOperator(s):                  #Find operators by precedence
    if s.find('**')!=-1:              #(** first, then *,/,//,%, then +,-)
        return findTwoOperands(s,'**')
    for x in s:
        if x=='*':
            return findTwoOperands(s,'*')
        if x=='/':
            if s[s.find('/')+1]=='/':
                return findTwoOperands(s,'//')
            else:
                return findTwoOperands(s,'/')
        if x=='%':
            return findTwoOperands(s,'%')
    for y in s:
        if y=='+':
            return findTwoOperands(s,'+')
        if y=='-':
            return findTwoOperands(s,'-')

def applySingleOperator(s):          #Do the operator finded by "nextOperator"
    if s.find('**')!=-1: 
        ans=int(s[:s.find('**')])**int(s[s.find('**')+2:])
    elif s.find('*')!=-1: 
        ans=int(s[:s.find('*')])*int(s[s.find('*')+1:])
    elif s.find('//')!=-1: 
        ans=int(s[:s.find('//')])//int(s[s.find('//')+2:])
    elif s.find('/')!=-1: 
        ans=int(s[:s.find('/')])/int(s[s.find('/')+1:])
    elif s.find('%')!=-1: 
        ans=int(s[:s.find('%')])%int(s[s.find('%')+1:])
    elif s.find('+')!=-1: 
        ans=int(s[:s.find('+')])+int(s[s.find('+')+1:])
    elif s.find('-')!=-1: 
        ans=int(s[:s.find('-')])-int(s[s.find('-')+1:])
    return str(ans)

def getEvalSteps(expr):
    if nextOperator(expr)==None:
        return expr+' = '+expr
    lenOfSpace=len(expr)
    result=expr
    while True:                  #Do the calculations until the ans is an int
        origin=nextOperator(expr)
        replace=applySingleOperator(origin)
        expr=expr.replace(origin,replace,1)
        result+=' = '+expr+'\n'+' '*lenOfSpace
        if (expr==replace): break
    return result[:len(result)-lenOfSpace-1]

def bonusDecode1(msg):
    result=''
    for n in msg:
        if n=='a':
            result+='z'
        elif n.islower():
            result+=chr(ord(n)-1)
        else:
            result+=n
    return result

def bonusDecode2(msg):
    result=''
    count=0          #Creat a list for decoding which contains letters and num
    codeScript = string.ascii_letters+string.digits
    for n in msg:
        if n.isalnum():
            result+=codeScript[(codeScript.find(n)+count)%62]
        else:
            result+=n
        count+=1
    return result

def bonusDecode3(msg):
    result=''
    code=msg.split(',')
    for n in range(1,len(code)+1):
        total=0
        for x in range(n):              #Sum up the nums before
            if code[x].startswith('\n'):
                total+=int(code[x][1:])
            else:
                total+=int(code[x])
        result+=chr(total)
    return result

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testPatternedMessage():
    print("Testing patternedMessage()...", end="")
    assert(patternedMessage("Go Pirates!!!", """
***************
******   ******
***************
""") == """GoPirates!!!GoP
irates   !!!GoP
irates!!!GoPira""")
    assert(patternedMessage("Three Diamonds!","""    *     *     *
   ***   ***   ***
  ***** ***** *****
   ***   ***   ***
    *     *     *
""")=="""    T     h     r
   eeD   iam   ond
  s!Thr eeDia monds
   !Th   ree   Dia
    m     o     n""")
    print("Passed. ")

def testEncodeRightLeftCipher():
    print("Testing encodeRightLeftCipher()...", end="")
    assert(encodeRightLeftCipher('WEATTACKATDAWN',4)=='4WTAWNTAEACDzyAKT')
    assert(encodeRightLeftCipher('ABCD',2)=='2ACDB')
    assert(encodeRightLeftCipher('WEATTACKATDAWN', 6)=='6WCWNKEAAzyTTTDxwAA')
    assert(encodeRightLeftCipher('NECEFTMWTJMCIDDAVTCOISSXJTEEPT', 2)==\
        '2NCFMTMIDVCISJEPTETXSOTADCJWTEE')
    print("Passed. ")

def testDecodeRightLeftCipher():
    print("Testing encodeRightLeftCipher()...", end="")
    assert(decodeRightLeftCipher('4WTAWNTAEACDzyAKT')=='WEATTACKATDAWN')
    assert(decodeRightLeftCipher('2ACDB')=='ABCD')
    assert(decodeRightLeftCipher('10MKLOKSFUGJMXTNSUJFXBPROQJAKWBY')==\
        'MSFXTFXQJYKKUMNJBOABLOGJSUPRKW')
    print("Passed. ")

def testBestStudentAndAvg():
    gradebook = """
# ignore  blank lines and lines starting  with  #'s
wilma,91,93
fred,80,85,90,95,100
betty,88
"""
    print("Testing bestStudentAndAvg()...", end="")
    assert(bestStudentAndAvg(gradebook) ==  "wilma:92")
    assert(bestStudentAndAvg('fred,0') == 'fred:0')
    print("Passed. ")

def testTopLevelFunctionNames():
    print("Testing topLevelFunctionNames()...", end="")
    # f is redefined
    code = """\
def f(x): return x+42
def g(x): return x+f(x)
def f(x): return x-42
"""
    assert(topLevelFunctionNames(code) == "f.g")
    # g() is in triple-quotes (""")
    code = '''\
def f(): return """
def g(): pass"""
'''
    assert(topLevelFunctionNames(code) == "f")
    assert(topLevelFunctionNames\
        ('def f(): return 42 # """\ndef g(): pass # """\n') == "f.g")
    print("Passed. ")

def testGetEvalSteps():
    print("Testing getEvalSteps()...", end="")
    assert(getEvalSteps('123') == '123 = 123')
    assert(getEvalSteps("2+3*4-8**3%3") == '''2+3*4-8**3%3 = 2+3*4-512%3
             = 2+12-512%3
             = 2+12-2
             = 14-2
             = 12''')
    print("Passed. ")

def bonusEncode1(msg):
    result = ""
    for c in msg:
        if (c.islower()):
            c = chr(ord('a') + (ord(c) - ord('a') + 1)%26)
        result += c
    return result

def testBonusDecode1():
    print("Testing bonusDecode1()...", end="")
    s='abcdefghijklmnopqrstuvwxyz'
    assert(bonusDecode1(bonusEncode1(s)) == s)
    print("Passed. ")

def bonusEncode2(msg):
    result = ""
    p = string.ascii_letters + string.digits
    for i in range(len(msg)):
        c = msg[i]
        if (c in p): c = p[(p.find(c) - i) % len(p)]
        result += c
    return result

def testBonusDecode2():
    print("Testing bonusDecode2()...", end="")
    s=string.ascii_letters + string.digits
    assert(bonusDecode2(bonusEncode2(s)) == s)
    print("Passed. ")

def bonusEncode3(msg):
    result = ""
    prev = 0
    for i in range(len(msg)):
        curr = ord(msg[i])
        if (result != ""): result += ","
        if ((i+1) % 15 == 0): result += "\n"
        result += str(curr - prev)
        prev = curr
    return result

def testBonusDecode3():
    print("Testing bonusDecode3()...", end="")
    s=string.ascii_letters+string.digits+string.punctuation+string.printable
    assert(bonusDecode3(bonusEncode3(s)) == s)
    print("Passed. ")

testPatternedMessage()
testEncodeRightLeftCipher()
testDecodeRightLeftCipher()
testBestStudentAndAvg()
testTopLevelFunctionNames()
testGetEvalSteps()
testBonusDecode1()
testBonusDecode2()
testBonusDecode3()