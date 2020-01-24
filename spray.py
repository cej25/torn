import numpy as np

minRounds = 4
maxRounds = 30
clipRounds = 60
numberOfClips = 3

minTurns = int(np.ceil(clipRounds/maxRounds))
maxTurns = int(np.ceil(clipRounds/minRounds))

#true for [4-30], 60 Dual Bushmasters
turnProbs = [0,0, 0.00036982248520710064, 0.04481777817754053, 0.27674679759354515, 0.38552707758954347, 0.21902780654302212, 0.06243370329510573, 0.010064103268452055, 0.0009594883935734232, 5.195705628142308e-05, 1.4478983822286237e-06, 1.762802071657744e-08, 7.124559596905629e-11, 5.91520564013313e-14, 3.7417803301574566e-18]

sprayMin = 0.22
sprayMax = 0.24

procProbMin = []
procProbMax = []
turnsDealt = []
turnsUsed = []

for i in range(minTurns,maxTurns+1):
    
    for j in range(1,i+1):
        
        if (j == 1):
            procProbMin.append(turnProbs[i]*sprayMin)
            procProbMax.append(turnProbs[i]*sprayMax)
            turnsDealt.append(2)
            turnsUsed.append(j)
        
    procProbMin.append(turnProbs[i]*(1-sprayMin))
    procProbMax.append(turnProbs[i]*(1-sprayMax))
    turnsDealt.append(i)
    turnsUsed.append(i)

summedMultiMin = 0
summedMultiMax = 0

for k in range(len(procProbMin)):
    a = turnsUsed[k]
    qualityMultiFirstClip = turnsDealt[k]
    
    for l in range(len(procProbMin)):
        b = turnsUsed[l]
        qualityMultiSecondClip = turnsDealt[l]
        
        for m in range(len(procProbMin)):
            c = turnsUsed[m]
            qualityMultiThirdClip = turnsDealt[m]
            
            if (a > 23):
                reloadMulti = 1
            else:
                if (a + b + 1 > 23):
                    if (a + b + 1 == 24):
                        reloadMulti = 23/24
                    else:
                        reloadMulti = 24/25
                else:
                    if (a + b + c + 2 > 23):
                        if (a + b + c + 2 == 24):
                            reloadMulti = 22/24
                        else:
                            reloadMulti = 23/24
                    else:
                        reloadMulti = (a + b + c) / (a + b + c + 2)
            
            qualityMultiTotal = (qualityMultiFirstClip + qualityMultiSecondClip + qualityMultiThirdClip) / (a + b + c)
    
            indyProbMin = procProbMin[k] * procProbMin[l] *  procProbMin[m]
            indyProbMax = procProbMax[k] * procProbMax[l] *  procProbMax[m]
            
            summedMultiMin += indyProbMin * qualityMultiTotal * reloadMulti
            summedMultiMax += indyProbMax * qualityMultiTotal * reloadMulti

print("Multiply quality by:", summedMultiMin, "to account for minimum spray and reloads.")
print("Multiply quality by:", summedMultiMax, "to account for maximum spray and reloads.")
