# reoriented

This is a simple neural network implementation which takes arbitrary chess board positions and attempts to determine whether or not the board is shown from white's perspective or black's perspective. More specifically, when fed a [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation), the neural network predicts whether the board has the square `a1` in the bottom left (`0`) or top right (`1`). There is no correct classification for many positions, as pawns are the only pieces which are strictly oriented, meaning that the neural network must guess in many cases. Note that an "upside down" FEN simply has its position string reversed; `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR` represents the starting position, whereas `RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr` is the same position with the board flipped.

### Installing

This implementation is written in Python 3.6, and uses [tensorflow](https://github.com/tensorflow/tensorflow), [python-chess](https://github.com/niklasf/python-chess) (for PGN parsing) and numpy. For a simple installation, create and activate a virtual environment using `venv`, then `pip install requirements.txt`.

### Creating datasets

By default, `collect_fens.py` takes any `.pgn` files in `data/pgns/` and converts them into `.fen` files containing training data for the model, placing these files in `data/train/`. FENs are gathered by iterating through each PGN, deciding randomly whether or not to add each board position to the training set, inverting the board position with probability `0.5`, and saving the FEN as well as its status (1 for inverted, 0 for upright). The validity of a PGN is not checked, so it is possible for invalid positions or malformed FENs to be added if the input files are not clean.

For simple usage, run `python3 collect_fens.py` or the equivalent python 3.x execution command for your system, after creating the folders `data/pgns/` and `data/train/` and adding some PGNs to collect positions from. Input sources can be modified via `constants.py`.

See the [lichess game database](https://database.lichess.org/) for a source of many PGNs.

### Training

Assuming training files have been generated in the training data folder (specified in `constants.py`), `python3 model.py` will generate and train a model, saving the model in `.hdf5` format in `data/saved_models/` after each `.fen` (by default containing 1 million positions) has been fed for training. 90% of samples are used for training, and 10% are used for validation.

### Prediction

`predict.py` takes parameters `--model`, the path to the `.hdf5` trained model, and `--fen`, a chess FEN string. It outputs (to `stdout`) the model's prediction and certainty.

```
python3 predict.py --model data/saved_models/test_model.hdf5 --fen RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr
Board is inverted (100.0% confidence)
```

### Model details

Currently, the model consists of an embedding layer (to allow the different chess pieces to be learned), a flattening layer, several densely-connected layers of the same size as the flattened vector, and a sigmoid function to generate an "answer" between `0` and `1`. A variety of model configurations using a similar pattern have been tested, with many resulting in the model converging to `98.5-98.9` percent accuracy.

### TODO

* add data cleaning/validation tools
* add unit tests
* improve model configuration
* add persistent prediction with API
