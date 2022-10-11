import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()



inv_action_map = {0:0, 1:1, 2:2, 3:4, 4:6}

if __name__ == "__main__":
    parser.add_argument("--states", type=str, help="Path to the cricket file")
    parser.add_argument("--value-policy", type=str, help="Path to the value and policy MDP file")
    
    args = parser.parse_args()
    states = []
    with open(args.states, 'r') as f:
        lines = f.readlines()
        for line in lines:
            states.append(line.strip())
    value_func = []
    policy = []
    with open(args.value_policy,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            value_func.append(line[0])
            policy.append(line[1])

    for i in range(int(len(states))):
        print(states[i], inv_action_map[int(policy[i])], value_func[i])




    