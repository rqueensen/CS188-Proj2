# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'


Expr = logic.Expr
PropSymbolExpr = logic.PropSymbolExpr

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    A, B, C = Expr("A"), Expr("B"), Expr("C")
    
    return logic.conjoin(A | B, ~A % (~B | C), logic.disjoin(~A, ~B, C))
    

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    A, B, C, D = Expr("A"), Expr("B"), Expr("C"), Expr("D")
    
    return logic.conjoin(C % (B|D), A >> (~B&~D), (~(B&~C)) >> A, (~D) >> C)

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    WumpusAlive = [PropSymbolExpr("WumpusAlive", 0), PropSymbolExpr("WumpusAlive", 1)]
    WumpusBorn = [PropSymbolExpr("WumpusBorn", 0)]
    WumpusKilled = [PropSymbolExpr("WumpusKilled", 0)]
    
    return logic.conjoin(WumpusAlive[1] % ((WumpusAlive[0] & ~WumpusKilled[0]) | (~WumpusAlive[0] & WumpusBorn[0])),
            ~(WumpusAlive[0] & WumpusBorn[0]), WumpusBorn[0])

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    return logic.pycoSAT(logic.to_cnf(sentence))
    
def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    expr_list = []
    
    for i in range(len(literals)):
        for j in range(len(literals)):
            if j > i:
                expr_list.append(~literals[i] | ~literals[j])
                
    return logic.conjoin(expr_list)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    expr_list = []
    expr_list.append(logic.disjoin(literals))
    
    for i in range(len(literals)):
        for j in range(len(literals)):
            if j > i:
                expr_list.append(~literals[i] | ~literals[j])
                
    return logic.conjoin(expr_list)
    
    
def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    plan = []
    times = []
    for key in model:
        name, indices = logic.PropSymbolExpr.parseExpr(key)
        if name in actions:
            times.append(int(indices))
            
    min_time = min(times)
    max_time = max(times)
    
    for i in range(min_time, max_time + 1):
        for key in model:
            name, indices = logic.PropSymbolExpr.parseExpr(key)
            if name in actions:
                if int(indices) == i and model[key]:
                    plan.append(name)
                    break
    return plan


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    expr_list = []
    if not walls_grid[x+1][y]:
        expr_list.append(PropSymbolExpr(pacman_str, x + 1, y, t-1) & PropSymbolExpr("West", t-1))
        
    if not walls_grid[x-1][y]:
        expr_list.append(PropSymbolExpr(pacman_str, x - 1, y, t-1) & PropSymbolExpr("East", t-1))
        
    if not walls_grid[x][y+1]:
        expr_list.append(PropSymbolExpr(pacman_str, x, y + 1, t-1) & PropSymbolExpr("South", t-1))
        
    if not walls_grid[x][y-1]:
        expr_list.append(PropSymbolExpr(pacman_str, x, y - 1, t-1) & PropSymbolExpr("North", t-1))
        
    if expr_list == []:
        return False
        
    pac_current = PropSymbolExpr(pacman_str, x, y, t)     
    return pac_current % logic.disjoin(expr_list)


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    init_x, init_y = problem.getStartState()
    goal_x, goal_y = problem.getGoalState()
    MAX_T = 51
    
    if (init_x, init_y) == (goal_x, goal_y):
        return []
    
    #Pacman must start at the initial position
    init_state_expr = PropSymbolExpr(pacman_str, init_x, init_y, 0)
    
    #Pacman can't be at multiple positions at once
    init_positions = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            init_positions.append(PropSymbolExpr(pacman_str, x, y, 0))
            
    pos_exclusion_expr = exactlyOne(init_positions)
    
    total_expr = [init_state_expr, pos_exclusion_expr]
    
    for t in range(1, MAX_T):
        #Pacman must be at the goal at time t
        goal_state_expr = PropSymbolExpr(pacman_str, goal_x, goal_y, t)
        
        #Pacman can't make more than one move per step
        possible_actions = [PropSymbolExpr("North", t-1), PropSymbolExpr("South", t-1), PropSymbolExpr("East", t-1), PropSymbolExpr("West", t-1)]
        action_exclusion_expr = exactlyOne(possible_actions) 
        
        #Each position has a corresponding successor
        successors = []
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                successor = pacmanSuccessorStateAxioms(x, y, t, walls)
                if successor != False:
                    successors.append(successor)
        
        successor_expr = logic.conjoin(successors)
        
        
        total_expr += [action_exclusion_expr, successor_expr]
        model_expr = logic.conjoin(total_expr + [goal_state_expr])
        model = findModel(model_expr)
        
        if model != False:
            path =  extractActionSequence(model, [game.Directions.NORTH, game.Directions.SOUTH,
                            game.Directions.EAST, game.Directions.WEST])
            return path
            
    return False


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]

    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    