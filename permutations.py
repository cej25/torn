import numpy as np

minRounds = 4
maxRounds = 6
clipRounds = 45
numberOfClips = 3

#minRounds,maxRounds,clipRounds,totalRoundsFired, turn
startParams = [minRounds,maxRounds,clipRounds,0,0]
seq = []
probSeq = []
runProb = [[] for j in range(25)]

file = open("permtest.dat","w")
def takeTurns(currentParams,sequence,probabilitySequence,runningProbability):
    turnParams = []
    currentParams[4] += 1
    turnParams[:] = currentParams[:]
    
    for i in range(currentParams[0],currentParams[1]+1):
        
        currentParams[:] = turnParams[:]
        lastTurn = False
                
        roundsFired = i
        sequence.append(roundsFired)
        currentParams[3] += roundsFired
        roundsLeft = currentParams[2] - currentParams[3]
        
        if (currentParams[1] - currentParams[0] != 0):
            if (i == currentParams[0] or i == currentParams[1]):
                indyProb = 1/(2*(currentParams[1] - currentParams[0]))
            else:
                indyProb = 1/(currentParams[1] - currentParams[0])
        else:
            indyProb = 1
        probabilitySequence.append(indyProb)
        
        if (roundsLeft > currentParams[1]):
            takeTurns(currentParams,sequence,probabilitySequence,runningProbability)
        elif (roundsLeft <= currentParams[1] and roundsLeft >= currentParams[0]):
            currentParams[1] = roundsLeft #update maxRounds
            takeTurns(currentParams,sequence,probabilitySequence,runningProbability)
        elif (roundsLeft == 0):
            lastTurn = True
        else:
            currentParams[0] = roundsLeft
            currentParams[1] = roundsLeft
            takeTurns(currentParams,sequence,probabilitySequence,runningProbability)
            
        if (lastTurn==True): 
            runningProbability[currentParams[4]].append(np.prod(probabilitySequence))
            sequenceData = str(sequence)
            probabilityData = str(np.prod(probabilitySequence))
            file.write(sequenceData)
            file.write(" - ")
            file.write(probabilityData)
            file.write("\n")
        
        del sequence[-1]
        del probabilitySequence[-1]

    return runningProbability

x = takeTurns(startParams,seq,probSeq,runProb)

minTurns = int(np.ceil(clipRounds/maxRounds))
maxTurns = int(np.ceil(clipRounds/minRounds))

for k in range(minTurns,maxTurns+1):
    print(k, "turn probability: ",sum(x[k]))
    
#now deal with reloading!
summedMulti = 0

for l in range(minTurns,maxTurns+1):
    
    for m in range(minTurns,maxTurns+1):
        
        for n in range(minTurns,maxTurns+1):
            
            if (l > 23):
                reloadMulti = 1
            else:
                if (l + m + 1 > 23):
                    if (l + m + 1 == 24):
                        reloadMulti = 23/24
                    else:
                        reloadMulti = 24/25
                else:
                    if (l + m + n + 2 > 23):
                        if (l + m + n + 2 == 24):
                            reloadMulti = 22/24
                        else:
                            reloadMulti = 23/24
                    else:
                        reloadMulti = (l + m + n) / (l + m + n + 2)
                        
            
            indyProb = sum(x[l]) * sum(x[m]) * sum(x[n])
            summedMulti += indyProb * reloadMulti
            
print("Multiply quality by:", summedMulti, "to compensate for reloads.")
