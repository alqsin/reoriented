import re

# Training
BATCH_SIZE = 256

# Dataset
FEN_COL = 'fen'
LABEL_COL = 'label'
DATA_DIR = 'data/train'
MODEL_DIR = 'data/saved_models'
DATA_RX = re.compile(r'\A[\w\(\)\-]+\.fen\Z')

# Data collection
SELECT_PROB = 0.07
EXP_SCALE = 0.99
SAMPLE_SIZE = int(1e6)
PGN_DIR = 'data/pgns'
PGN_RX = re.compile(r'\A\w+\.[pP][gG][nN]\Z')

# General
EMBED_SIZE = 13
INPUT_LENGTH = 64

piece_legend = {
  'P': 1,
  'p': 7,
  'B': 2,
  'b': 8,
  'N': 3,
  'n': 9,
  'R': 4,
  'r': 10,
  'Q': 5,
  'q': 11,
  'K': 6,
  'k': 12,
}
