# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
import time
import Queue

class AsynchronousValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.counter = 0
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = collections.defaultdict(float)
        states = self.mdp.getStates()
        for state in states:
            self.values[state] = 0

            
        def getState(states):
            state = states[self.counter]
            self.counter += 1
            if self.counter == len(states):
                self.counter = 0
            return state
        
        for i in range(iterations):
            state = getState(states)
            
            if mdp.isTerminal(state):
                continue
               
            bestValue = -100000
            for action in mdp.getPossibleActions(state):
                q_value = self.computeQValueFromValues(state, action)
                if q_value > bestValue:
                    bestValue = q_value
            
            self.values[state] = bestValue

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        value = 0
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for futureState, prob in statesAndProbs:
            value += prob * (self.mdp.getReward(state) + self.discount * self.values[futureState])
            
        return value
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None
            
        bestValue = -100000
        for action in self.mdp.getPossibleActions(state):
            q_value = self.computeQValueFromValues(state, action)
            if q_value > bestValue:
                bestValue = q_value
                bestAction = action
                
        return bestAction
        
    def bestQ(self, state):
        values = []
        for action in self.mdp.getPossibleActions(state):
            q_value = self.computeQValueFromValues(state, action)
            values.append(q_value)
        return max(values)
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = collections.defaultdict(float)
        states = self.mdp.getStates()
        
        predecessors = {}
        for state in states:
            self.values[state] = 0
            predecessors[state] = []

        
        
        for state in states:
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for futureState, prob in statesAndProbs:
                        if prob != 0 and state not in predecessors[futureState]:
                            predecessors[futureState].append(state)

        Q = Queue.PriorityQueue()
        
        for s in states:
            if not self.mdp.isTerminal(s):
                diff = abs(self.values[s] - self.bestQ(s))
                Q.put((-diff, s))
                
        for i in range(self.iterations):
            if Q.empty():
                return
            prior, s = Q.get()
            
            if not self.mdp.isTerminal(s):
                self.values[s] = self.bestQ(s)
                
            for p in predecessors[s]:
                diff = abs(self.values[p] - self.bestQ(p))
                
                update = False
                if diff > theta:
                    update = True
                    for x in predecessors:
                        if p == x[1]:
                            if x[0] <= -diff:
                                update = False
                                break
                if update:
                    Q.put((-diff, p))
                    
                
                        
                            
                
                
                
                
                
                
                
                
