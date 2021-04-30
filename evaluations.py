import chess
from math import sqrt, log
import pieceMaps
import random

VALUES = {chess.KING : 10.0 , chess.QUEEN : 9.0, chess.ROOK: 5.0, chess.BISHOP : 3.0, chess.KNIGHT : 3.0, chess.PAWN : 1.0}

# Total evaluation of a move
def moveValue(move, board):
  return positionValue(move, board) + captureValue(move, board) + developValue(move, board)

# Evaluated destination square position
def positionValue(move, board, toSquare=None):
  movingPiece = board.piece_type_at(move.from_square)

  desiredMap = None

  if (movingPiece == chess.KING):
    desiredMap = pieceMaps.kingMap
  elif (movingPiece == chess.QUEEN):
    desiredMap = pieceMaps.queenMap
  elif (movingPiece == chess.ROOK):
    desiredMap = pieceMaps.rookMap
  elif (movingPiece == chess.BISHOP):
    desiredMap = pieceMaps.bishopMap
  elif (movingPiece == chess.KNIGHT):
    desiredMap = pieceMaps.knightMap
  elif (movingPiece == chess.PAWN):
    desiredMap = pieceMaps.pawnMap

  if (toSquare == None):
    toSquare = move.to_square
    if (board.turn == chess.BLACK):
      toSquare = 63 - toSquare

  return desiredMap[toSquare]

# Evaluate any capture moves
def captureValue(move, board):
  if (board.is_capture(move)):
    opponentPiece = board.piece_type_at(move.to_square)
    myPiece = board.piece_type_at(move.from_square)

    # En passant edge case
    if (opponentPiece == None):
      return VALUES[chess.PAWN] - VALUES[myPiece]
    else:
      return VALUES[opponentPiece] - VALUES[myPiece]
  else:
    return 0

# Returns positive or negative number based on how more developed position is
def developValue(move, board):
  currPosValue = positionValue(move, board, toSquare=move.from_square)
  nextPosValue = positionValue(move, board)

  # Scale return based on percentage gain of move
  delta = abs(currPosValue - nextPosValue)

  relativeDifference = delta / currPosValue

  # 33% cutoff point
  developingValue = (relativeDifference - 0.55) * (5/3)

  return developingValue

# Sorts a move list
def sortMoves(moveList, board):
  return sorted(moveList, key=lambda x : moveValue(x, board))

# Picks the highest value move
def pickBestMove(moveList, board):
  currBestMove = moveList[0]
  for i in range(1, len(moveList)):
    if moveValue(moveList[i], board) > moveValue(currBestMove, board):
      currBestMove = moveList[i]

  return currBestMove

# Picks a move in the list based on a normal distribution
def pickMove(moveList, board):
  moveIndex = random.gauss(0, len(moveList)/2)
  moveIndex = round(abs(moveIndex))

  if (moveIndex > len(moveList) - 1):
    moveIndex = len(moveList) - 1

  # Skip en passant moves
  #if (board.is_en_passant(moveList[moveIndex])):
  #  return pickMove(moveList, board)
  #else:
  return moveList[moveIndex]
