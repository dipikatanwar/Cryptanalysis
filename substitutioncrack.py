import sys
import random
from math import log10

nargs = len(sys.argv)
if nargs != 2:sys.exit()
filename = sys.argv[1]
cipherText = open(filename,'r').read()
inputChar = '1234567890@#$zyxwvutsrqpon'
outputChar = 'abcdefghijklmnopqrstuvwxyz'
inputCharArr = [c for c in inputChar ] 
outputCharArr = [c for c in outputChar] 

pop_size = 500
select_pop = 150
select_random = 50
child_count = 300
generation = 200
alphabete_set = 26
crossover_rate = 30
mutation_rate = 3
total = 0

def readQuad():
    global total
    outDict = {}
    fp = open('english_quadgrams.txt', 'r')
    for line in fp:
        word, count = line.lower().split()
        total += int(count)
        outDict[word] = int(count)
    for k in outDict.keys():
        outDict[k] = log10(float(outDict[k])/total)        
    return outDict

probability = readQuad()

def decrypt(mapping):
    global cipherText
    outText = ''
    for c in cipherText:
        if c in [' ', ',', '.']:
            outText += c
        else:
            outText += mapping[c]
    return outText


def score(text):
    global probability,total
    s = 0
    for i in range(len(text)-3):
        word = text[i:i+4]
        if ' ' in word: continue
        s += probability.get(word,log10(0.001/total))
    return s

def getFitness(mapping):
    global cipherText, inputCharArr, outputCharArr
    outText = ''
    for c in cipherText:
        if c in [' ', ',', '.']:
            outText += ' '
        else:
            outText += mapping[c]
    return score(outText)

def replace(child,index,value):
    outchild = child.copy()
    save = outchild[index]
    outchild[index] = value
    for k,v in child.items():
        if v == value:
            outchild[k] = save
    #print(outchild)
    return outchild

def crossOver(mapArr):
    global inputChar,child_count
    newMapArr = mapArr.copy()
    for c in range(child_count):
        x = random.sample(mapArr,2)
        child = x[0].copy()
        for i in range(crossover_rate):
             index = random.choice(inputChar)
             child = replace(child, index, x[1][index])
        newMapArr.append(child)
    return newMapArr

def mutation(mapArr):
    global child_count,pop_size,inputChar,mutation_rate
    newMapArr = mapArr[:child_count].copy()
    child = mapArr[child_count:].copy()
    for c in child:
        for i in range(mutation_rate):
            index = random.sample(inputChar,2)
            v = c[index[0]]
            c[index[0]] = c[index[1]]
            c[index[1]] = v
        newMapArr.append(c)
    return newMapArr

def select(mapArr):
    global select_pop, select_random
    mapArr.sort(key=getFitness,reverse=True)
    newMapArr = mapArr[:select_pop].copy()
    samples = random.sample(mapArr[select_pop:],select_random)
    for s in samples:newMapArr.append(s)
    return newMapArr

def getRandomMap():
    global outputCharArr,inputChar
    x = outputCharArr.copy()
    random.shuffle(x)
    ret = {}
    for i in range(alphabete_set):
        ret[inputChar[i]] = x[i]
    return ret

def init():
    global pop_size
    mapArr = []
    for i in range(pop_size):
        mapArr.append(getRandomMap())
    return mapArr


def main():
    readQuad()
    mapArr = init()
    print("The algoritm will run for ", generation , "generations")
    for gen in range(generation):
        if gen%10 == 0:
            print("Running Generation ", gen)
        mapArr = select(mapArr)
        mapArr = crossOver(mapArr)
        mapArr = mutation(mapArr)    
    print(mapArr[0])
    print(decrypt(mapArr[0]))

main()
