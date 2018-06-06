#Pulls small amounts of data so I can see how it is stored
with open('./posts.csv', 'r') as r:
    x = 0
    for lines in r:
        lines =lines.strip()
        if len(lines) > 0:
            if x < 5:
                print(str(x) + '\n\n\n' + lines+'\n\n')
                x += 1
            else:
                break
