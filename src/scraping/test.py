with open('subDetails.txt', 'r') as r:
	comment = ''
	split = str(chr(3))+'::'+str(chr(4))
	for line in r:
	        comment = comment + line
	        #print(line)
	        if line.strip() == split:
	        	#print(comment)
	        	break
	        	
	comment = comment.split(str(chr(4)))
	print(comment[0])
	for x in comment:
		x = x.split(str(chr(3)))
		print(x)
