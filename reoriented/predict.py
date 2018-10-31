import argparse

import numpy as np
import tensorflow as tf
from tensorflow import keras

import fen_tools

def parse_args():
  parser = argparse.ArgumentParser(description = 'Parse prediction args.')
  parser.add_argument('--model', nargs='?', default=None,
                      help="Path to .hdf5 model")
  parser.add_argument('--fen', nargs='?', default=None,
                      help="FEN to predict")
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_args()

  model_path = args.model
  if model_path is None:
    raise ValueError("Must specify a model with --model")

  fen = args.fen
  if fen is None:
    raise ValueError("Must specify a FEN with --fen")
  
  # put fen into numpy array
  fen_arr = np.empty((1, 64), np.int8)
  fen_arr[0] = fen_tools.normalize_fen(fen_tools.trim_fen(fen))

  # load model and predict
  model = keras.models.load_model(model_path)
  prediction = model.predict(fen_arr, batch_size = 1)[0][0]

  if prediction >= 0.5:
    print("Board is inverted ({:.1%} confidence)".format(
      (prediction - 0.5) / 0.5
    ))
  else:
    print("Board is right-side up ({:.1%} confidence)".format(
      (0.5 - prediction) / 0.5
    ))
