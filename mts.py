from math import sqrt, log
from Node import Node
import chess
import time
import random
import multiprocessing
import pieceMaps
import evaluations
from itertools import product
from functools import partial

MAX_TIME = 240
VALUES = {chess.KING : 2000, chess.QUEEN : 1000, chess.ROOK: 500, chess.BISHOP : 300, chess.KNIGHT : 300, chess.PAWN : 100}

# Upper confidence bound equation of the node (selection policy)
def ucb1(n):
  if (n.plays == 0):
    return 0

  averageUtility = n.utility / n.plays
  c = sqrt(2)
  exploitationTerm = sqrt(log(n.parent.plays, 10) / n.plays)

  return averageUtility + (c * exploitationTerm)

# Leaf node finder
def select_and_expand(n, depth=0):
  print(n.plays)
  # Generate possible moves if not already done
  if (n.unexpandedMoves == None):
    n.unexpandedMoves = []
    moves = n.board.generate_legal_moves()

    for move in moves:
      n.unexpandedMoves.append(move)
    n.unexpandedMoves = evaluations.sortMoves(n.unexpandedMoves, n.board)

  # Explore unexplored nodes
  if (n.unexpandedMoves != []):
    newNode = Node(n.board.copy())
#    move = n.unexpandedMoves.pop(random.randint(0, len(n.unexpandedMoves)-1))
    move = evaluations.pickMove(n.unexpandedMoves, n.board)

    n.unexpandedMoves.remove(move)

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
    return select_and_expand(selectedNode, depth=depth+1)

# Game simulator
def simulate(n, startingSide):
  currBoard = n.board.copy()
  t = time.time()

  while (currBoard.legal_moves.count() != 0 and (not currBoard.is_insufficient_material()) and (time.time() - t < 1.5)):
    moveList = []
    for move in currBoard.legal_moves:
      moveList.append(move)

    moveList = evaluations.sortMoves(moveList, currBoard)
#    currBoard.push(moveList[random.randint(0, len(moveList)-1)])
    currBoard.push(evaluations.pickMove(moveList, currBoard))
#    currBoard.push(evaluations.pickBestMove(moveList, currBoard))

  if (currBoard.is_stalemate() or currBoard.is_insufficient_material()):
    return 0.03
  elif (currBoard.turn != startingSide):
    return 1
  else:
    return 0

def back_propagate(result, child):
  currNode = child

  while (currNode != None):
    currNode.utility += result
    currNode.plays += 1
    currNode = currNode.parent

# Picks 16 nodees that are to be expanded (for multithreading)
def getSelectionQueue(n, count=16):
  selectedQueue = []
  for i in range(0, count):
    newNode = select_and_expand(n)
    if (newNode == None):
      break
    else:
      selectedQueue.append(newNode)

  return selectedQueue

# Tree search algorithm to return a move given a board state
def mts(currBoard):
  t = time.time()
  side = currBoard.turn
  tree = Node(currBoard)
  counter = 0
  while(time.time() - t < MAX_TIME):
    queue = getSelectionQueue(tree)
    p = multiprocessing.Pool()
    startTime = time.time()
    results = p.map(partial(simulate, startingSide=side), queue)
    print(time.time() - startTime)
    p.close()
    for i in range(0, len(results)):
      counter += 1
      back_propagate(results[i], queue[i])

    print(counter)
#    child = select_and_expand(tree)
#    result = simulate(child, side)
#    back_propagate(result, child)

  currNode = tree.leafs[0]
  for i in range(1, len(tree.leafs)):
    if (tree.leafs[i].plays > currNode.plays):
      currNode = tree.leafs[i]

  print("MCTS Depth:", counter)

  return currNode
