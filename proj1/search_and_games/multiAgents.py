# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print("successorGameState \n" + str(successorGameState))
        #print("newPos " + str(newPos))
        #print("newFood \n" + str(newFood))
        #print("newGhostStates " + str(newGhostStates))
        #print("newScaredTimes " + str(newScaredTimes))

        totalDistance = 0
        numFoods = 0;
        x = newFood.width
        y = newFood.height
        minDistance = -1
        for i in range(x):
            for j in range(y):
                if (newFood[i][j]):
                    #print("food location: (" + str(i) + ", " + str(j) + ").")
                    currentDistance = manhattanDistance([i, j], [newPos[0], newPos[1]])
                    if (minDistance == -1 or currentDistance < minDistance):
                       minDistance = currentDistance
                    totalDistance += manhattanDistance([i, j], [newPos[0], newPos[1]])
                    numFoods += 1
        if (numFoods != 0):
          foodAvg = float(totalDistance)/float(numFoods)
        else:
          foodAvg = totalDistance

        scaredAvg = 0
        for ghost in newScaredTimes:
          scaredAvg += ghost
        scaredAvg = float(scaredAvg) / float(len(newScaredTimes))

        ghostdist = 0;
        for state in newGhostStates:
          position = state.getPosition()
          ghostdist += manhattanDistance([position[0], position[1]], [newPos[0], newPos[1]])
        ghostdist = float(ghostdist) / float(len(newGhostStates))

        factors = [1 if foodAvg == 0 else 1/float(foodAvg), 1 if minDistance == 0 else 1/float(minDistance), ghostdist, scaredAvg, successorGameState.getScore()]
        weights = [800, 3, 1.5, .1, 1200]

        score = sum([float(i)*float(w) for i, w in zip(factors, weights)])
        #print factors
        #print ("score: " + str(score))
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #helper that decides whether or not to terminate
        def terminate(depth, state, agent):
          return depth == self.depth or state.isWin() or state.isLose() or len(getActions(state, agent)) == 0

        def maximize(state, depth, agent):
          if (terminate(depth, state, agent)):
            return (self.evaluationFunction(state), Directions.STOP)

          max_values = []
          for action in getActions(state, agent):
            minimum = minimize(state.generateSuccessor(agent, action), depth, 1)[0]
            max_values += [(minimum, action)]
          return max(max_values)

        def minimize(state, depth, agent):
          if (terminate(depth, state, agent)):
            return (self.evaluationFunction(state), Directions.STOP)

          next_minimax = maximize if agent == gameState.getNumAgents() - 1 else minimize
          min_values = []
          for action in getActions(state, agent):
            maximum = next_minimax(state.generateSuccessor(agent, action), depth + 1 if gameState.getNumAgents() - 1 == agent else depth, 0 if gameState.getNumAgents() - 1 == agent else agent + 1)[0]
            min_values += [(maximum, action)]

          return min(min_values)

        def getActions(state, agent):
          possible_actions = state.getLegalActions(agent)
          for action in possible_actions:
            if action == Directions.STOP:
              possible_actions.remove(action)
          return possible_actions

        return maximize(gameState, 0, 0)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #helper that decides whether or not to terminate
        def terminate(depth, state, agent):
          return depth == self.depth or state.isWin() or state.isLose() or len(getActions(state, agent)) == 0

        def maximize(state, depth, agent):
          if (terminate(depth, state, agent)):
            return (self.evaluationFunction(state), Directions.STOP)

          max_values = []
          for action in getActions(state, agent):
            minimum = minimize(state.generateSuccessor(agent, action), depth, 1)[0]
            max_values += [(minimum, action)]
          return max(max_values)

        def minimize(state, depth, agent):
          if (terminate(depth, state, agent)):
            return (self.evaluationFunction(state), Directions.STOP)
          actions = getActions(state, agent)
          next_minimax = maximize if agent == gameState.getNumAgents() - 1 else minimize
          avg_value = 0;
          for action in actions:
            maximum = next_minimax(state.generateSuccessor(agent, action), depth + 1 if gameState.getNumAgents() - 1 == agent else depth, 0 if gameState.getNumAgents() - 1 == agent else agent + 1)[0]
            avg_value += maximum

          #best = random.randint(0, len(min_values) - 1)
          return (float(avg_value)/float(len(actions)), actions[0])

        def getActions(state, agent):
          possible_actions = state.getLegalActions(agent)
          for action in possible_actions:
            if action == Directions.STOP:
              possible_actions.remove(action)
          return possible_actions

        return maximize(gameState, 0, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: We are using a linear combination of several calculations to find a 
      decent weighting of the calculations. A lot of guess and check for sure. For this, 
      it was sufficient for us to use our #6 solution and tweak it a bit. Interestingly, 
      adding the minDistance variable to the linear combination helps a ton, even though
      its weight is 3 (compared to a similar attribute, average distance, whose weight is
        1200). 
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #print("successorGameState \n" + str(successorGameState))
    #print("newPos " + str(newPos))
    #print("newFood \n" + str(newFood))
    #print("newGhostStates " + str(newGhostStates))
    #print("newScaredTimes " + str(newScaredTimes))

    totalDistance = 0
    numFoods = 0;
    x = newFood.width
    y = newFood.height
    minDistance = -1
    for i in range(x):
        for j in range(y):
            if (newFood[i][j]):
                #print("food location: (" + str(i) + ", " + str(j) + ").")
                currentDistance = manhattanDistance([i, j], [newPos[0], newPos[1]])
                if (minDistance == -1 or currentDistance < minDistance):
                   minDistance = currentDistance
                totalDistance += manhattanDistance([i, j], [newPos[0], newPos[1]])
                numFoods += 1
    if (numFoods != 0):
      foodAvg = float(totalDistance)/float(numFoods)
    else:
      foodAvg = totalDistance

    scaredAvg = 0
    for ghost in newScaredTimes:
      scaredAvg += ghost
    scaredAvg = float(scaredAvg) / float(len(newScaredTimes))

    ghostdist = 0;
    for state in newGhostStates:
      position = state.getPosition()
      ghostdist += manhattanDistance([position[0], position[1]], [newPos[0], newPos[1]])
    ghostdist = float(ghostdist) / float(len(newGhostStates))

    factors = [1 if foodAvg == 0 else 1/float(foodAvg), 1 if minDistance == 0 else 1/float(minDistance), ghostdist, scaredAvg, currentGameState.getScore()]
    weights = [700, 3, 1.4, .1, 1300]

    score = sum([float(i)*float(w) for i, w in zip(factors, weights)])
    #print factors
    #print ("score: " + str(score))
    return score

# Abbreviation
better = betterEvaluationFunction

