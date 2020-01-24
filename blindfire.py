import numpy as np

#even these will never change since only Rheinmetall MG 3 has blindfire
minRounds = 20
maxRounds = 30
clipRounds = 100
numberOfClips = 3

minTurns = int(np.ceil(clipRounds/maxRounds))
maxTurns = int(np.ceil(clipRounds/minRounds))

#correct for [20-30], 100 Rheinmetall MG 3
turnProbs = [0,0,0,0,0.28976071428571304,0.7102392857142543]

#these are general, as these are boundaries of Rheinmetall MG 3
qualityMin = [23.25450785] #Blindfire minimum quality
qualityMax = [26.88299505] #Blindfire maximum quality
qualityMinInfiniteSpeed = [64.5958551389 for a in range(maxTurns+1)]
qualityMaxInfiniteSpeed = [65.5682806098 for b in range(maxTurns+1)]

#calculate quality value for successive turns
for i in range(maxTurns-1): #could probably be maxTurns rather than maxTurns-1
    qualityMin.append(qualityMin[0]/36*(36-(i+1)*5)) #36 is Rheinmetall MG 3's minimum Accuracy
    qualityMax.append(qualityMax[0]/41*(41-(i+1)*5)) #41 is Rheinmetall MG 3's minimum Accuracy

blindfireMin = 0.15
blindfireMax = 0.17

procProbMin = []
procProbMax = []
turnsDealt = []
turnsUsed = []

#iterate over how many turns it takes to expend full clip
for j in range(minTurns,maxTurns+1):
    
    #iterate over when blindfire procs
    for k in range(1,j+1):
        
        procProbMin.append(turnProbs[j]*blindfireMin*(1-blindfireMin)**(k-1))
        procProbMax.append(turnProbs[j]*blindfireMax*(1-blindfireMax)**(k-1))
        turnsDealt.append(j)
        turnsUsed.append(k)
    
    #blindfire does not proc in j turns
    procProbMin.append(turnProbs[j]*(1-blindfireMin)**j)
    procProbMax.append(turnProbs[j]*(1-blindfireMax)**j)
    turnsDealt.append(j)
    turnsUsed.append(k)

summedMultiMin = 0
summedMultiMax = 0
summedMultiMinInfiniteSpeed = 0
summedMultiMaxInfiniteSpeed = 0


for l in range(len(procProbMin)):
    a = turnsUsed[l]
    x = turnsDealt[l] - a + 1
    qualityMinFirstClip = np.sum(qualityMin[0:x]) + (a - 1) * qualityMin[0]
    qualityMaxFirstClip = np.sum(qualityMax[0:x]) + (a - 1) * qualityMax[0]
    qualityMinInfiniteSpeedFirstClip = np.sum(qualityMinInfiniteSpeed[0:x]) + (a - 1) * qualityMinInfiniteSpeed[0]
    qualityMaxInfiniteSpeedFirstClip = np.sum(qualityMaxInfiniteSpeed[0:x]) + (a - 1) * qualityMaxInfiniteSpeed[0]
    
    for m in range(len(procProbMin)):
        b = turnsUsed[m]
        y = turnsDealt[m] - b + 1
        qualityMinSecondClip = np.sum(qualityMin[0:y]) + (b - 1) * qualityMin[0]
        qualityMaxSecondClip = np.sum(qualityMax[0:y]) + (b - 1) * qualityMax[0]
        qualityMinInfiniteSpeedSecondClip = np.sum(qualityMinInfiniteSpeed[0:y]) + (b - 1) * qualityMinInfiniteSpeed[0]
        qualityMaxInfiniteSpeedSecondClip = np.sum(qualityMaxInfiniteSpeed[0:y]) + (b - 1) * qualityMaxInfiniteSpeed[0]
        
        for n in range(len(procProbMin)):
            c = turnsUsed[n]
            z = turnsDealt[n] - c + 1
            qualityMinThirdClip = np.sum(qualityMin[0:z]) + (c - 1) * qualityMin[0]
            qualityMaxThirdClip = np.sum(qualityMax[0:z]) + (c - 1) * qualityMax[0]
            qualityMinInfiniteSpeedThirdClip = np.sum(qualityMinInfiniteSpeed[0:z]) + (c - 1) * qualityMinInfiniteSpeed[0]
            qualityMaxInfiniteSpeedThirdClip = np.sum(qualityMaxInfiniteSpeed[0:z]) + (c - 1) * qualityMaxInfiniteSpeed[0]
            
            d = a + b + c
            qualityMinMulti = (qualityMinFirstClip + qualityMinSecondClip + qualityMinThirdClip) / (d * qualityMin[0])
            qualityMaxMulti = (qualityMaxFirstClip + qualityMaxSecondClip + qualityMaxThirdClip) / (d * qualityMax[0])
            qualityMinMultiInfiniteSpeed = (qualityMinInfiniteSpeedFirstClip + qualityMinInfiniteSpeedSecondClip + qualityMinInfiniteSpeedThirdClip) / (d * qualityMinInfiniteSpeed[0])
            qualityMaxMultiInfiniteSpeed = (qualityMaxInfiniteSpeedFirstClip + qualityMaxInfiniteSpeedSecondClip + qualityMaxInfiniteSpeedThirdClip) / (d * qualityMaxInfiniteSpeed[0])
            
            
            if (a > 23):
                reloadMulti = 1
            else:
                if (a + b + 1 > 23):
                    if (a + b + 1 == 24):
                        reloadMulti = 23/24
                    else:
                        reloadMulti = 24/25
                else:
                    if (d + 2 > 23):
                        if (d + 2 == 24):
                            reloadMulti = 22/24
                        else:
                            reloadMulti = 23/24
                    else:
                        reloadMulti = d / (d + 2)
            
            indyProbMin = procProbMin[l] * procProbMin[m] *  procProbMin[n]
            indyProbMax = procProbMax[l] * procProbMax[m] *  procProbMax[n]
            
            summedMultiMin += indyProbMin * qualityMinMulti * reloadMulti
            summedMultiMax += indyProbMax * qualityMaxMulti * reloadMulti
            summedMultiMinInfiniteSpeed += indyProbMin * qualityMinMultiInfiniteSpeed * reloadMulti
            summedMultiMaxInfiniteSpeed += indyProbMax * qualityMaxMultiInfiniteSpeed * reloadMulti

print("Minimum multi: ", summedMultiMin, "including reloads.")
print("Maximum multi: ", summedMultiMax, "including reloads.")
print("Minimum multi (Infinite Speed): ", summedMultiMinInfiniteSpeed, "including reloads.")
print("Maximum multi (Infinite Speed): ", summedMultiMaxInfiniteSpeed, "including reloads.")
