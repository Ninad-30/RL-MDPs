import os
import matplotlib.pyplot as plt                  

os.system("python encoder.py --states cricket_state_list.txt --parameters data/cricket/sample-p1.txt --q " + str(0.25) + "> mdpfile.txt")
os.system("python planner.py --mdp mdpfile.txt > policy_value_file.txt")
os.system("python decoder.py --states states --value-policy policy_value_file.txt > policyfile")

opt_pol = []
for i in range(20):
    opt_pol.append(0)

with open("policyfile") as f:
    for line in f:
        balls = 10*int(line[0])+int(line[1])
        runs = 10*int(line[2])+int(line[3])
        if(balls == 10 and runs<21):
            opt_pol[runs-1] = float((line.split())[2])

os.system("python planner.py --mdp mdpfile.txt --policy new_rand_pol.txt > policy_value_file.txt")
os.system("python decoder.py --states cricket_state_list.txt --value-policy policy_value_file.txt > policyfile")

rand_pol = []
for i in range(20):
    rand_pol.append(0)

with open("policyfile") as f:
    for line in f:
        balls = 10*int(line[0])+int(line[1])
        runs = 10*int(line[2])+int(line[3])
        if(balls == 10 and runs<21):
            rand_pol[runs-1] = float((line.split())[2])

x = range(1,21)
plt.xlabel("Required runs")
plt.ylabel("Win Probability")
plt.plot(x, opt_pol)
plt.plot(x, rand_pol)
plt.legend(["Optimal Policy", "Random Policy"])
plt.savefig("plot2.jpg")
plt.show()