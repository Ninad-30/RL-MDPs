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
        self.actions = [0,1,2,4,6] # The attempts
        self.outcomesA = [-1,0,1,2,3,4,6] # The outcomes for A
        self.outcomesB = [-1,0,1] # The outcomes for B
        self.terminal_states = ['won','lost']
        self.action_index_map = {0:0, 1:1, 2:2, 4:3, 6:4}
        

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
        print("numActions", len(self.actions)) # 0,1,2,4,6
        print("end", len(self.states)-2, len(self.states)-1)
        debug_log = False
        #print("transition", "s", "a", "s", "r", "prob")
        if debug_log:
            for i,state in enumerate(self.states):
                if i == len(self.states)-1 or i == len(self.states)-2:
                    break
                # Determining the current situation
                curr_state = state
                if(curr_state == "lost" or curr_state == "won"):
                    continue
                else:
                    balls_left = int(curr_state[0:2])
                    runs_left = int(curr_state[2:4])

                # Condition if A has strike
                if i < self.strike_rot:

                    for a in range(len(self.actions)):
                        virtual_balls = balls_left - 1
                        balls_done = self.tot_balls - virtual_balls
                        virtual_states_probs = {}

                        for o,outcome in enumerate(self.outcomesA):
                            virtual_runs = runs_left - outcome
                            prob = float(self.parametersA[a][o])
                            
                            if outcome == -1 or (virtual_runs > 0 and virtual_balls == 0):
                                # Game lost
                                state_jump_id = len(self.states)-1

                                print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                if state_jump_id not in virtual_states_probs:
                                    virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob
                                
                            
                            elif virtual_runs <= 0 and virtual_balls >= 0:
                                # Game won
                                state_jump_id = len(self.states)-2

                                print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")
                                
                                if state_jump_id not in virtual_states_probs:
                                    virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob
                                

                            else:
                                #print("Game continues")
                                # Logical EXOR conditon between if its ball and whether even number of runs are scored and Game continues
                                vstate_id = i + self.tot_runs + outcome 
                                #   True                 
                                if (outcome%2 == 0) == (virtual_balls%6 == 0):
                                    # Change strike if odd runs are score and its not the last ball
                                    # Change strike if even runs are scored and it is the last ball
                                    #print(vstate_id, self.strike_rot, len(self.states)-2)
                                    state_jump_id = (vstate_id + self.strike_rot)%(len(self.states))

                                    print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike changed")
                                    
                                    if state_jump_id not in virtual_states_probs:
                                        virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                                    
                                else:
                                    # Dont change strike
                                    state_jump_id = vstate_id

                                    print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    if state_jump_id not in virtual_states_probs:
                                        virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                        prob_sum = 0
                        
                        for vstates in virtual_states_probs:
                            prob_sum += virtual_states_probs[vstates]
                            if vstates == len(self.states)-2:
                                reward = 1
                            else:
                                reward = 0
                            print("transition", i, self.action_index_map[self.actions[a]], vstates, reward, virtual_states_probs[vstates])
                        # if prob_sum < 1:
                        #     print("Probs do not add up to 1")
                        # else:
                        #     print("Probs do add up")

                # Condition if B has strike
                else:
                    for a in range(len(self.actions)):
                        virtual_balls = balls_left - 1
                        balls_done = self.tot_balls - virtual_balls
                        virtual_states_probs = {}
                        for o,outcome in enumerate(self.outcomesB):
                            
                            virtual_runs = runs_left - outcome
                            prob = self.parametersB[o]

                            if outcome == -1:
                                # Game lost
                                state_jump_id = len(self.states)-1
                                reward = 0
                                if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob

                                print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                            
                            elif outcome == 0:
                                state_jump_id = (virtual_balls - 1)*self.runs + runs_left + self.strike_rot
                                if virtual_runs > 0 and virtual_balls <= 0:
                                    # Game lost (Balls finished)
                                    state_jump_id = len(self.states)-1
                                    reward = 0
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob

                                    print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                else:
                                    # Game continues
                                    #print(balls_done) 
                                    if virtual_balls%6 == 0:
                                        # Over. Strike changes (A gets strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id - self.strike_rot
                                        # print(f"vstate_id: {vstate_id}")
                                        # print(f"state_jump_id: {state_jump_id}")
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike Changes")

                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                    else:
                                        # Over. Strike doesnt change (B retains strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                            
                            else: # Outcome is 1
                                # print(f"virtual_runs: {virtual_runs}")
                                # print(f"virtual_balls: {virtual_balls}")
                                

                                if virtual_runs <= 0 and virtual_balls >= 0:
                                    # Game won
                                    state_jump_id = len(self.states)-2
                                    reward = 1
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                                    

                                    print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                                elif virtual_runs > 0 and virtual_balls <=0:
                                    # Game lost (Balls finished)
                                    state_jump_id = len(self.states)-1
                                    reward = 0
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob

                                    print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                                else:
                                    # Game continues
                                    if not virtual_balls%6 == 0:
                                        # Over. Strike changes (A gets strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = (vstate_id - self.strike_rot)%(len(self.states))
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike changed")
                                        
                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                    else:
                                        # Over. Strike doesnt change (B retains strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob
                                        
                                        print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")
                                        
                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                        for vstates in virtual_states_probs:
                                prob_sum += virtual_states_probs[vstates]
                                if vstates == len(self.states)-2:
                                    reward = 1
                                else:
                                    reward = 0
                                print("transition", i, self.action_index_map[self.actions[a]], vstates, reward, virtual_states_probs[vstates])                    

            print("mdptype", "episodic")
            print("discount", 1)
        else:
            for i,state in enumerate(self.states):
                if i == len(self.states)-1 or i == len(self.states)-2:
                    break
                # Determining the current situation
                curr_state = state
                if(curr_state == "lost" or curr_state == "won"):
                    continue
                else:
                    balls_left = int(curr_state[0:2])
                    runs_left = int(curr_state[2:4])

                # Condition if A has strike
                if i < self.strike_rot:

                    for a in range(len(self.actions)):
                        virtual_balls = balls_left - 1
                        balls_done = self.tot_balls - virtual_balls
                        virtual_states_probs = {}

                        for o,outcome in enumerate(self.outcomesA):
                            virtual_runs = runs_left - outcome
                            prob = float(self.parametersA[a][o])
                            
                            if outcome == -1 or (virtual_runs > 0 and virtual_balls == 0):
                                # Game lost
                                state_jump_id = len(self.states)-1

                                #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                if state_jump_id not in virtual_states_probs:
                                    virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob
                                
                            
                            elif virtual_runs <= 0 and virtual_balls >= 0:
                                # Game won
                                state_jump_id = len(self.states)-2

                                #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")
                                
                                if state_jump_id not in virtual_states_probs:
                                    virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob
                                

                            else:
                                #print("Game continues")
                                # Logical EXOR conditon between if its ball and whether even number of runs are scored and Game continues
                                vstate_id = i + self.tot_runs + outcome 
                                #   True                 
                                if (outcome%2 == 0) == (virtual_balls%6 == 0):
                                    # Change strike if odd runs are score and its not the last ball
                                    # Change strike if even runs are scored and it is the last ball
                                    #print(vstate_id, self.strike_rot, len(self.states)-2)
                                    state_jump_id = (vstate_id + self.strike_rot)%(len(self.states))

                                    #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike changed")
                                    
                                    if state_jump_id not in virtual_states_probs:
                                        virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                                    
                                else:
                                    # Dont change strike
                                    state_jump_id = vstate_id

                                    #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    if state_jump_id not in virtual_states_probs:
                                        virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                        prob_sum = 0
                        
                        for vstates in virtual_states_probs:
                            prob_sum += virtual_states_probs[vstates]
                            if vstates == len(self.states)-2:
                                reward = 1
                            else:
                                reward = 0
                            print("transition", i, self.action_index_map[self.actions[a]], vstates, reward, virtual_states_probs[vstates])
                        # if prob_sum < 1:
                        #     print("Probs do not add up to 1")
                        # else:
                        #     print("Probs do add up")

                # Condition if B has strike
                else:
                    for a in range(len(self.actions)):
                        virtual_balls = balls_left - 1
                        balls_done = self.tot_balls - virtual_balls
                        virtual_states_probs = {}
                        for o,outcome in enumerate(self.outcomesB):
                            
                            virtual_runs = runs_left - outcome
                            prob = self.parametersB[o]

                            if outcome == -1:
                                # Game lost
                                state_jump_id = len(self.states)-1
                                reward = 0
                                if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                else:
                                    virtual_states_probs[state_jump_id] += prob

                                #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                            
                            elif outcome == 0:
                                state_jump_id = (virtual_balls - 1)*self.runs + runs_left + self.strike_rot
                                if virtual_runs > 0 and virtual_balls <= 0:
                                    # Game lost (Balls finished)
                                    state_jump_id = len(self.states)-1
                                    reward = 0
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob

                                    #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                else:
                                    # Game continues
                                    #print(balls_done) 
                                    if virtual_balls%6 == 0:
                                        # Over. Strike changes (A gets strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id - self.strike_rot
                                        # print(f"vstate_id: {vstate_id}")
                                        # print(f"state_jump_id: {state_jump_id}")
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike Changes")

                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                    else:
                                        # Over. Strike doesnt change (B retains strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                            
                            else: # Outcome is 1
                                # print(f"virtual_runs: {virtual_runs}")
                                # print(f"virtual_balls: {virtual_balls}")
                                

                                if virtual_runs <= 0 and virtual_balls >= 0:
                                    # Game won
                                    state_jump_id = len(self.states)-2
                                    reward = 1
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob
                                    

                                    #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                                elif virtual_runs > 0 and virtual_balls <=0:
                                    # Game lost (Balls finished)
                                    state_jump_id = len(self.states)-1
                                    reward = 0
                                    if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                    else:
                                        virtual_states_probs[state_jump_id] += prob

                                    #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")

                                    #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)

                                else:
                                    # Game continues
                                    if not virtual_balls%6 == 0:
                                        # Over. Strike changes (A gets strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = (vstate_id - self.strike_rot)%(len(self.states))
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob

                                        #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}, Strike changed")
                                        
                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                                    else:
                                        # Over. Strike doesnt change (B retains strike)
                                        vstate_id = i + self.tot_runs + outcome
                                        state_jump_id = vstate_id
                                        reward = 0
                                        if state_jump_id not in virtual_states_probs:
                                            virtual_states_probs[state_jump_id] = prob
                                        else:
                                            virtual_states_probs[state_jump_id] += prob
                                        
                                        #print(f"state: {i, self.states[i]}, outcome: {outcome}, next_state: {state_jump_id, self.states[state_jump_id]}")
                                        
                                        #print("transition", i, self.action_index_map[a], state_jump_id, reward, prob)
                        for vstates in virtual_states_probs:
                                prob_sum += virtual_states_probs[vstates]
                                if vstates == len(self.states)-2:
                                    reward = 1
                                else:
                                    reward = 0
                                print("transition", i, self.action_index_map[self.actions[a]], vstates, reward, virtual_states_probs[vstates])                    

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
    #print(Cricket.states)
    # print(Cricket.parametersA)
    Cricket.determineMDPvalues()
    #print(Cricket.action_index_map[6])
    ## IDK what to do next???
    ## Mu me lo




    

    
