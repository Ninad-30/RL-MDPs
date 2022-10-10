import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
parser = ArgumentParser()




class CricketMDP():
    def __init__(self):
    
        self.states = []
        self.parametersA = []
        self.parametersB = []
        self.q = 0
        self.balls = 0
        self.runs = 0
        self.terminal_states = ['out', 'balls_over', 'win']
        self.actionsA = [0,1,2,4,6] # The attempts
        self.outcomesA = [-1,0,1,2,3,4,6] # The outcomes for A
        self.outcomesB = [-1,0,1] # The outcomes for B
        self.terminal_states = ['won','lost']
        

    def set_game(self, states, parameters, q):

        with open(states, 'r') as states:
            for state in states.readlines():
                self.states.append(state.strip())
            self.states *= 2
            self.states += self.terminal_states 

        with open(parameters, 'r') as params:
            for param in params.readlines()[1:]:
                param = param.split()
                self.parametersA.append(param[1:])
        
        self.tot_balls = int(self.states[0][:2])
        self.tot_runs = int(self.states[0][2:])
        self.q = float(q)
        self.parametersB = [self.q, (1-self.q)/2, (1-self.q)/2]
        self.strike_rot = self.tot_balls * self.tot_runs
    
    def determineMDPvalues(self):

        print("numStates", len(self.states))
        print("numActions", len(self.actionsA)) # 0,1,2,4,6
        print("end", len(self.states)-1, len(self.states)-2)
        print("transition", "s", "a", "s", "r", "prob")
        for i,state in enumerate(self.states):
            # Determining the current situation
            curr_state = state
            if(curr_state == "lost" or curr_state == "won"):
                continue
            else:
                balls_left = int(curr_state[0:2])
                runs_left = int(curr_state[2:4])

            # Condition if A has strike
            if i < self.strike_rot:

                for a in range(len(self.actionsA)):
                    virtual_balls = balls_left - 1
                    for o,outcome in enumerate(self.outcomesA):

                        virtual_runs = runs_left - outcome
                        prob = self.parametersA[a][o]
                        #print(f"action taken: {a}, outcome: {outcome}, virtual runs: {virtual_runs}")
                        if outcome == -1 or (virtual_runs > 0 and virtual_balls == 0):
                            # Game lost
                            state_jump_id = len(self.states)-1
                            reward = 0
                            print("transition", i, self.actionsA[a], state_jump_id, reward, prob)
                        
                        elif virtual_runs <= 0 and virtual_balls >= 0:
                            # Game won
                            state_jump_id = len(self.states)-2
                            reward = 1
                            print("transition", i, self.actionsA[a], state_jump_id, reward, prob)

                        else:
                            #print("Game continues")
                            # Logical EXOR conditon between if its ball and whether even number of runs are scored and Game continues
                            if (outcome%2 == 0) != (virtual_balls%6 == 0):
                                # Change strike if odd runs are score and its not the last ball
                                # Change strike if even runs are scored and it is the last ball
                                state_jump_id = ((virtual_balls - 1)*self.runs + virtual_runs)%self.strike_rot + 1
                                print("transition", i, self.actionsA[a], state_jump_id, reward, prob)
                            else:
                                # Dont change strike
                                state_jump_id = (virtual_balls - 1)*self.runs + virtual_runs
                                print("transition", i, self.actionsA[a], state_jump_id, reward, prob) 

            # Condition if B has strike
            else:

                for o,outcome in enumerate(self.outcomesB):
                    virtual_balls = balls_left - 1
                    virtual_runs = runs_left - outcome
                    prob = self.parametersB[o]

                    if outcome == -1:
                        state_jump_id = len(self.states)-1
                        reward = 0
                        print("transition", i, 5, state_jump_id, reward, prob)
                    
                    elif outcome == 0:
                        state_jump_id = (virtual_balls - 1)*self.runs + runs_left + self.strike_rot
                        if virtual_runs > 0 and virtual_balls <= 0:
                            # Game lost
                            state_jump_id = len(self.states)-1
                            reward = 0
                            print("transition", i, 5, state_jump_id, reward, prob)
                    
                    else:
                        if virtual_runs <= 0 and virtual_balls >= 0:
                            # Game won
                            state_jump_id = len(self.states)-2
                            reward = 1
                            print("transition", i, 5, state_jump_id, reward, prob)
                        else:
                            # Game continues and strike changes
                            state_jump_id = (virtual_balls - 1)*self.runs + virtual_runs
                            reward = 0
                            print("transition", i, 5, state_jump_id, reward, prob)

        print("mdptype", "episodic")
        print("discount", 1)




# 1015 state, action-> 0,1,2,4,6, outcome-> -1,0,1,2,3,4,6
        




if __name__ == "__main__":
    parser.add_argument("--states", type=str, help="Path to the cricket file")
    parser.add_argument("--mdp", type=str, help="Path to the MDP file")
    parser.add_argument("--parameters", type=str, help="Path to the environment parameters")
    parser.add_argument("--q", type=float, help="Weakness of the player")
    args = parser.parse_args()

    Cricket = CricketMDP()
    Cricket.set_game(args.states, args.parameters, args.q)
    # print(Cricket.parametersA)
    # print(Cricket.parametersB)
    print(Cricket.states)
    print(Cricket.parametersA)
    Cricket.determineMDPvalues()
    ## IDK what to do next???
    ## Mu me lo




    

    
