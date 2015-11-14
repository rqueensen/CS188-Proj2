# policyIterationAgents.py
# ------------------------
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
import numpy as np

from learningAgents import ValueEstimationAgent

class PolicyIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PolicyIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs policy iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 20):
        """
          Your policy iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        states = self.mdp.getStates()
        # initialize policy arbitrarily
        self.policy = {}
        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                self.policy[state] = self.mdp.getPossibleActions(state)[0]
        # initialize policyValues dict
        self.policyValues = {}
        for state in states:
            self.policyValues[state] = 0

        for i in range(self.iterations):
            # step 1: call policy evaluation to get state values under policy, updating self.policyValues
            self.runPolicyEvaluation()
            # step 2: call policy improvement, which updates self.policy
            self.runPolicyImprovement()

    def runPolicyEvaluation(self):
        """ Run policy evaluation to get the state values under self.policy. Should update self.policyValues.
        Implement this by solving a linear system of equations using numpy. """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        #T and R
        transition = np.zeros((len(states),)*2)
        reward = np.zeros(len(self.mdp.getStates()))
        
        #build arbitrary order to handle unordered state dict
        order = {key: value for (key, value) in zip(states, range(len(states)))}
        
        for state in states:            
            if self.mdp.isTerminal(state):
                continue
            Qvalue = 0
            reward[order[state]] = self.mdp.getReward(state)
            for nextstate, probability in self.mdp.getTransitionStatesAndProbs(state, self.policy[state]):
                transition[order[state]][order[nextstate]] = probability
                
        A = np.eye(len(states)) - self.discount * transition
        X = np.linalg.solve(A, reward)
        
        for state in states: self.policyValues[state] = X[order[state]]
        

    def runPolicyImprovement(self):
        """ Run policy improvement using self.policyValues. Should update self.policy. """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        
        for state in states:
            self.policy[state] = None
            if self.mdp.isTerminal(state):
                continue
                
            eu_actions = {}
            for action in self.mdp.getPossibleActions(state):
                eu_actions[action] = self.computeQValueFromValues(state, action)
            if len(eu_actions) != 0:
                self.policy[state] = max(eu_actions, key=eu_actions.get)
            
                
            

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.policyValues.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for futureState, prob in statesAndProbs:
            value += prob * (self.mdp.getReward(state) + self.discount * self.policyValues[futureState])
            
        return value

    def getValue(self, state):
        return self.policyValues[state]

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getPolicy(self, state):
        return self.policy[state]

    def getAction(self, state):
        return self.policy[state]
