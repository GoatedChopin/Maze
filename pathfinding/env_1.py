"""
Try loading in a maze as a set of nodes where each node is a 4-tuple of boolean "walls". If the wall is present, it's True, else it's False. 
The env.state attribute should be a Matrix of m x n x 5 where each row-column pair represents a node's wall placement and whether or not it has been visited, 
although an m x n x 4 matrix might suffice with just the walls.

This might be achieved relatively easily using the maze_console.py file, since it uses nodes with something close to this structure.
Perhaps the step function can increase the node's 5th layer in the "state" attribute by 1 each time the agent visits, 
which will result in a state that represents how many times the agent has visited each node.

The reward might need to be -1 for visiting a new node, -2 for visiting a node previously visited, and +rows*columns points for solving the maze.
This way, the agent is rewarded for completing the maze in as few steps possible. 
The reward for completing a maze probably needs to be proportional to the amount of rows/columns that the maze has, otherwise the agent might end up thinking (erroneously)
that it's employing terrible strategy on big mazes (because of the relatively larger penalties in total steps) when in fact this is not the case.

*Perhaps incorporating the Cartesian distance from the end node to the current node into the reward function could yield better learning results.*
"""

import gym
class BasicEnv(gym.Env):
    def __init__(self):
            self.action_space = gym.spaces.Discrete(5)
            self.observation_space = gym.spaces.Discrete(2)
    def step(self, action):
            state = 1
        
            if action == 2:
                reward = 1
            else:
                reward = -1
                
            done = True
            info = {}
            return state, reward, done, info
    def reset(self):
            state = 0
            return state