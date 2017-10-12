def compressH(fileName):
    data = open(fileName,"r")
    dataWrite = open("CompressedData.txt","a")
    while True:
        line = str.strip(data.readline())
        if line == "":
            break
        dataPointRepeatAmt = 0
        x = None
        xT = None
        dataPointRepeat = []
        patternRepeat = None
        for d in line:
            if d == x:
                if dataPointRepeatAmt < 1:
                    dataPointRepeatAmt +=1
                else:
                    dataPointRepeatAmt += 1
            else:
                if dataPointRepeatAmt >= 2:
                    dataPointRepeat.append("R"+str(dataPointRepeatAmt))
                    dataPointRepeat.append(d)
                    dataPointRepeatAmt = 0
                else:
                    dataPointRepeat.append(d)
                    dataPointRepeatAmt = 0
            x = d
##        patternRepeat = dataPointRepeat
##        listEat = 0
##        for p in patternRepeat:
##            if p.find("R") != -1:
##                pIndex = patternRepeat.index(p)
##                patternRepeat.insert(int(pIndex),".")
##                patternRepeat.remove(patternRepeat[pIndex+1])
##                patternRepeat.insert(int(pIndex)-1,".")
##                patternRepeat.remove(patternRepeat[pIndex])
##        print(patternRepeat)
            
        for i in dataPointRepeat:
            dataWrite.write(i)
    dataWrite.close()
    data.close()

def compressV(fileName):
    data = open(fileName,"r")
    dataWrite = open("CompressedData.txt","a")
    xLine = []
    xyLine = []
    while True:
        xLineD = str.strip(data.readline())
        if xLineD == "":
            break
        xLine.append(xLineD)
        xyLine.append(xLine)
    print (xyLine)
    for i in range(0,len(xyLine)+1):
        for c in range(0,len(xyLine[i])+1):
            for b in xyLine[c][i]:
                print (b,end="")

        
##    while True:
##        line = data.readline()
##        if line == "":
##            break
##        dataPointRepeatAmt = 0
##        x = None
##        dataPointRepeat = []
##        for d in line:
##            if d == x:
##                if dataPointRepeatAmt < 1:
##                    dataPointRepeatAmt +=1
##                else:
##                    dataPointRepeatAmt += 1
##            else:
##                if dataPointRepeatAmt >= 2:
##                    dataPointRepeat.append("R"+str(dataPointRepeatAmt))
##                    dataPointRepeat.append(d)
##                    dataPointRepeatAmt = 0
##                else:
##                    dataPointRepeat.append(d)
##                    dataPointRepeatAmt = 0
##            x = d
##        for i in dataPointRepeat:
##            dataWrite.write(i)
    dataWrite.close()
    data.close()
    
#compressV("Data.txt")
compressH("Data.txt")
