import os
import matplotlib.pyplot as plt                  

def run(q):
    os.system("python encoder.py --states cricket_state_list.txt --parameters data/cricket/sample-p1.txt --q " + str(q) + "> mdpfile.txt")
    os.system("python planner.py --mdp mdpfile.txt > policy_value_file.txt")
    os.system("python decoder.py --states cricket_state_list.txt --value-policy policy_value_file.txt > policyfile")

    with open("policyfile") as f:
        line = f.readline()

    line = line.split()
    ans1 = float(line[2])

    print("completed ans1")

    os.system("python planner.py --mdp mdpfile.txt --policy new_rand_pol.txt > policy_value_file.txt")
    os.system("python decoder.py --states cricket_state_list.txt --value-policy policy_value_file.txt > policyfile")
    
    with open("policyfile") as f:
        line = f.readline()

    line = line.split()
    ans2 = float(line[2])

    return ans1, ans2

if __name__ == "__main__":
    
    q_array = []
    prob_array_1 = []
    prob_array_2 = []
    for i in range(21):
        q_array.append(i/20)
        x = run(i/20)
        prob_array_1.append(x[0])
        prob_array_2.append(x[1])
    plt.xlabel("B's Weakness(q)")
    plt.ylabel("Probability of winning")
    
    plt.plot(q_array, prob_array_1)
    plt.plot(q_array, prob_array_2)
    plt.legend(["Optimal Policy", "Random Policy"])
    plt.savefig("plot1.jpg")
    plt.show()

