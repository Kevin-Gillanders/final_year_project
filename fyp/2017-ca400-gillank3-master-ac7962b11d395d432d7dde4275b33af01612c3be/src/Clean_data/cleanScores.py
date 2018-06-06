with open('CombinedScores.txt', 'r') as r:
    with open('cleanCombinedScores','w') as w:
        dictScores = {}
        count = 0
        tot = 0
        for ids in r:
            ids = ids.strip().split(',')
            if ids[0] in dictScores:
                #If duplicates were present in new scores file
                #The average of the two scores is taken 
                sc = dictScores[ids[0]]
                dictScores[ids[0]] = int((int(ids[1]) + int(sc))/2)
                count += 1
            else:
                dictScores[ids[0]] = ids[1]
            tot += 1
        for k,v in dictScores.items():
            w.write(str(k)+','+str(v) + '\n')
print('count : ', count, 'total : ', tot, ' New total : ', tot - count)
