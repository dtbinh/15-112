# hw6.py
# Hanzhou Lu / hanzhoul / II
import math
import string
import time
import copy
import bisect

"""
[s15-quiz1]
[1.a]
Program will crash.

[1.b]
d1 = 100, d2 = 0 It should calculate absolute value.

[2]
A 12
B 49
C 1
D 1.6
E 1.0
F 3
G 1
H 2
I True
J False
M 2
N <class 'int'>
O None

[3]
64

[4]
def roundToInt(f):
    positiveOrNegative = f/abs(f)
    f = abs(f)
    return int(positiveOrNegative*((f-f%1)+f%1//0.5))

[s15-quiz2]
[1]
(4, 4)
(2, 6)
(25, 7)
(28, 44)
(8, 5)
(15, 6)
(16, 7)

[2]
7

[3.a]
301

[3.c]
Because values on both sides of 0 are >0 which 
findZeroWithBisection() cannot find.

[4]
def convertNumber(a):
    a = abs(a)
    result = 0
    temp = a
    for i in range(10):
        a = temp
        while a != 0:
            if a%10 == i:
                result = result*10+i
                break
            a//=10
    return result

def sameDigits(m,n):
    return convertNumber(m) == convertNumber(n)
"""

"""
[2.1]
It count the length of a.
The worst-case big-oh of this function is O(n).
(The for-loop has n steps, each step take the same time.)

def betterSlow1(a):
    return len(a)

The worst-case big-oh of this function is O(1).
(The big-oh of function len(list) is O(1).) 

[2.2]
Check if there isn't repeated number in the list.
The worst-case big-oh of this function is O(n^2).
(It has n steps in the first for-loop and n-i steps in the second for-loop.)

def betterSlow2(a):
    seta = set(a)
    return len(seta) == len(a)

The worst-case big-oh of this function is O(1).
The big-oh of function len(list) is O(1).

[2.3]
Count how many numbers in b don't occur in a.
The worst-case big-oh of this function is O(n^2).
(It has n steps in the for-loop and big-oh of a step is O(n).)

def betterSlow3(a,b):
    seta = set(a)
    result = 0
    for c in b:
        if c not in seta:
            result += 1
    return result 

The worst-case big-oh of this function is O(n).
(It has n steps in the for-loop and each step take the same time.)

[2.4]
Calculate the biggest delta between numbers in a snd b.
The worst-case big-oh of this function is O(n^2).
(It has n steps in the first for-loop and the second for-loop.)

def betterSlow4(a,b):
    a = set(a)
    b = set(b)
    (maxa,mina) = (max(a),min(a))
    (maxb,minb) = (max(b),min(b))
    return max(abs(maxa-minb), abs(maxb-mina))

The worst-case big-oh of this function is O(n).
(The big-oh of function max() is O(n).)

[2.5]
Calculate the smallest delta between numbers in a and b.
The worst-case big-oh of this function is O(n^2).
(It has n steps in the first for-loop and the second for-loop.)

def betterSlow5(a,b):
    bestDelta = abs(a[0] - b[0])
    a = sorted(a)
    for i in b:
        index = bisect.bisect_left(a,i)
        if index == 0: 
            delta = a[0] - i
        elif index == len(a):
            delta = i - a[-1]
        else:
            delta1 = i - a[index-1]
            delta2 = a[index] - i
            delta = min(delta1,delta2)
        bestDelta = min(bestDelta,delta)
    return bestDelta

The worst-case big-oh of this function is O(nlogn).
(The big-oh of function bisect.bisect() is O(logn).)
"""

def invertDictionary(d):
    newd = dict()
    for key in d:
        value = d[key]
        if value not in newd:           #this value doesn't appear before
            newd[value] = set([key])
        else:                           #this value appeared before
            newd[value].add(key)        #add this value
    return newd

def sparseMatrixAdd(sm1, sm2):
    size = dict()                       #save the max-size of matrix to size
    size['rows'] = max(sm1['rows'], sm2['rows'])
    size['cols'] = max(sm1['cols'], sm2['cols'])
    result = sm2.copy()         #add elements in sm2 to result
    result.update(size)
    for key in sm1:             #add elements in sm1 to result
        if key not in result:
            result[key] = sm1[key]
        elif (type(key) != str):
            result[key] += sm1[key]
    return result

def friendsOfFriends(d):
    fof = dict()
    for key in d:
        fof[key] = set()
        for name in d[key]:
            if name in d:         #add friends of friends(not include friends)
                fof[key].update(d[name] - d[key])
        fof[key] -= set([key])          #del himself from the fof
    return fof




######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
def testInvertDictionary():
    print("Testing invertDictionary()...", end="")
    assert(invertDictionary({1:2, 2:3, 3:4, 5:3}) == 
       {2:set([1]), 3:set([2,5]), 4:set([3])})
    assert(invertDictionary(dict()) == dict())
    assert(invertDictionary({1:2, 2:3, 3:4}) == 
       {2:set([1]), 3:set([2]), 4:set([3])})
    print("Passed. ")


def testSparseMatrixAdd():
    print("Testing sparseMatrixAdd()...", end="")
    assert(sparseMatrixAdd({"rows":5, "cols":4, (1,1):2, (1,2):3},
                       {"rows":3, "cols":6, (1,1):5, (2,2):6}) ==
                       {"rows":5, "cols":6, (1,1):7, (1,2):3, (2,2):6})
    assert(sparseMatrixAdd({"rows":5, "cols":4},
                       {"rows":3, "cols":6}) ==
                       {"rows":5, "cols":6})
    assert(sparseMatrixAdd({"rows":5, "cols":4, (1,1):2},
                       {"rows":3, "cols":6, (1,1):5, (2,2):6}) ==
                       {"rows":5, "cols":6, (1,1):7, (2,2):6})
    print("Passed. ")

def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    d = dict()
    d["fred"] = set(["wilma", "betty", "barney", "bam-bam"])
    d["wilma"] = set(["fred", "betty", "dino"])

    assert(friendsOfFriends(d) == \
    {'fred': {'dino'}, 'wilma': {'bam-bam', 'barney'}})

    assert(friendsOfFriends({}) == {})

    d.update({"bam-bam":{'fred'}})
    assert(friendsOfFriends(d) == {'bam-bam': {'wilma', 'barney', 'betty'},
     'wilma': {'bam-bam', 'barney'}, 'fred': {'dino'}})
    print("Passed. ")

testInvertDictionary()
testSparseMatrixAdd()
testFriendsOfFriends()