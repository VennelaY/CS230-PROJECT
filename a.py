import sys
import os
import numpy as np
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

trace = sys.argv[1]
trace += ".xz"
N_warm = sys.argv[2]
N_sim = sys.argv[3]

LLCways = [4,16,32]
L2Cways = [2,8,16]
L1Dways = [3,12,24]
L1Iways = [2,8,16]
TOTAL_SIZE = 2048*16

def changeWAYS(LLCway, prevLLCWay,L2Cway, prevL2CWay,L1Dway, prevL1DWay,L1Iway, prevL1IWay):
    #read input file
    fin = open("./inc/cache.h", "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    #prevset = TOTAL_SIZE//prevWay
    #newset = TOTAL_SIZE//way
    #data = data.replace('LLC_SET NUM_CPUS*%d'%prevset, 'LLC_SET NUM_CPUS*%d'%newset)
    data = data.replace('LLC_WAY %d'%prevLLCWay, 'LLC_WAY %d'%LLCway)
    data = data.replace('L1I_WAY %d'%prevL1IWay, 'L1I_WAY %d'%L1Iway)
    data = data.replace('L1D_WAY %d'%prevL1DWay, 'L1D_WAY %d'%L1Dway)
    data = data.replace('L2C_WAY %d'%prevL2CWay, 'L2C_WAY %d'%L2Cway)
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open("./inc/cache.h", "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

def find_ipc_LLCmissrate(file, nsim):
    folder = 'results_' + str(nsim) + 'M'
    ipc = None
    search_ipc = "cumulative IPC:"
    LLCmissrate = None
    search_LLCmissrate = "LLC TOTAL ACCESS: HIT: MISS:"
    with open("./%s/%s"%(folder, file), 'rt') as fin:
        for line in fin:
            found = True
            for wordie in search_ipc.split():
                if wordie not in line.split():
                    found = False
                    break
            # if all(word in line.split() for word in search_ipc.split()):
            if found:
                # Search for the first unknown string
                word = line.split(search_ipc)
                wordList = word[1].split()
                ipc = float(wordList[0])
            found = True
            for wordie in search_LLCmissrate.split():
                if wordie not in line.split():
                    found = False
                    break
            # if all(word in line.split() for word in search_LLCmissrate.split()):
            if found:
                # Search for the second unknown string
                access = None
                miss = None
                wordList = line.split()
                for word in wordList:
                    if word=="ACCESS:":
                        access = wordList[wordList.index(word)+1]
                    elif word=="MISS:":
                        miss = wordList[wordList.index(word)+1]
                if access is not None and miss is not None:
                    LLCmissrate = (float(miss)/float(access))*100
            if ipc is not None and LLCmissrate is not None:
                # Both unknown strings found
                return(ipc, LLCmissrate)
    

policies = ['lru','lfu', 'fifo', 'rnd']
plotdata = []

prevLLCWay = 32
prevL2CWay = 16
prevL1DWay = 24
prevL1IWay = 16
for i in range(3):
    changeWAYS(LLCways[i], prevLLCWay,L2Cways[i], prevL2CWay,L1Dways[i], prevL1DWay,L1Iways[i], prevL1IWay)
    prevLLCWay = LLCways[i]
    prevL2CWay = L2Cways[i]
    prevL1DWay = L1Dways[i]
    prevL1IWay = L1Iways[i]
    #now build binary file for lfu, fifo and rnd replacement policies
    policywiseData = []
    for policy in policies:
        os.system('./build_champsim.sh bimodal no no no no ' + policy + ' 1')
        os.system('./run_champsim.sh bimodal-no-no-no-no-' + policy + '-1core ' + N_warm + " " + N_sim + " " + trace)
        resultfile = trace + '-bimodal-no-no-no-no-' + policy + '-1core.txt'
        policywiseData.append(find_ipc_LLCmissrate(resultfile, N_sim))
        
    plotdata.append(policywiseData)
i = 0
for diffWays in plotdata:
    print("LLC_Way: ",end="")
    print(LLCways[i], ": ")
    print("L2C_Way: ",end="")
    print(L2Cways[i], ": ")
    print("L1D_Way: ",end="")
    print(L1Dways[i], ": ")
    print("L1I_Way: ",end="")
    print(L1Iways[i], ": ")
    i += 1
    for diffPol in diffWays:
        print(diffPol)
    print("\n")

#plotting, we generate two different plots for ipc and LLC miss rate
N = 3
ind = np.arange(N)
# ind = [0,1,2,3]
width = 0.2

#data--ipc
lruipc = [plotdata[0][0][0], plotdata[1][0][0],  plotdata[2][0][0]]
lfuipc = [plotdata[0][1][0], plotdata[1][1][0], plotdata[2][1][0]]
fifoipc = [plotdata[0][2][0], plotdata[1][2][0],  plotdata[2][2][0]]
rndipc = [plotdata[0][3][0], plotdata[1][3][0],  plotdata[2][3][0]]

#data--LLC miss rate
lruLLCmissrate = [plotdata[0][0][1], plotdata[1][0][1],  plotdata[2][0][1]]
lfuLLCmissrate = [plotdata[0][1][1], plotdata[1][1][1],  plotdata[2][1][1]]
fifoLLCmissrate = [plotdata[0][2][1], plotdata[1][2][1], plotdata[2][2][1]]
rndLLCmissrate = [plotdata[0][3][1], plotdata[1][3][1], plotdata[2][3][1]]

plt.subplot(1,2,1)
bar1 = plt.bar(ind, lfuipc, width, color = 'r')
bar2 = plt.bar(ind+width, fifoipc, width, color='g')
bar3 = plt.bar(ind+width*2, rndipc, width, color = 'b')
bar4 = plt.bar(ind+width*3, lruipc, width, color = 'c')

ymin, ymax = 0.25, 0.35
plt.ylim(ymin, ymax)

# Generate 100 evenly spaced y-coordinates between ymin and ymax
y_ticks = np.linspace(ymin, ymax, 20)

# Set y-tick positions and labels
plt.yticks(y_ticks)
plt.xlabel("Number of llc_ways")
plt.ylabel("IPC")
plt.xticks(ind+width,['4', '16', '32'])
plt.legend( (bar1, bar2, bar3, bar4), ('LFU', 'FIFO', 'rnd', 'LRU') )
plt.title("Comparing IPC values for different replacement policies for different way values", fontsize=10)

plt.subplot(1,2,2)
bar5 = plt.bar(ind, lfuLLCmissrate, width, color = 'r')
bar6 = plt.bar(ind+width, fifoLLCmissrate, width, color='g')
bar7 = plt.bar(ind+width*2, rndLLCmissrate, width, color = 'b')
bar8 = plt.bar(ind+width*3, lruLLCmissrate, width, color = 'c')
plt.xlabel("Number of llc_ways")
plt.ylabel("LLC miss rate %")
plt.xticks(ind+width,['4', '16', '32'])
plt.legend( (bar5, bar6, bar7, bar8), ('LFU', 'FIFO', 'rnd', 'LRU') )
plt.title("Comparing LLC miss rates for different replacement policies for different way values", fontsize=10)

plt.suptitle("Plot for trace " + trace,fontsize=20, fontweight='bold')
plt.show()
