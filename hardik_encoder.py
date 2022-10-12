#! /usr/bin/python
import random,argparse,sys
parser = argparse.ArgumentParser()
import numpy as np
import pulp

class Encoder():
    def __init__(self, states_path, parameters_path, q):
        self.states_path = states_path
        self.parameters_path = parameters_path
        self.q = q
        
        self.states = []
        self.states2 = []
        self.states1 = []
        self.parameters1 = []
        self.parameters = []
        self.balls = 0
        self.runs = 0

        with open(self.states_path) as f:
            for line in f.readlines():
                self.states1.append(line)

        for line in self.states1:
            line = line.split()
            self.states2.append(line)
        
        with open(self.parameters_path) as f:
            for line in f.readlines():
                self.parameters1.append(line)

        for line in self.parameters1:
            line = line.split()
            self.parameters.append(line)
        # self.n = len(self.input)
        self.states2 = np.array(self.states2)
        for x in self.states2:
            self.states.append(x[0])
        bbrr = self.states[0]
        self.states = np.flip(self.states)
        # print("states", self.states)

        self.parameters = np.array(self.parameters)
        self.parameters = np.delete(self.parameters, 0, 0)
        self.parameters = np.delete(self.parameters, 0, 1)
        self.parameters = self.parameters.astype(float)
        # print("Parameters", self.parameters)

        # Finding intial balls and runs required
        self.balls = int(bbrr[0:2])
        self.runs = int(bbrr[2:4])
        self.n = self.balls * self.runs

        # print("balls", self.balls)
        # print("runs", self.runs)
        
        self.terminal_states = np.array(["lose", "win"])
        self.states = np.append(self.states, self.states)
        self.states = np.append(self.states, self.terminal_states)
        # print(self.states)
        # first n states are for batter A on strike and other n are for batter B on strike
        # Last 2 are lose and win whcih are terminal states
        self.actionsA = [0, 1, 2, 4, 6]
        # states and parameters are read
        # self.transitions = []
        self.outcomes = [-1, 0, 1, 2, 3, 4, 6]
        self.parameters_B = [self.q, (1 - self.q)/2, (1 - self.q)/2]
        self.outcomes_B = [-1, 0, 1]
        
        # printing things needed before transitions
        print("numStates", 2*self.n + 2)
        print("numActions", 5)
        print("end", 2*self.n, 2*self.n + 1)
        ###########################################

        # Going over all states except terminal states and generating transitions from them
        for i in range(2*self.n):

            curr_state = self.states[i]
            if(curr_state == 'lose' or curr_state == 'win'):
                pass # No transitions will take place from terminal states
            else:
                curr_balls = int(curr_state[0:2])
                # print("curr_balls", curr_balls)
                curr_runs = int(curr_state[2:4])
                # print("curr_runs", curr_runs)

            if(i < self.n):
                # A has strike
                #looping over all actions a batter can do
                for a in range(len(self.actionsA)):
                    # one ball will be reduced
                    next_state_balls = curr_balls - 1

                    # loop over all outcomes by each action of A
                    for j in range(len(self.outcomes)):
                        next_state_runs = curr_runs - self.outcomes[j]
                        prob = self.parameters[a][j]

                        if(self.outcomes[j] == -1 or (next_state_runs > 0 and next_state_balls == 0)):# condition of lose
                            next_state_id = 2*self.n #lose state
                            print("transition", i, a, next_state_id, 0, prob)

                        else: # cases other than lose
                            next_state_id = (next_state_balls - 1)*self.runs + (next_state_runs - 1)
                            win_flag = False
                            if(next_state_runs <= 0 and next_state_balls >= 0): # conditon of win
                                next_state_id = 2*self.n + 1 # win state
                                win_flag = True
                                print("transition", i, a, next_state_id, 1, prob)

                            flag_B = False

                            if(next_state_balls % 6 == 0 and (self.outcomes[j] == 1 or self.outcomes[j] == 3)):
                                flag_B = False ## Over change and odd runs
                            elif(next_state_balls % 6 != 0 and (self.outcomes[j] == 1 or self.outcomes[j] == 3)):
                                flag_B = True   ## Over not change and odd runs
                            elif(next_state_balls % 6 == 0 and (self.outcomes[j] == 0 or self.outcomes[j] == 2 or self.outcomes[j] == 4 or self.outcomes[j] == 6)):
                                flag_B = True   ## over changes and even runs
                            else:   ## Over not changes and even runs
                                flag_B = False

                            reward = 0
                            if(next_state_id == 2*self.n + 1): ## win state
                                reward = 1

                            # B gets strike
                            if(win_flag):   # If won then transition already printed
                                pass
                            else:       # If not won
                                if(flag_B):
                                    next_state_id = (next_state_id + self.n) # If B gets strike then we will go to B's states half

                                    print("transition", i, a, next_state_id, reward, prob)

                                # A keeps strike
                                else:

                                    print("transition", i, a, next_state_id, reward, prob)

            else:
                # B has strike
                #looping over all actions a batter can do
                for a in range(len(self.actionsA)):
                    next_state_balls = curr_balls - 1

                    # loop over all outcomes by each action of B
                    for j in range(len(self.outcomes_B)):
                        next_state_runs = curr_runs - self.outcomes_B[j]
                        prob = self.parameters_B[j]

                        if(self.outcomes_B[j] == -1):
                        #  or (next_state_runs > 0 and next_state_balls == 0)):# condition of lose
                            next_state_id = 2*self.n #lose state
                            print("transition", i, a, next_state_id, 0, prob)

                        else: # cases other than -1

                            if(self.outcomes_B[j] == 0): # Can't go in win state
                                if(next_state_balls % 6 != 0): # B keeps strike
                                    next_state_id = (next_state_balls - 1)*self.runs + (curr_runs - 1) + self.n
                                else:   # strike rotates
                                    next_state_id = (next_state_balls - 1)*self.runs + (curr_runs - 1)

                                if(next_state_balls == 0):
                                    next_state_id = 2*self.n # lose state
                                # print("balls", curr_balls)
                                # print("runs", curr_runs)
                                print("transition", i, a, next_state_id, 0, self.parameters_B[1])

                            else:
                                next_state_runs = curr_runs - 1 # B scored one run
                                if(next_state_balls % 6 != 0): # B keeps strike
                                    next_state_id = (next_state_balls - 1)*self.runs + (next_state_runs - 1)
                                else: # strike rotates
                                    next_state_id = (next_state_balls - 1)*self.runs + (next_state_runs - 1) + self.n
                                reward = 0
                                if(next_state_runs == 0):
                                    next_state_id = 2*self.n + 1 # win state
                                    reward = 1

                                if(next_state_balls == 0 and next_state_runs > 0):
                                    next_state_id = 2*self.n # lose state

                                # print("balls", curr_balls)
                                # print("runs", curr_runs)

                                print("transition", i, a, next_state_id, reward, self.parameters_B[2])


