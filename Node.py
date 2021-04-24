class Node:

  def __init__(self, board):
    self.board = board
    self.utility = 0
    self.plays = 0
    self.parent = None
    self.leafs = []
    self.unexpandedMoves = None
