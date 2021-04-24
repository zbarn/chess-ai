import chess
import time
import random
from mts import mts

board = chess.Board()
PIECE_VALIES = {"PAWN" : 1, "KNIGHT" : 3, "BISHOP" : 3, "ROOK" : 5, "QUEEN" : 9}

def main():
  while board.is_checkmate() == False:
    playerMove()
    aiMove()

  printEndGame()

def playerMove():
  printPlayerInfo()
  uciMove = promptForLegalMove()
  board.push(chess.Move.from_uci(uciMove))
  time.sleep(1)
  print("\n\n\n")
  return

def aiMove():
  if (board.is_checkmate()):
    return

  printBotInfo()
  uciMove = findBotMove()
  board.push(uciMove)
  time.sleep(1)
  print("\n\n\n")
  return

def printPlayerInfo():
  print("======================================")
  print("PLAYER'S TURN")
  print("======================================")
  print("Current board:\n")
  print(board)
  print("\nPlease enter your move.")

def printBotInfo():
  print("======================================")
  print("BOT'S TURN")
  print("======================================")
  print("Current board:\n")
  print(board)
  print("\nThe bot will now makes its move.")

def promptForLegalMove():
  uciMove = input("Enter move: ")
  while (not chess.Move.from_uci(uciMove) in board.legal_moves):
    print("That move is illegal.")
    uciMove = input("Enter move: ")

  return uciMove

def findBotMove():
  move = mts(board).board.pop()
  return move

def printEndGame(board):
  if (not board.is_checkmate()):
    raise Exception("The game has not ended.")

  if (board.turn == chess.WHITE):
    winner = "BLACK"
  else:
    winner = "WHITE"

  print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
  print("End of game reached.")
  print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
  print(winner, "has won the game after", str(board.fullmove_number), "turns.")



main()