###############################Old part####################

                # B has strike
                # We have no choice over B's action, it will be determined by environment using q
                # B_result = np.random.choice(self.outcomes_B, 1, self.parameters_B)
                # for h in range(3): # looping over outcomes of B
                #     B_result = self.outcomes_B[h]
                #     # print("B_result", B_result)
                #     next_state_balls = curr_balls - 1

                #     if(B_result == -1):
                #         # or (next_state_balls == 0 and next_state_runs > 0)):
                #         next_state_id = 2*self.n #lose state
                #         # print("balls", curr_balls)
                #         # print("runs", curr_runs)

                #         print("transition", i, 5, next_state_id, 0, self.parameters_B[0])

                #     else:

                #         if(B_result == 0): # Can't go in win state
                #             next_state_id = (next_state_balls - 1)*self.runs + curr_runs + self.n
                #             if(next_state_balls == 0):
                #                 next_state_id = 2*self.n # lose state
                #             # print("balls", curr_balls)
                #             # print("runs", curr_runs)

                #             print("transition", i, 5, next_state_id, 0, self.parameters_B[1])

                #         else:
                #             next_state_runs = curr_runs - 1
                #             next_state_id = (next_state_balls - 1)*self.runs + next_state_runs
                #             reward = 0
                #             if(next_state_runs == 0):
                #                 next_state_id = 2*self.n + 1 # win state

                #             if(next_state_balls == 0 and next_state_runs > 0):
                #                 next_state_id = 2*self.n # lose state

                #             if(next_state_id == 2*self.n + 1): # win case
                #                 reward = 1
                #             # print("balls", curr_balls)
                #             # print("runs", curr_runs)

                #             print("transition", i, 5, next_state_id, reward, self.parameters_B[2])
##################################################################################
        print("mdptype", "episodic")
        print("discount", 1)




if __name__ == "__main__":
    parser.add_argument("--states",type=str)
    parser.add_argument("--parameters",type=str)
    parser.add_argument("--q",type=float)

    args = parser.parse_args()
    Encoder(args.states, args.parameters, args.q)



