import chess.pgn
import random
import os

import constants as const
import fen_tools

def find_fens(game, probability):
  fen_list = []
  board = game.board()
  for (move_num, move) in enumerate(game.main_line()):
    board.push(move)
    if random.random() * pow(const.EXP_SCALE, move_num) < probability:
      fen_list.append(board.fen())
  return fen_list

def parse_and_write_fens(fens, file_out):
  file_out.write(const.FEN_COL + ',' + const.LABEL_COL + '\n')
  for fen in fens:
    curr_fen = fen_tools.trim_fen(fen)
    if random.random() > 0.5:
      curr_fen = fen_tools.flip_fen(curr_fen)
      curr_fen += ',1'
    else:
      curr_fen += ',0'
    file_out.write(curr_fen + '\n')

def get_filename_out(filename, file_num):
  filename_out = os.path.join(const.DATA_DIR, os.path.basename(filename))
  filename_out = filename_out.replace('.pgn', '({}).fen'.format(file_num))
  return filename_out

def try_read_game(pgnfile):
  while True:
    try:
      game = chess.pgn.read_game(pgnfile)
    except ValueError:
      continue
    except Exception:
      return None
    else:
      break
  return game

def traverse_pgn(filename, batch_size):
  fen_list = []
  with open(filename, 'r') as pgnfile:
    game = try_read_game(pgnfile)
    game_num = 1
    file_num = 0
    while game is not None:
      print("Doing game number {}".format(game_num), end='\r')
      fen_list += find_fens(game, const.SELECT_PROB)
      if len(fen_list) >= batch_size:
        print("\nWriting last {} FENs...".format(len(fen_list)))
        with open(get_filename_out(filename, file_num), 'w') as file_out:
          parse_and_write_fens(fen_list, file_out)
        file_num += 1
        fen_list = []
      game_num += 1
      game = try_read_game(pgnfile)
  print("\nWriting last {} FENs...".format(len(fen_list)))
  with open(get_filename_out(filename, file_num), 'w') as file_out:
    parse_and_write_fens(fen_list, file_out)

if __name__ == '__main__':
  processed = [f for f in os.listdir(const.DATA_DIR) if '.fen' in f.lower()]
  for filename in os.listdir(const.PGN_DIR):
    if filename.lower().endswith('.pgn'):
      if any([os.path.basename(filename).replace('.pgn','')
              in f for f in processed]):
        print("Skipping file {}...".format(filename))
        continue
      print("Doing file {}...".format(filename))
      traverse_pgn(
        os.path.join(const.PGN_DIR, filename),
        const.SAMPLE_SIZE,
      )
      print()