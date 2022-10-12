#! /usr/bin/python
import random,argparse,sys
parser = argparse.ArgumentParser()
import numpy as np
# import pulp

class Decoder():
    def __init__(self, path, states_path):
        self.path = path
        self.states_path = states_path
        self.input1 = []
        self.input = []

        self.states = []
        self.states2 = []
        self.states1 = []
        self.actions = [0, 1, 2, 4, 6]

        with open(self.states_path) as f:
            for line in f.readlines():
                self.states1.append(line)

        for line in self.states1:
            line = line.split()
            self.states2.append(line)
        
        self.states2 = np.array(self.states2)
        for x in self.states2:
            self.states.append(x[0])
        
        with open(self.path) as f:
            for line in f.readlines():
                self.input1.append(line)

        for line in self.input1:
            line = line.split()
            self.input.append(line)

        self.n = len(self.input)
        self.n = int((self.n - 2)/2)
        self.input = self.input[0:self.n]
        # print(self.input)
        self.input = np.flip(self.input)
        for x in range(len(self.input)):
            # print("xx", self.input[x][0])
            print(self.states[x], self.actions[int(float(self.input[x][0]))], self.input[x][1])
        
        
if __name__ == "__main__":
    # parser.add_argument("--value-policy",type=str)
    parser.add_argument("--value-policy",type=str)
    parser.add_argument("--states",type=str)
    args = parser.parse_args()

    Decoder(args.value_policy, args.states)


    


