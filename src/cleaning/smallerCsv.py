with open('./data/Cleaned.csv', 'r') as r:
    with open('smallSamp.csv', 'w') as w:
        count = 0
        for line in r:
            if count < 20:
                w.write(line)
            else:
                break
            count += 1
