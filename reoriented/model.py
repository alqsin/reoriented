import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

import fen_tools
import constants as const

def print_model_loss(curr_index, total_index, loss, acc, prev_loss, prev_acc,
                     train = True):
  if train:
    loss_str = 'Train: '
  else:
    loss_str = 'Validate: '
  new_loss = (loss * const.BATCH_SIZE + prev_loss *
    (curr_index - const.BATCH_SIZE)) / curr_index
  new_acc = (acc * const.BATCH_SIZE + prev_acc *
    (curr_index - const.BATCH_SIZE)) / curr_index
  loss_str += "{}/{} - loss: {:.4f} - acc: {:.4f}".format(
    curr_index,
    total_index,
    new_loss,
    new_acc
  )
  print(loss_str, end='\r')
  return new_loss, new_acc

def shuffle_arrays_together(a, b):
  """Shuffle two NumPy arrays using same indices."""
  assert len(a) == len(b)
  p = np.random.permutation(len(a))
  return a[p], b[p]

def import_data_fast(filename):
  """Does the same thing as import_data(), but does not use Pandas to read
  data. Should be faster, but is probably less stable and does not work if
  columns are permuted or if there are extra columns.
  """
  fens = np.empty((const.SAMPLE_SIZE, 64), np.int8)
  labels = np.empty(const.SAMPLE_SIZE, np.int8)
  with open(filename, 'r') as f:
    f.readline()  # skip first line
    for i, line in enumerate(f):
      if i >= const.SAMPLE_SIZE:
        break
      line_split = line.split(',')
      fens[i] = fen_tools.normalize_fen(line_split[0])
      labels[i] = (int(line_split[1]))
  
  if i < const.SAMPLE_SIZE - 1:
    print("File {} contained fewer than {} rows!".format(
                     filename, const.SAMPLE_SIZE))
    return None, None

  return shuffle_arrays_together(fens, labels)

def get_model():
  """Returns a model which can be trained on the data."""

  model = keras.Sequential()
  model.add(keras.layers.Embedding(
    const.EMBED_SIZE, 16,
    input_length = const.INPUT_LENGTH
  ))
  model.add(keras.layers.Flatten())
  model.add(keras.layers.Dense(
    1024,
    activation = 'relu'))
  model.add(keras.layers.Dense(
    1024,
    activation = 'relu'))
  model.add(keras.layers.Dense(
    1024,
    activation = 'relu'))
  model.add(keras.layers.Dense(1, activation = 'sigmoid'))

  model.compile(
    optimizer = keras.optimizers.Adam(lr = 0.001),
    loss = 'binary_crossentropy',
    metrics = ['accuracy'],
  )

  return model

def run_train_model(model, data_file):
  fens, labels = import_data_fast(data_file)
  if fens is None or labels is None:
    return

  NUM_VALIDATE = int(round(const.VALIDATION_FRAC * const.SAMPLE_SIZE))

  fen_val = fens[:NUM_VALIDATE]
  label_val = labels[:NUM_VALIDATE]
  fen_train = fens[NUM_VALIDATE:]
  label_train = labels[NUM_VALIDATE:]

  # train batchwise
  curr_pos = prev_loss = prev_acc = 0
  while curr_pos < const.SAMPLE_SIZE - NUM_VALIDATE:
    loss = model.train_on_batch(
      x = fen_train[curr_pos:curr_pos + const.BATCH_SIZE],
      y = label_train[curr_pos:curr_pos + const.BATCH_SIZE]
    )
    curr_pos += const.BATCH_SIZE
    if curr_pos > const.SAMPLE_SIZE - NUM_VALIDATE:
      curr_pos = const.SAMPLE_SIZE - NUM_VALIDATE

    prev_loss, prev_acc = print_model_loss(
      curr_pos, const.SAMPLE_SIZE - NUM_VALIDATE, loss[0], loss[1],
      prev_loss, prev_acc
    )
  print()  # adds newline so previous print_model_loss is visible

  # validate batchwise
  curr_pos = prev_loss = prev_acc = 0
  while curr_pos < NUM_VALIDATE:
    loss = model.test_on_batch(
      x = fen_val[curr_pos:curr_pos + const.BATCH_SIZE],
      y = label_val[curr_pos:curr_pos + const.BATCH_SIZE]
    )
    curr_pos += const.BATCH_SIZE
    if curr_pos > NUM_VALIDATE:
      curr_pos = NUM_VALIDATE

    prev_loss, prev_acc = print_model_loss(
      curr_pos, NUM_VALIDATE, loss[0], loss[1],
      prev_loss, prev_acc, train = False
    )
  print()  # adds newline so previous print_model_loss is visible

if __name__ == '__main__':
  model = get_model()
  model.summary()

  data_files = [os.path.join(const.DATA_DIR, f) for
                f in os.listdir(const.DATA_DIR) if
                const.DATA_RX.match(f) is not None]

  # determine file save name
  # need to fix this - only checks if '0' model is saved
  model_files = os.listdir(const.MODEL_DIR)
  save_filename = 'model-{}-train-{}.hdf5'
  save_model_num = 0
  while save_filename.format(save_model_num, 0) in model_files:
    save_model_num += 1
  save_filename = save_filename.format(save_model_num, '{}')

  train_num = 0
  for _ in range(5):
    for data_file in data_files:
      run_train_model(model, data_file)
      keras.models.save_model(
        model,
        os.path.join(const.MODEL_DIR, save_filename.format(train_num))
      )
      train_num += 1
