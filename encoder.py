import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()
from planner import MDP



class CricketMDP(MDP):
    def __init__(self):
        pass
    




if __name__ == "__main__":
    parser.add_argument("--states", type=str, help="Path to the cricket file")
    parser.add_argument("--mdp", type=str, help="Path to the MDP file")
    parser.add_argument("--parameters", type=str, help="Path to the environment parameters")
    parser.add_argument("--q", type=float, help="Weakness of the player")


    

    
