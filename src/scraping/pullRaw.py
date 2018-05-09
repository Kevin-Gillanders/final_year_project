import pprint as pp
with open ('./raw1.txt', 'w') as w:
    with open('./posts.csv', 'r') as r:
        x = 0
        for lines in r:
            lines = lines.strip()

            if len(lines) > 0:
                x += 1
                if x > 476000 and x < 476310:
                    w.write('count : '+ str(x)+ '\n\n\n' +lines + '\n\n\n')
                    #print('hello')
                    #pp.pprint(lines)#print(str(x) + '\n\n\n' + lines+'\n\n')
                    #print('\n\n\n')
                elif x > 477000:
                    break
