import time

# This adds the new score to the csv of previous data

with open("../../data/scores/cleanCombinedScoresAlphbetised.txt", "r") as r:
    with open("../../data/submissions/Cleaned.csv", "r") as r1:
        with open("../../data/submissions/newPosts.csv", "w") as w:
            with open("../../data/scores/notYetFoundScores.txt", "w") as w1:
                w.write(r1.readline().replace('\n', '') + '\tnew_score\n')
                #List of lists will contain id and new scores
                scores = []
                for score in r:
                    scores.append(score.split(","))
                found = False
                present = 0
                notPresent = 0
                count = 0
                t1 = time.time()
                # This will take a couple hours as
                # the scores are out of order
	    	    # If the score is found add it to the csv
 	        	# Then remove it from the list
                try:
                    for attr in r1:
                        attr = attr.replace('\n', '').split("\t")
                        count += 1
                        for score in scores:
                            # Scores position
                            if attr[27] == score[0]:
                                attr.append(score[1].replace('\n', ''))
                                w.write("\t".join(attr)+'\n')
                                scores.remove(score)
                                found = True
                                break
                        if found:
                            present += 1
                            found = False
                            continue
                        else:
                            notPresent += 1
                            found = False
                            continue
                except KeyboardInterrupt:
                    for score in scores:
                        #Scores position
                        w1.write(','.join(score))
                    print("got to {}".format(count))
print("it took : {} to input {}, {} could not be found".format(time.time()-t1, present, notPresent))