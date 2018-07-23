with open('cleanCombinedScores', 'r') as r:
    with open('cleanCombinedScoresAlphbetised.txt', 'w') as w:
        #The combined scores was unordered and as such this was very slow
        #I ordered it and this has significantly reduced the time needed
        #To join the scores
        r.readline()
        l = r.readlines()
        l.sort()
        for x in reversed(l):
            w.write(x)
