import re
import random

import constants as const

pieces_pattern = r'[rnbqkpRNBQKP1-8]+'
board_pattern = (pieces_pattern + '/') * 7 + pieces_pattern
board_rx = re.compile(board_pattern)
board_only_rx = re.compile(r'\A' + board_pattern + r'\Z')

def is_int(x):
  try:
    int(x)
  except ValueError:
    return False
  return True

def normalize_fen(fen):
  """Normalizes board representation of FEN by printing each piece as an
  integer, with each empty square as a 0. Returns a list of integers.
  """
  result = []
  for char in fen:
    if char in const.piece_legend:
      result.append(const.piece_legend[char])
    elif is_int(char):
      for _ in range(int(char)):
        result.append(0)
    elif char == '/':
      continue
    else:
      raise ValueError("Not a valid character!")
  return result

def trim_fen(fen):
  """Returns the board representation section of a FEN."""
  result = board_rx.match(fen)
  if result is None:
    raise ValueError("The following FEN does not appear to be valid:\n"
                     "{}".format(fen))
  return result.group(0)

def flip_fen(board_fen):
  """Flips a FEN so that the pieces are facing the opposite direction.
  FEN must contain board representation and no other fields.
  """
  if board_only_rx.match(board_fen) is None:
    raise ValueError("The following FEN is not properly formatted:\n"
                     "{}".format(board_fen))
  return board_fen[::-1]

# def process_fens(fens):
#   """Trims every FEN in fens, randomly flipping some, then appending a
#   (comma-separated) 0 to un-flipped FENs and a 1 to flipped FENs. Returns all
#   FENs as a list.
#   """
#   curr_row = 1
#   result_list = []
#   for fen in fens:
#     print("Doing row {}".format(curr_row), end='\r')
#     curr_row += 1
#     curr_fen = trim_fen(fen)
#     if random.random() > 0.5:
#       curr_fen = flip_fen(curr_fen)
#       curr_fen += ',1'
#     else:
#       curr_fen += ',0'
#     result_list.append(curr_fen)
#   print()
#   return result_list

# if __name__ == '__main__':
#   filename = 'data/lichess_2014_01.fen'
#   filename_out = filename.replace('.fen', '_mixed.csv')
#   with open(filename, 'r') as fen_file:
#     fen_list = process_fens(fen_file)
  
#   with open(filename_out, 'w') as fen_file_out:
#     curr_row = 1
#     fen_file_out.write(const.FEN_COL + ',' + const.LABEL_COL + '\n')
#     for fen in fen_list:
#       print('Writing row {}'.format(curr_row), end='\r')
#       fen_file_out.write(fen + '\n')
#       curr_row += 1
#     print()