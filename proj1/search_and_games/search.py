# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """

    def DFS(problem, state, depth, current, prevDepth):
        if (problem.goalTest(state)):
            return []
        if (current >= depth):
            return None
        else:
            for action in problem.getActions(state):
                NewState = problem.getResult(state, action)
                if (NewState not in prevDepth or current + 1 <= prevDepth[NewState]):
                    prevDepth[NewState] = current + 1
                    result = DFS(problem, NewState, depth, current + 1, prevDepth)
                    if (type(result) is list):
                        return [action] + result
            return None
                    
    count = 1
    prevDepth = {}
    prevDepth[problem.getStartState()] = 0
    while(True):
        result = DFS(problem, problem.getStartState(), count, 0, prevDepth)
        if (result != None):
            return result
        count += 1
                    
                
    


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    #node = (state, f(n), preceding action, preceding action cost, parent)
    frontier = [(start, 0, [], 0, None)]
    visited = []
    finalNode = None
    while frontier:
        frontier = sorted(frontier, key=lambda x: x[1])
        node = frontier.pop(0)
        state = node[0]
        if state in visited:
            continue
        visited.append(state)
        if (problem.goalTest(state)):
            finalNode = node
            break
        for action in problem.getActions(state):
            NewState = problem.getResult(state, action)
            frontier += [(NewState, heuristic(NewState, problem) + node[3] + problem.getCost(state, action), [action], node[3] + problem.getCost(state, action), node)]
            
    path = []
    while finalNode:
        path += finalNode[2]
        finalNode = finalNode[4]
        
    return path[::-1]
        

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
