import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()
from planner import MDP



class CricketMDP(MDP):
    def __init__(self, states):
        super().__init__(self)
        self.states = states
    




if __name__ == "__main__":
    parser.add_argument("--states", type=str, help="Path to the cricket file")
    parser.add_argument("--mdp", type=str, help="Path to the MDP file")
    parser.add_argument("--parameters", type=str, help="Path to the environment parameters")
    parser.add_argument("--q", type=float, help="Weakness of the player")
    args = parser.parse_args()

    CricketGame = CricketMDP()
    with open(args.states, 'r') as states:
        lines = states.readlines()
        listofstates = []
        for state in lines:
            listofstates.append(int(lines.strip()))
        CricketGame.states = listofstates
    ## IDK what to do next???



    




    

    
