import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
with open("../../data/submissions/newPosts.csv", "r") as r:
    r.readline()
    diff = []
    for line in r:
        line = line.replace('\n', '').split('\t')
        x = int(line[5])
        y = int(line[56])
        x = int(line[66])
        ans = abs(x-y)
        #if y < 5000:
        diff.append([x,y,abs(x-y)])
        '''if int(line[5]) > int(line[66]) :# != 67:
            print("old score  : " + str(line[5]) + "     New score  : " + str(line[66]))
            print(line[17])'''

diff = sorted(diff, key=lambda x: x[0])
a = []
b = []
for x in diff:
    a.append(x[0])
    b.append(x[1])
t = np.array(a)
t1 = np.array(b)
#do linregress
slope, intercept, r_value, p_value, std_err = stats.linregress(t, t1)
#fit = np.polyfit(t, t1, deg=1)
#plt.plot(t,fit[0] * t + fit[1], color='red')
plt.plot(t, intercept + slope*t, 'r', label='fitted line')
plt.scatter(t,t1)
print("r_value is : {}   p_value is : {} \n".format(r_value, p_value))
#plt.hist(t1, bins=25)#, range=(1000.0, 40000.0))
plt.ylabel('old score')
plt.xlabel('num comments')
plt.show()
