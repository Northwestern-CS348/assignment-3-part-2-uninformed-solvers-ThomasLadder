
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        print(self.currentState.state)
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            if self.currentState.children == []:
                movables = self.gm.getMovables()
                # getting children
                for movable in movables:
                    self.gm.makeMove(movable)
                    new_child = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
                    self.currentState.children.append(new_child)
                    new_child.parent = self.currentState
                    self.gm.reverseMove(movable)

            # while len(self.currentState.children) > self.currentState.nextChildToVisit:
            if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                self.currentState.nextChildToVisit += 1
                while len(self.currentState.children) > self.currentState.nextChildToVisit:
                    self.visited[self.currentState.children[self.currentState.nextChildToVisit]] = True
                    self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
                    self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
         #   else:
    #        if len(self.currentState.children) == self.currentState.nextChildToVisit:
          #      self.gm.reverseMove(self.currentState.requiredMovable)
           #     self.currentState = self.currentState.parent

     #                   self.gm.reverseMove(movables[self.currentState.nextChildToVisit]) #check why out of range
    #
            #^^^ mm doubly confused about this
                ##^^Why does this happen


            #currentState - is a gameState object
            #gameState
            #new game state when you go into the next
            #Each node is a gameState object

            #To do visited, set that one equal to true

            #for loop to generate all of the childen, and then visit the first one
            #What knowlege base actually has in it
            #Each move, make that move, check if this is a move we've visited, if not in self.visited,
            #Set this to the children, and set the upper one as the parent of that
            #

            #cState.requiredMovable = movables[0]

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        return True
