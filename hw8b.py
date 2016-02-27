# hw8.py
# Hanzhou Lu / hanzhoul / II

def isPrime(n, factor=2):
    if (n < 2): return False
    elif (factor*factor > n): return True
    elif (n % factor == 0): return False
    else: return isPrime(n, factor+1)

def countDigit(n):
    if n == 0: return 0    #base case
    return 1 + countDigit(n//10)

def leftTruncated(n):
    exp = countDigit(n) - 1
    nextN = n % 10**exp
    if countDigit(nextN) != exp:  #There is a 0 in this number
        return -1
    return nextN

def isLeftTruncatablePrime(n):
    if n <= 1: return False
    if not isPrime(n):
        return False
    if n//10 == 0:
        return True       #base case
    return isLeftTruncatablePrime(leftTruncated(n))

def nthLeftTruncatablePrime(n, currentCount = -1, guess = 1):
    if n == currentCount:
        return guess - 1  #base case
    if isLeftTruncatablePrime(guess):
        currentCount += 1
    return nthLeftTruncatablePrime(n, currentCount, guess + 1)

def carrylessAdd(x, y, digit = 0):
    if x == 0 and y == 0:
        return 0          #base case
    add = (x % 10 + y % 10) % 10
    return add * 10**digit + carrylessAdd(x//10, y//10, digit+1)

def longestDigitRun(n, currentNum=None, currentRun=1, bestNum=0, bestRun=1):
    if n == 0:
        return bestNum
    if currentNum == None:       #init()
        n = abs(n)
        currentNum = n % 10
        bestNum = n % 10
    elif n % 10 == currentNum:   #consecutive num
        currentRun += 1
        if currentRun > bestRun:
            bestNum = currentNum
            bestRun = currentRun
        elif currentRun == bestRun and currentNum < bestNum:
            bestNum = currentNum
    elif n % 10 != currentNum:
        currentNum = n % 10
        currentRun = 1
    return longestDigitRun(n//10, currentNum, currentRun, bestNum, bestRun)

def isPalindrome(s):
    if len(s) == 0 or len(s) == 1:
        return True
    if s[0] != s[-1]:
        return False
    return isPalindrome(s[1:-1])

def isPalindromeWithLength(s, length, bestPalindrome = None):
    if len(s) < length:
        return bestPalindrome      #base case
    if isPalindrome(s[0:length]):  #check string with same length
        if bestPalindrome == None or s[0:length] > bestPalindrome:
            bestPalindrome = s[0:length]
    return isPalindromeWithLength(s[1:], length, bestPalindrome)

def longestSubpalindrome(s, l = None):
    if l == None:
        l = len(s)
    if s == '': return ''
    bestPalindrome = isPalindromeWithLength(s, l)
    if bestPalindrome == None:
        return longestSubpalindrome(s, l-1)
    else:
        return bestPalindrome     #base case






######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testIsPrime():
    print("Testing isPrime... ", end="")
    assert(isPrime(7) == True)
    assert(isPrime(2) == True)
    assert(isPrime(3) == True)
    assert(isPrime(4) == False)
    assert(isPrime(239) == True)
    print("Passed!")

def testCountDigit():
    print("Testing countDigit... ", end="")
    assert(countDigit(7) == 1)
    assert(countDigit(17) == 2)
    assert(countDigit(117) == 3)
    print("Passed!")

def testCarrylessAdd():
    print("Testing carrylessAdd... ", end="")
    assert(carrylessAdd(1, 2) == 3)
    assert(carrylessAdd(785, 376) == 51)
    assert(carrylessAdd(99, 1) == 90)
    print("Passed!")

def testLeftTruncated():
    print("Testing leftTruncated... ", end="")
    assert(leftTruncated(4321) == 321)
    assert(leftTruncated(321) == 21)
    assert(leftTruncated(21) == 1)
    print("Passed!")

def testIsLeftTruncatablePrime():
    print("Testing isLeftTruncatablePrime... ", end="")
    assert(isLeftTruncatablePrime(7) == True)
    assert(isLeftTruncatablePrime(997) == True)
    assert(isLeftTruncatablePrime(1) == False)
    assert(isLeftTruncatablePrime(103) == False)
    assert(isLeftTruncatablePrime(743) == True)
    print("Passed!")

def testNthLeftTruncatablePrime():
    print("Testing nthLeftTruncatablePrime... ", end="")
    assert(nthLeftTruncatablePrime(0) == 2)
    assert(nthLeftTruncatablePrime(10) == 53)
    assert(nthLeftTruncatablePrime(20) == 223)
    print("Passed!")

def testLongestDigitRun():
    print("Testing longestDigitRun... ", end="")
    assert(longestDigitRun(123334444445) == 4)
    assert(longestDigitRun(112233) == 1)
    assert(longestDigitRun(11222333) == 2)
    assert(longestDigitRun(1122333) == 3)
    print("Passed!")

def testIsPalindrome():
    print("Testing isPalindrome... ", end="")
    assert(isPalindrome('abcba') == True)
    assert(isPalindrome('abba') == True)
    assert(isPalindrome('a') == True)
    assert(isPalindrome('ababba') == False)
    print("Passed!")

def testIsPalindromeWithLength():
    print("Testing isPalindromeWithLength... ", end="")
    assert(isPalindromeWithLength('abcba',5) == 'abcba')
    assert(isPalindromeWithLength('abba',4) == 'abba')
    assert(isPalindromeWithLength('a',1) == 'a')
    assert(isPalindromeWithLength('ababba',4) == 'abba')
    print("Passed!")

def testLongestSubpalindrome():
    print("Testing longestSubpalindrome... ", end="")
    assert(longestSubpalindrome('abcba') == 'abcba')
    assert(longestSubpalindrome('abba') == 'abba')
    assert(longestSubpalindrome("ab-4-be!!!") == 'b-4-b')
    assert(longestSubpalindrome("abcbce") == 'cbc')
    print("Passed!")

testIsPrime()
testCountDigit()
testLeftTruncated()
testIsLeftTruncatablePrime()
testNthLeftTruncatablePrime()
testCarrylessAdd()
testLongestDigitRun()
testIsPalindrome()
testIsPalindromeWithLength()
testLongestSubpalindrome()