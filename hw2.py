import math

def almostEqual(d1, d2):
    epsilon = 10**-8
    return (abs(d2 - d1) < epsilon)

def isPrime(n):
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

def nthPrime(n):
    found = 0
    guess = 0
    while (found <= n):
        guess += 1
        if (isPrime(guess)):
            found += 1
    return guess

def sumOfSquaresOfDigits(n):
    total=0
    if (n==0):return 0
    while (n!=0):
        total+=(n%10)**2
        n//=10
    return total

def isHappyNumber(n):
    if (n<=0):return False
    if (n==1):return True
    total=sumOfSquaresOfDigits(n)
    while (total!=4):
        total=sumOfSquaresOfDigits(total)
        if (total==1):return True
    return False

def nthHappyNumber(n):
    x=0
    count=-1
    while True:
        if (isHappyNumber(x)):
            count+=1
        if (count==n):return x
        x+=1

def nthHappyPrime(n):
    count=-1
    y=2
    while True:
        if(isHappyNumber(y) and isPrime(y)):
            count+=1
        if (count==n):return y
        y+=1

def isKaprekarNumber(n):
    if (n==0): return False
    if (n==1): return True
    nsquare=n**2
    digitOfRightNum=0
    while True:
        digitOfRightNum+=1
        if(nsquare%10**digitOfRightNum==0):continue
        if(nsquare//10**digitOfRightNum==0):return False
        b=nsquare%10**digitOfRightNum
        a=nsquare//10**digitOfRightNum
        if(a+b==n):return True

def nearestKaprekarNumber(n):
    delta=-1
    while True:
        delta+=1
        if(isKaprekarNumber(n-delta)==True):return (n-delta)
        elif(isKaprekarNumber(n+delta)==True):return (n+delta)

def nthCarolPrime(n):
    x=2
    counter=-1
    while True:
        if (isPrime((2**x-1)**2-2)):
            counter+=1
        if (counter==n):return ((2**x-1)**2-2)
        x+=1

def integral(f, a, b, N):
    step=(b-a)/N
    sigma=0
    for n in range(0,N+1):
        sigma+=f(a+n*step)
    return (step*(2*sigma-f(a)-f(b))/2)

def carrylessMultiply(x, y):
    total=0
    n=0
    k=0
    while (x//10**math.ceil(n/2)!=0)or(y//10**math.ceil(n/2)!=0):
        for power in range(0,n+1):
            a=x//(10**(power))%10
            b=y//(10**(n-power))%10
            k+=a*b
        total+=(k%10)*10**n
        k=0    
        n+=1
    return total

def makeBoard(moves):
    total=0
    for n in range(0,moves):
        total+=8*10**n
    return total

def digitCount(n):
    n=abs(n)
    counter=0
    while True:
        n//=10
        counter+=1
        if (n==0): return counter

def kthDigit(n, k):
    n=abs(n)
    counter=0
    while True:
        if (counter==k):return n%10
        n//=10
        counter+=1

def replaceKthDigit(n, k, d):
    return n-(kthDigit(n,k)-d)*10**k

def getLeftmostDigit(n):
    return kthDigit(n,digitCount(n)-1)

def clearLeftmostDigit(n):
    return (n-getLeftmostDigit(n)*10**(digitCount(n)-1))

def makeMove(board, position, move):
    if (move!=1 and move!=2): return ("move must be 1 or 2!")
    elif (position>digitCount(board)): return ("offboard!")
    elif (kthDigit(board,(digitCount(board)-position))!=8): return ("occupied!")
    else:
        return replaceKthDigit(board,(digitCount(board)-position),move)

def isWin(board):
    for n in range(0,digitCount(board)-2):
        if (kthDigit(board,n)==2)and(kthDigit(board,n+1)==1)and(kthDigit(board,n+2)==1):
            return True
    return False

def isFull(board):
    for n in range(0,digitCount(board)):
        if(kthDigit(board,n)==8): return False
    return True

def play112(game):
    n=digitCount(game)
    board=makeBoard(kthDigit(game,n-1))
    if (n==1): return (str(board)+": Unfinished!")
    for step in range(n-2,0,-2):
        unverifiedBoard=makeMove(board,kthDigit(game,step),kthDigit(game,step-1))
        if (type(unverifiedBoard)==str):
            if (n%4==1): return (str(board)+": Player 2: "+unverifiedBoard)
            else: return (str(board)+": Player 1: "+unverifiedBoard)
        board=unverifiedBoard
        if (isWin(board) and n%4==1): return (str(board)+": Player 2 wins!")
        if (isWin(board) and n%4==3): return (str(board)+": Player 1 wins!")
        if (isFull(board)): return (str(board)+": Tie!")
    if (not isFull(board)): return (str(board)+": Unfinished!")


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testsunOfSquaresOfDigits():
    print("Testing sunOfSquaresOfDigits()...", end="")
    assert(sumOfSquaresOfDigits(5) == 25)   # 5**2 = 25
    assert(sumOfSquaresOfDigits(12) == 5)   # 1**2 + 2**2 = 1+4 = 5
    assert(sumOfSquaresOfDigits(234) == 29) # 2**2 + 3**2 + 4**2 = 4 + 9 + 16 = 29
    assert(sumOfSquaresOfDigits(3232323) == 48)
    print("Passed. ")

def testisHappyNumber():
    print("Testing isHappyNumber()...", end="")
    assert(isHappyNumber(-7) == False)
    assert(isHappyNumber(1) == True)
    assert(isHappyNumber(2) == False)
    assert(isHappyNumber(97) == True)
    assert(isHappyNumber(98) == False)
    assert(isHappyNumber(404) == True)
    assert(isHappyNumber(405) == False)
    print("Passed. ")

def testnthHappyNumber():
    print("Testing nthHappyNumber()...", end="")
    assert(nthHappyNumber(0) == 1)
    assert(nthHappyNumber(1) == 7)
    assert(nthHappyNumber(2) == 10)
    assert(nthHappyNumber(3) == 13)
    assert(nthHappyNumber(4) == 19)
    assert(nthHappyNumber(5) == 23)
    assert(nthHappyNumber(6) == 28)
    assert(nthHappyNumber(7) == 31)
    print("Passed. ")   

def testnthHappyPrime():
    print("Testing nthHappyPrime()...", end="")
    assert(nthHappyPrime(0) == 7)
    assert(nthHappyPrime(1) == 13)
    assert(nthHappyPrime(2) == 19)
    assert(nthHappyPrime(3) == 23)
    assert(nthHappyPrime(4) == 31)
    print("Passed. ")

def testisKaprekarNumber():
    print("Testing isKaprekarNumber()...", end="")
    assert(isKaprekarNumber(0) == False)
    assert(isKaprekarNumber(1) == True)
    assert(isKaprekarNumber(2) == False)
    assert(isKaprekarNumber(3) == False)
    assert(isKaprekarNumber(703) == True)
    assert(isKaprekarNumber(2223) == True)
    print("Passed. ")

def testnearestKaprekarNumber():
    print("Testing nearestKaprekarNumber()...", end="")
    assert(nearestKaprekarNumber(49) == 45)
    assert(nearestKaprekarNumber(50) == 45)
    assert(nearestKaprekarNumber(51) == 55)
    assert(nearestKaprekarNumber(1) == 1)
    assert(nearestKaprekarNumber(2222) == 2223)
    print("Passed. ")

def testnthCarolPrime():
    print("Testing nthCarolPrime()...", end="")
    assert(nthCarolPrime(0) == 7)
    assert(nthCarolPrime(1) == 47)
    assert(nthCarolPrime(2) == 223)
    assert(nthCarolPrime(6) == 16769023)
    print("Passed. ")

def h1(x):return x
def h2(x):return 3*x**2+3
def h3(x):return 5
def testintegral():
    print("Testing integral()...", end="")
    assert(almostEqual(integral(h1,-3/2,4,20),6.875) == True)
    assert(almostEqual(integral(h2,0,8,1000000),536) == True)
    assert(almostEqual(integral(h3,100,200,123),500) == True)
    print("Passed. ")

def testcarrylessMultiply():
    print("Testing carrylessMultiply()...", end="")
    assert(carrylessMultiply(10,123) == 1230)
    assert(carrylessMultiply(123,10) == 1230)
    assert(carrylessMultiply(9,9) == 1)
    assert(carrylessMultiply(643,59) == 417)
    print("Passed. ")

def testmakeBoard():
    print("Testing makeBoard()...", end="")
    assert(makeBoard(1) == 8)
    assert(makeBoard(2) == 88)
    assert(makeBoard(3) == 888)
    print("Passed. ")

def testdigitCount():
    print("Testing digitCount()...", end="")
    assert(digitCount(0) == 1)
    assert(digitCount(5) == digitCount(-5) == 1)
    assert(digitCount(42) == digitCount(-42) == 2)
    assert(digitCount(121) == digitCount(-121) == 3)
    print("Passed. ")

def testkthDigit():
    print("Testing kthDigit()...", end="")
    assert(kthDigit(789, 0) == kthDigit(-789, 0) == 9)
    assert(kthDigit(789, 1) == kthDigit(-789, 1) == 8)
    assert(kthDigit(789, 2) == kthDigit(-789, 2) == 7)
    assert(kthDigit(789, 3) == kthDigit(-789, 3) == 0)
    assert(kthDigit(789, 4) == kthDigit(-789, 4) == 0)
    print("Passed. ")

def testreplaceKthDigit():
    print("Testing replaceKthDigit()...", end="")
    assert(replaceKthDigit(789, 0, 6) == 786)
    assert(replaceKthDigit(789, 1, 6) == 769)
    assert(replaceKthDigit(789, 2, 6) == 689)
    assert(replaceKthDigit(789, 3, 6) == 6789)
    assert(replaceKthDigit(789, 4, 6) == 60789)
    print("Passed. ")

def testgetLeftmostDigit():
    print("Testing getLeftmostDigit()...", end="")
    assert(getLeftmostDigit(7089) == 7)
    assert(getLeftmostDigit(89) == 8)
    assert(getLeftmostDigit(9) == 9)
    assert(getLeftmostDigit(0) == 0)
    print("Passed. ")

def testclearLeftmostDigit():
    print("Testing clearLeftmostDigit()...", end="")
    assert(clearLeftmostDigit(789) == 89)
    assert(clearLeftmostDigit(89) == 9)
    assert(clearLeftmostDigit(9) == 0)
    assert(clearLeftmostDigit(0) == 0)
    assert(clearLeftmostDigit(60789) == 789)
    print("Passed. ")

def testmakeMove():
    print("Testing makeMove()...", end="")
    assert(makeMove(8, 1, 1) == 1)
    assert(makeMove(888888, 1, 1) == 188888)
    assert(makeMove(888888, 2, 1) == 818888)
    assert(makeMove(888888, 5, 2) == 888828)
    assert(makeMove(888888, 6, 2) == 888882)
    assert(makeMove(888888, 6, 3) == "move must be 1 or 2!")
    assert(makeMove(888888, 7, 1) == "offboard!")
    assert(makeMove(888881, 6, 1) == "occupied!")
    print("Passed. ")

def testisWin():
    print("Testing isWin()...", end="")
    assert(isWin(888888) == False)
    assert(isWin(112888) == True)
    assert(isWin(811288) == True)
    assert(isWin(888112) == True)
    assert(isWin(211222) == True)
    assert(isWin(212212) == False)
    print("Passed. ")

def testisFull():
    print("Testing isFull()...", end="")
    assert(isFull(888888) == False)
    assert(isFull(121888) == False)
    assert(isFull(812188) == False)
    assert(isFull(888121) == False)
    assert(isFull(212122) == True)
    assert(isFull(212212) == True)
    print("Passed. ")

def testplay112():
    print("Testing play112()...", end="")
    assert(play112( 5 ) == "88888: Unfinished!")
    assert(play112( 521 ) == "81888: Unfinished!")
    assert(play112( 52112 ) == "21888: Unfinished!")
    assert(play112( 5211231 ) == "21188: Unfinished!")
    assert(play112( 521123142 ) == "21128: Player 2 wins!")
    assert(play112( 521123151 ) == "21181: Unfinished!")
    assert(play112( 52112315142 ) == "21121: Player 1 wins!")
    assert(play112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(play112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(play112( 51211 ) == "28888: Player 2: occupied!")
    assert(play112( 5122221 ) == "22888: Player 1: occupied!")
    assert(play112( 51261 ) == "28888: Player 2: offboard!")
    assert(play112( 51122324152 ) == "12212: Tie!")
    print("Passed. ")

def testall():
    testsunOfSquaresOfDigits()
    testisHappyNumber()
    testnthHappyNumber()
    testnthHappyPrime()
    testisKaprekarNumber()
    testnearestKaprekarNumber()
    testnthCarolPrime()
    testintegral()
    testcarrylessMultiply()
    testmakeBoard()
    testdigitCount()
    testkthDigit()
    testreplaceKthDigit()
    testgetLeftmostDigit()
    testclearLeftmostDigit()
    testmakeMove()
    testisWin()
    testisFull()
    testplay112()

testall()
