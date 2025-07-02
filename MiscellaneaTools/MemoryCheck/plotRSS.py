import matplotlib.pyplot as plt
import seaborn as sns

with open("RSS_s2.out") as f:
    data = f.read()
data = data.split('\n')

y = [row.split(' ')[0] for row in data]
x = range(1, len(y))
y.pop()
y = [float(i) / (1024*1024) for i in y]


with open("RSS_sqs2.out") as f2:
    data2 = f2.read()

data2 = data2.split('\n')

y2 = [row.split(' ')[0] for row in data2]
x2 = range(1, len(y2))
y2.pop()
y2 = [float(i) / (1024*1024) for i in y2]


with open("RSS_step3.out") as f3:
    data3 = f3.read()

data3 = data3.split('\n')

y3 = [row.split(' ')[0] for row in data3]
x3 = range(len(y), len(y) + len(y3)-1)

y3.pop()
y3 = [float(i) / (1024*1024) for i in y3]


sns.set_style("darkgrid") # Apply the darkgrid style

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_title("RSS memory PromptCalibProdSiStrip", weight='bold')
ax1.set_xlabel('time [s]')
ax1.set_ylabel('RSS [GB]')
ax1.plot(x2,y2, c='#FFB000', label='This PR @fb67ef3: 100k events')
ax1.plot(x,y, c='#785EF0', label='PromptCalibProdSiStrip')
ax1.plot(x3,y3, c='#648FFF', label='step3')
Leg = ax1.legend(['step 2+3 squashed', 'step 2 à la PCL',  'step 3 à la PCL'],loc="upper right", bbox_to_anchor=(1.0,0.85))
#ax1.axvline(x=x[-1], color='k', linestyle='--', label='Step 2 end')
# ax1.grid(color='grey', linestyle='-', linewidth=0.3) # You can remove this line as darkgrid provides its own grid
plt.show()
fig.savefig('./memory.png')
