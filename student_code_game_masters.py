from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peg1 = ()
        peg2 = ()
        peg3 = ()
        onStatement = Statement()
        onTerm1 = Term('?x')
        onTerm2 = Term('?y')
        onStatement.terms = (onTerm1, onTerm2)
        onStatement.predicate = 'on'
        for fact in self.kb.facts:
            if match(fact.statement, onStatement):
                if fact.statement.terms[0] == Term(Constant('disk1')):
                    disk = 1
                elif fact.statement.terms[0] == Term(Constant('disk2')):
                    disk = 2
                elif fact.statement.terms[0] == Term(Constant('disk3')):
                    disk = 3
                elif fact.statement.terms[0] == Term(Constant('disk4')):
                    disk = 4
                elif fact.statement.terms[0] == Term(Constant('disk5')):
                    disk = 5
                if fact.statement.terms[1] == Term(Constant('peg1')):
                    peg1 = peg1 + (disk,)
                elif fact.statement.terms[1] == Term(Constant('peg2')):
                    peg2 = peg2 + (disk,)
                elif fact.statement.terms[1] == Term(Constant('peg3')):
                    peg3 = peg3 + (disk,)

        peg1 = tuple(sorted(peg1))
        peg2 = tuple(sorted(peg2))
        peg3 = tuple(sorted(peg3))
        result = (peg1, peg2, peg3)
        return result
        ### student code goes here

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # ToGO:
  #      if not(self.isMovableLegal(movable_statement)):
  #          pass
        currDisk = movable_statement.terms[0]
        prevPeg = movable_statement.terms[1]
        newPeg = movable_statement.terms[2]

        # On next peg
        newOnStatement = Statement()
        newOnStatement.predicate = 'on'
        newOnStatement.terms = [currDisk, newPeg]
        newOnFact = Fact(newOnStatement)
        self.kb.kb_assert(newOnFact) #1

        #Not on previous peg
        removeOnStatement = Statement()
        removeOnStatement.predicate = 'on'
        removeOnStatement.terms = [currDisk, prevPeg]
        removeOnFact = Fact(removeOnStatement)
        self.kb.kb_retract(removeOnFact) #2


        #If Prev Empty Logic
        ONStatement = Statement()
        ONTerm1 = Term('?x')
        ONTerm2 = Term(prevPeg)
        ONStatement.terms = (ONTerm1, ONTerm2)
        ONStatement.predicate = 'on'
        ONFact = Fact(ONStatement)
        if not(self.kb.kb_ask(ONFact)):
            prevEmptyStatement = Statement()
            prevEmptyStatement.terms = [prevPeg]
            prevEmptyStatement.predicate = 'empty'
            prevEmptyFact = Fact(prevEmptyStatement)
            self.kb.kb_assert(prevEmptyFact) #3
        else:
        # previous disk now on top
        #           AND
        # Not above previous disk
            abovePrevStatement = Statement()
            aboveTerm = Term('?x')
            abovePrevStatement.terms = [currDisk, aboveTerm]
            abovePrevStatement.predicate = 'Above'
            for fact in self.kb.facts:
                if match(fact.statement, abovePrevStatement):
                    prevDisk = fact.statement.terms[1]
                    self.kb.kb_retract(fact) #7
                    break
            prevonTopStatement = Statement()
            prevonTopStatement.predicate = 'onTop'
            prevonTopStatement.terms = [prevDisk, prevPeg]
            prevonTopFact = Fact(prevonTopStatement)
            self.kb.kb_assert(prevonTopFact) #8

        # Above next disk
        # If next not empty
        nextEmptyBool = False
        nextEmptyStatement = Statement()
        nextEmptyStatement.terms = [newPeg]
        nextEmptyStatement.predicate = 'empty'
        for fact in self.kb.facts:
            if match(fact.statement, nextEmptyStatement):
                nextEmptyBool = True
                self.kb.kb_retract(fact) #9
                break

        if nextEmptyBool == False:
            nextOnTopStatement = Statement()
            nextOnTopStatement.predicate = 'onTop'
            onTopTerm1 = Term('?x')
            nextOnTopStatement.terms = [onTopTerm1, newPeg]
            nextOnTopFact = Fact(nextOnTopStatement)
            for fact in self.kb.facts:
                if match(fact.statement, nextOnTopStatement):
                    nextOnTop = fact.statement.terms[0]
                    aboveNextStatement = Statement()
                    aboveNextStatement.predicate = 'Above'
                    aboveNextStatement.terms = [currDisk, nextOnTop]
                    aboveNextFact = Fact(aboveNextStatement)
                    self.kb.kb_assert(aboveNextFact) #6
                    self.kb.kb_retract(nextOnTopFact)
                    break



        #On top of new peg
        newonTopStatement = Statement()
        newonTopStatement.predicate = 'onTop'
        newonTopStatement.terms = [currDisk, newPeg]
        newonTopFact = Fact(newonTopStatement)
        self.kb.kb_assert(newonTopFact) #4

        #Not on top of previous peg
        removeonTopStatement = Statement()
        removeonTopStatement.predicate = 'onTop'
        removeonTopStatement.terms = [currDisk, prevPeg]
        removeonTopFact = Fact(removeonTopStatement)
        self.kb.kb_retract(removeonTopFact) #5





        #Destination not empty

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1 = [0, 0, 0]
        row2 = [0, 0, 0]
        row3 = [0, 0, 0]
        tilePosStatement = Statement()
        posTerm1 = Term('?x')
        posTerm2 = Term('?y')
        posTerm3 = Term('?tile')
        tilePosStatement.terms = (posTerm1, posTerm2, posTerm3)
        tilePosStatement.predicate = 'tilePos'
        for fact in self.kb.facts:
            if match(fact.statement, tilePosStatement):
                if fact.statement.terms[2] == Term(Constant('tile1')):
                    term = 1
                if fact.statement.terms[2] == Term(Constant('tile2')):
                    term = 2
                if fact.statement.terms[2] == Term(Constant('tile3')):
                    term = 3
                if fact.statement.terms[2] == Term(Constant('tile4')):
                    term = 4
                if fact.statement.terms[2] == Term(Constant('tile5')):
                    term = 5
                if fact.statement.terms[2] == Term(Constant('tile6')):
                    term = 6
                if fact.statement.terms[2] == Term(Constant('tile7')):
                    term = 7
                if fact.statement.terms[2] == Term(Constant('tile8')):
                    term = 8
                if fact.statement.terms[2] == Term(Constant('empty')):
                    term = -1
                if fact.statement.terms[0] == Term(Constant('pos1')):
                    col = 0
                elif fact.statement.terms[0] == Term(Constant('pos2')):
                    col = 1
                elif fact.statement.terms[0] == Term(Constant('pos3')):
                    col = 2
                if fact.statement.terms[1] == Term(Constant('pos1')):
                    row1[col] = term

                elif fact.statement.terms[1] == Term(Constant('pos2')):
                    row2[col] = term

                elif fact.statement.terms[1] == Term(Constant('pos3')):
                    row3[col] = term

        row1 = tuple(row1)
        row2 = tuple(row2)
        row3 = tuple(row3)
        result = (row1, row2, row3)
        return result

        ### Student code goes here

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        newFactStatement1 = Statement()
        newFactStatement1.predicate = 'tilePos'
        newFactStatement1.terms = [movable_statement.terms[3], movable_statement.terms[4], movable_statement.terms[0]]
        newFact1 = Fact(newFactStatement1)
        newFactStatement2 = Statement()
        newFactStatement2.predicate = 'tilePos'
        newFactStatement2.terms = [movable_statement.terms[1], movable_statement.terms[2], Term(Constant('empty'))]
        newFact2 = Fact(newFactStatement2)
        removeFactStatement1 = Statement()
        removeFactStatement1.predicate = 'tilePos'
        removeFactStatement1.terms = [movable_statement.terms[1], movable_statement.terms[2], movable_statement.terms[0]]
        removeFact1 = Fact(removeFactStatement1)
        removeFactStatement2 = Statement()
        removeFactStatement2.predicate = 'tilePos'
        removeFactStatement2.terms = [movable_statement.terms[3], movable_statement.terms[4], Term(Constant('empty'))]
        removeFact2 = Fact(removeFactStatement2)
        self.kb.kb_assert(newFact1)
        self.kb.kb_assert(newFact2)
        self.kb.kb_retract(removeFact1)
        self.kb.kb_retract(removeFact2)

        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
