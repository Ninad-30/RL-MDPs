import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()




class CricketMDP():
    def __init__(self):
        self.statesA = []
        self.statesB = []
        self.states = []
        self.parametersA = []
        self.parametersB = []
        self.q = 0
        self.balls = 0
        self.runs = 0
        self.terminal_states = ['out', 'balls_over', 'win']
        self.actionsA = [0,1,2,4,6] # The attempts
        self.outcomesA = [-1,0,1,2,3,4,6] # The outcomes
        self.outcomesB = [-1,0,1]

    def set_env(self, states, parameters, q):

        with open(states, 'r') as states:
            for state in states.readlines():
                self.statesA.append(state.strip().join("A"))
                self.statesB.append(state.strip().join("B"))
            self.states = self.statesA + self.statesB + self.terminal_states

        with open(parameters, 'r') as params:
            for param in params.readlines()[1:]:
                self.parameters.append(param.strip())
        
        self.balls = self.states[0][:2]
        self.runs = self.states[0][2:]
        self.q = float(q)
        self.parametersB = [self.q, (1-self.q)/2, (1-self.q)/2]
        
        self.T = np.zeros((len(self.states),len(self.actions),len(self.states)))
        self.R = np.zeros((len(self.states),len(self.actions),len(self.states)))

    def set_TandR(self):
        




if __name__ == "__main__":
    parser.add_argument("--states", type=str, help="Path to the cricket file")
    parser.add_argument("--mdp", type=str, help="Path to the MDP file")
    parser.add_argument("--parameters", type=str, help="Path to the environment parameters")
    parser.add_argument("--q", type=float, help="Weakness of the player")
    args = parser.parse_args()

    Cricket = CricketMDP()
    Cricket.set_env(args.states, args.parameters, args.q)
    print(Cricket.states)
    print(Cricket.parameters)
    print(Cricket.balls, Cricket.runs, Cricket.q)

    ## IDK what to do next???
    ## Mu me lo




    

    
