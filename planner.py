import numpy as np
import pulp
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()

# import warnings
# warnings.filterwarnings("ignore")

# Value Iteration Algo:
# Initialize, V <- arbitary bounded vector of size num_states
# Repeat:

# for all s, V <- max a of sum(T(s,a,s'){R(s,a,s') + gamma*V(s')})


# Linear Programming Algo:
# Max(-sum(V(s))) subject to V(s) >= sum(T(s,a,s'){R(s,a,s') + gamma*V(s')})
# V* is the unique solution to this LP. 


# Howard's Policy Iteration:
# Greedy, improve all current improvable states
# For a state s, if Q(s,a) > V(s) for a policy pi, then the state s can be improved
# Update the policy to choose such a state s above
# Once there are no such states left, the policy obtained is optimal, pi*

class MDP:
    def __init__(self, numStates=0, numActions=0, mdptype=None, discount=0, endStates=None):
        self.numStates = numStates
        self.numActions = numActions
        self.mdptype = mdptype
        self.T = np.zeros((self.numStates,self.numActions,self.numStates))
        self.R = np.zeros((self.numStates,self.numActions,self.numStates))
        self.gamma = discount
        self.endStates = endStates
        self.validStates = [i for i in range(self.numStates)]
        for end in self.endStates:
            if end == -1:
                break
            else:
                self.validStates.remove(end)


    def set_TandR_probs(self, T):
        # here T has to be list containing lines directly from the mdp txt file
        for t1 in T:
            self.R[int(t1[0]),int(t1[1]),int(t1[2])] = float(t1[3])
            self.T[int(t1[0]),int(t1[1]),int(t1[2])] = float(t1[4])

    def readPolicy(self, policy_file):
        V_pi = [0]*self.numStates
        with open(policy_file, 'r') as pf:
            lines = pf.readlines()
            for i in range(len(lines)):
                V_pi[i] = int(lines[i].strip())
        return np.array(V_pi)


    def Value_Iteration(self):
    
        V = np.zeros(self.numStates)
        PI = np.zeros(self.numStates,dtype=int)
        
        while(True):
            max_diff = 0
            V_new = np.zeros_like(V)
            for s0 in self.validStates:
                aV = []
                for a in range(self.numActions):
                    sumV = 0
                    for s in range(self.numStates):
                        
                        sumV += self.T[s0,a,s]*(self.R[s0,a,s]+self.gamma*V[s])
                    aV.append(sumV)

                V_new[s0] = max(aV)
                max_diff = max(max_diff, abs(V_new[s0]-V[s0]))
                PI[s0] = np.argmax(aV)
            V = V_new
            if max_diff <= 1e-10:
                break            

        return np.array(V), np.array(PI)


    def EvaluatePolicy(self, PI):

        V = np.zeros(self.numStates)
        while(True):
            max_diff = 0
            V_new = np.zeros_like(V)
            for s0 in self.validStates:
                sumV = 0
                a = PI[s0]
                for s in range(self.numStates):
                    sumV += self.T[s0,a,s]*(self.R[s0,a,s]+self.gamma*V[s])
                V_new[s0] = sumV
                max_diff = max(max_diff, abs(V_new[s0]-V[s0]))
            V = V_new
            if max_diff <= 1e-10:
                break


        return np.array(V)


    def Howards_PI(self):
       
        V = np.zeros(self.numStates)
        Q = np.zeros((self.numStates,self.numActions))
        PI = np.zeros(self.numStates,dtype=int)
        improvable_states = [s for s in self.validStates]

        while(True):
        # Policy Evaluation
            max_diff = 0
            V_new = np.zeros_like(V)
            for s0 in self.validStates:
                sumV = 0
                a = PI[s0]
                for s in range(self.numStates):
                    sumV += self.T[s0,a,s]*(self.R[s0,a,s]+self.gamma*V[s])
                V_new[s0] = sumV
                max_diff = max(max_diff, abs(V_new[s0]-V[s0]))
            V = V_new
            if max_diff <= 1e-10:
                break

            # Policy Iteration
            # To find improvable states
            for s0 in improvable_states:
                for a in range(self.numActions):
                    Q_new = 0
                    for s in range(self.numStates):
                        Q_new += self.T[s0,a,s]*(self.R[s0,a,s] + self.gamma*V[s])
                    Q[s0,a] = Q_new
            
            # Have Q[s,a] for every state-action pair
            for s in improvable_states:
                maxQ = Q[s,PI[s]]
                isImproved = False
                for a in range(self.numActions):
                    # Determing the action which has the higest Q(s,a), for policy improvement
                    if Q[s,a] - V[s]:
                        if Q[s,a] > maxQ:
                            PI[s] = a
                        isImproved = True
                if not isImproved:
                    improvable_states.pop(s)
            
        return V, PI
            

    def LP(self):

        states = range(self.numStates)

        V = pulp.LpVariable.dicts("V", states, cat="Continuous")
        Obj = pulp.LpProblem("Maximize_negative_of_sum_of_Values", pulp.LpMaximize)
        Obj += pulp.lpSum([-V[s] for s in states])
    
        for s0 in states:  
            for a in range(self.numActions):
                Obj += V[s0] >= pulp.lpSum([self.T[s0,a,s]*(self.R[s0,a,s] + self.gamma*V[s]) for s in states])

        Obj.solve(pulp.PULP_CBC_CMD(msg=False))
        V_soln = np.array([V[s].varValue for s in states])
        PI_soln = np.zeros(self.numStates)
        for s0 in range(self.numStates):
            aV = []
            for a in range(self.numActions):
                sumV = 0
                for s in range(self.numStates):
                    sumV += self.T[s0,a,s]*(self.R[s0,a,s] + self.gamma*V_soln[s])
                aV.append(sumV)
            PI_soln[s0] = int(np.argmax(aV))

        return V_soln, PI_soln




