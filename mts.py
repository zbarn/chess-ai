from math import sqrt, log
from Node import Node
import chess
import time
import random

# Upper confidence bound equation of the node (selection policy)
def ucb1(n):
  averageUtility = n.utility / n.plays
  c = sqrt(2)
  exploitationTerm = sqrt(log(n.parent.plays, 10) / n.plays)

  return averageUtility + (c * exploitationTerm)

# Leaf node finder
def select_and_expand(n):
  # Generate possible moves if not already done
  if (n.unexpandedMoves == None):
    n.unexpandedMoves = []
    moves = n.board.generate_legal_moves()

    for move in moves:
      n.unexpandedMoves.append(move)

  # Explore unexplored nodes
  if (n.unexpandedMoves != []):
    newNode = Node(n.board.copy())
    move = n.unexpandedMoves.pop(random.randint(0, len(n.unexpandedMoves)-1))
    newNode.board.push(move)
    newNode.parent = n
    n.leafs.append(newNode)
    return newNode
  # Resursively call select
  else:
    selectedNode = n.leafs[0]
    for i in range(1, len(n.leafs)):
      if (ucb1(n.leafs[i]) > ucb1(selectedNode)):
        selectedNode = n.leafs[i]
    return select_and_expand(selectedNode)

# Game simulator
def simulate(n, startingSide):
  currBoard = n.board.copy()

  while (currBoard.legal_moves.count() != 0 and (not currBoard.is_insufficient_material())):
    moveList = []
    for move in currBoard.legal_moves:
      moveList.append(move)
    currBoard.push(moveList[random.randint(0, len(moveList)-1)])

  if (currBoard.is_stalemate() or currBoard.is_insufficient_material()):
    print("DRAW")
    return 0.5
  elif (currBoard.turn != startingSide):
    print("WIN")
    return 1
  else:
    print("LOSE")
    return 0

def back_propagate(result, child):
  currNode = child

  while (currNode != None):
    currNode.utility += result
    currNode.plays += 1
    currNode = currNode.parent

# Tree search algorithm to return a move given a board state
def mts(currBoard):
  side = currBoard.turn

  tree = Node(currBoard)

  for i in range(0, 1000):
    child = select_and_expand(tree)
    result = simulate(child, side)
    back_propagate(result, child)

  currNode = tree.leafs[0]
  for i in range(1, len(tree.leafs)):
    if (tree.leafs[i].plays > currNode.plays):
      currNode = tree.leafs[i]

  return currNode
