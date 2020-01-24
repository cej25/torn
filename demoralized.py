import numpy as np
import itertools as it
import time

start_time = time.time()

minRounds = 4
maxRounds = 6
clipRounds = 45
numberOfClips = 3

#correct for [4-6], 45 GAK
turnProbs = [0,0,0,0,0,0,0,0,0.009246826171875,0.534393310546875,0.44753265380859375,0.008826732635498047,4.76837158203125e-07]

minTurns = int(np.ceil(clipRounds/maxRounds))
maxTurns = int(np.ceil(clipRounds/minRounds))

demoMin = 0.19
demoMax = 0.23

def findMulti(combo,minOrMax):
    
    totalMulti = 1
    multi = 1
    
    for i in range(len(combo)-1):

        if (i == 0):
            if (combo[i] == 0):
                multi = 1
            elif (combo[i] == 1):
                if (minOrMax == 0):
                    multi = 1.177
                else:
                    multi = 1.169
    
        elif (combo[i] != combo[i-1]):
            if (combo[i] == 1):
                if (minOrMax == 0):
                    multi = 1.177
                else:
                    multi = 1.169
            elif (combo[i] == 2):
                if (minOrMax == 0):
                    multi = 1.408
                else:
                    multi = 1.389
            elif (combo[i] == 3):
                if (minOrMax == 0):
                    multi = 1.718
                else:
                    multi = 1.684
            elif (combo[i] == 4):
                if (minOrMax == 0):
                    multi = 2.154
                else:
                    multi = 2.098
            elif (combo[i] == 5):
                if (minOrMax == 0):
                    multi = 2.806
                else:
                    multi = 2.715
        
        totalMulti += multi
        
    averageMulti = totalMulti/len(combo)
    return averageMulti
        
    
def findProb(combos,demoMin,demoMax):
    
    z = len(combos)
    combo = [combos[a] for a in range(z)]
    
    demosUsed = max(combo)
    if (demosUsed == 5):
        x = combo.index(5)
        minProb = demoMin ** 5 * (1 - demoMin) ** (x - 4)
        maxProb = demoMax ** 5 * (1 - demoMax) ** (x - 4)
    else:
        minProb = demoMin ** demosUsed * (1 - demoMin) ** (z - demosUsed)
        maxProb = demoMax ** demosUsed * (1 - demoMax) ** (z - demosUsed)
    
    return minProb, maxProb
    

def findCombos(turns,demos,combos,clip):
    
    if (clip > 1):
        
        comboBefore = [combos[a] for a in range(len(combos))]
        demosBefore = demos
        if (demosBefore < 5):
            demosAllowed = int(5 - demosBefore)
        else:
            demosAllowed = 0
        
        combos = []
        demos = []
        
        if (demosAllowed > turns):
            demosAllowed = turns
        
        for i in range(demosAllowed+1):
            
            lst = [list(b) for b in it.product([0,1], repeat=turns)]
            
            newlst = []
            for k in range(len(lst)):
                if (np.sum(lst[k]) == i):
                    newlst.append(lst[k])
            
            for l in range(len(newlst)):
                
                sequence = comboBefore
                demosUsedBefore = max(sequence)
                
                #calculates new sequence based on clip 1 + range of possiblities for clip 2
                for m in range(turns):
                    z = len(sequence)       
                    sequence = np.append(sequence,sequence[z-1]+newlst[l][m])
                                
                #appends sequence to array of sequences
                combos.append(sequence)
                      
                #calculate number of demos used and not used this clip
                demosUsed = max(sequence) - demosUsedBefore
                
                demos.append(max(sequence))
   

            
    elif (clip == 1):
        
        demosAllowed = 5
        
        if (demosAllowed > turns):
            demosAllowed = turns
                    
        for i in range(demosAllowed+1):
            
            lst = [list(j) for j in it.product([0,1], repeat=turns)]
            
            newlst = []
            for k in range(len(lst)):
                if (np.sum(lst[k]) == i):
                    newlst.append(lst[k])
            
            for l in range(len(newlst)):
                
                sequence = np.zeros(turns)
                demosUsedBefore = sequence[-1]
                
                for m in range(turns):
                    sequence[m] = sequence[m-1]+newlst[l][m]
                combos.append(sequence)
                
                demosUsed = max(sequence) - demosUsedBefore
                
                demos.append(demosUsed)
                            
    return combos,demos


combosFirstClip = []
combosSecondClip = []
combosThirdClip = []

demosFirstClip = []
demosSecondClip = []
demosThirdClip = []

#minTurns = 1
#maxTurns = 1

prevLenFirstClip = 0
prevLenSecondClip = 0
prevLenThirdClip = 0

runningMultiMin = 0
runningMultiMax = 0

for i in range(minTurns,maxTurns+1):
    resultFirstClip = findCombos(i,demosFirstClip,combosFirstClip,clip=1)
    combosFirstClip.append(resultFirstClip[0])
    demosFirstClip.append(resultFirstClip[1])
    del combosFirstClip[-1]
    del demosFirstClip[-1]

    for j in range(prevLenFirstClip,len(combosFirstClip)):
        
        for k in range(minTurns, maxTurns+1):            
            resultSecondClip = findCombos(k,demosFirstClip[j],combosFirstClip[j],clip=2)
            combosSecondClip.append(resultSecondClip[0])
            demosSecondClip.append(resultSecondClip[1])
            
            for l in range(prevLenSecondClip,len(combosSecondClip)):
                for m in range(len(combosSecondClip[l])):

                    thirdClipTurns = 23 - len(combosSecondClip[l][m])
                    for n in range(thirdClipTurns, thirdClipTurns+1):
                        resultsThirdClip = findCombos(n, demosSecondClip[l][m],combosSecondClip[l][m],clip=3)
                        combosThirdClip.append(resultsThirdClip[0])
                        demosThirdClip.append(resultsThirdClip[1])
                        
                        turnProb3 = 1 #fixed, always, for [[4-6], 45] GAK
                        
                        for o in range(prevLenThirdClip,len(combosThirdClip)): 
                            for p in range(len(combosThirdClip[o])):
                                
                                if (i > 23):
                                    reloadMulti = 1
                                else:
                                    if (i + k + 1 > 23):
                                        if (i + k + 1 == 24):
                                            reloadMulti = 23/24
                                        else:
                                            reloadMulti = 24/25
                                    else:
                                        if (i + k + n + 2 > 23):
                                            if (i + k + n + 2 == 24):
                                                reloadMulti = 22/24
                                            else:
                                                reloadMulti = 23/24
                                        else:
                                            reloadMulti = (i + k + n) / (i + k + n + 2)
                                
                                
                                minProb, maxProb = findProb(combosThirdClip[o][p],demoMin,demoMax)
                                
                                indyMultiMin = findMulti(combosThirdClip[o][p],minOrMax=0)
                                runningMultiMin += indyMultiMin * minProb * turnProbs[i] * turnProbs[k] * reloadMulti
                                
                                indyMultiMax = findMulti(combosThirdClip[o][p],minOrMax=1) #max
                                runningMultiMax += indyMultiMax * maxProb * turnProbs[i] * turnProbs[k] * reloadMulti
                                
                        prevLenThirdClip = len(combosThirdClip)
            
            prevLenSecondClip = len(combosSecondClip)
    
    print("end of another first clip...", time.time()-start_time,"seconds")
    prevLenFirstClip = len(combosFirstClip)
    
    
print("Minimum multi:",runningMultiMin)
print("Maximum multi:",runningMultiMax)
print(time.time() - start_time)