if __name__ == "__main__":
    parser.add_argument('--mdp', type=str, help='Path to the MDP file')
    parser.add_argument('--algorithm', type=str, default='default', help='The algorithm used to find the optimal policy and value function')
    parser.add_argument('--policy', type=str, default = None, help='Path to the file specifying a policy for the given MDP')
    args = parser.parse_args()

    with open(args.mdp,'r') as mdp_info:
        lines = mdp_info.readlines()
        # each line of the txt file is a string in a list
        numStates = int(lines[0].split()[1])
        numActions = int(lines[1].split()[1])
        endStates = lines[2].split()[1:]
        endStates = [int(end) for end in endStates]
        mdptype = lines[-2].split()[1]
        discount = float(lines[-1].split()[1])

        mdp = MDP(numStates,numActions, mdptype, discount, endStates)
        t = []
        for i in range(len(lines)):
            l = lines[i].split()
            if l[0] == "transition":
                t.append(l[1:])
        mdp.set_TandR_probs(t)
    
    if args.policy is not None:
        PI = mdp.readPolicy(args.policy)
        V_pi = mdp.EvaluatePolicy(PI)
        # print(PI)
        # print(V_pi)
        for i in range(numStates):
            # print(type(PI[i]))
            # print(type(V_pi[i]))
            print(round(V_pi[i],6),PI[i])

    else:                
        if args.algorithm == 'vi':
            # print(mdp.mdptype)
            # print(mdp.endStates, mdp.validStates)
            V_star, pi_star = mdp.Value_Iteration()
        elif args.algorithm == 'hpi':
            V_star, pi_star = mdp.Howards_PI()
        elif args.algorithm == 'lp':
            V_star, pi_star = mdp.LP()
        elif args.algorithm == 'default':
            V_star, pi_star = mdp.Value_Iteration()
                                    
        for i in range(numStates):
            print(round(V_star[i],6), pi_star[i])
        




