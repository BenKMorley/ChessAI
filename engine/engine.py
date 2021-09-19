import tensorflow as tf
import numpy
from chessboard.chessboard import Chessboard
from chessboard.encoding.encoding import fen_to_chessboard

print("Starting engine.py")
OPT = 'qt'

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
game = Chessboard()
fen_to_chessboard(game, STARTING_FEN)
game.start()
binary_arrays = game.find_all_binary_arrays()
moves = game.moves_list
success_chance = []

input_shape = (14, 8, 8)

initializer = tf.keras.initializers.RandomNormal(mean=0., stddev=1.)

# Make a seperate model for white and black
classification_model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(numpy.product(list(input_shape)), activation='relu'),
    tf.keras.layers.Dense(400, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(128, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(16, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(3, initializer=initializer)
])

winning_model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(numpy.product(list(input_shape)), activation='relu'),
    tf.keras.layers.Dense(400, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(128, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(16, activation='relu', initializer=initializer),
    tf.keras.layers.Dense(1, activation='softmax', initializer=initializer)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

for i in range(len(moves)):
    x = winning_model.evaluate(binary_arrays[i])
    success_chance.append(x)


# model.fit(boards_in, prediction_out, epochs=10)

# Let's watch the untrained model in action
classification_model.evaluate(x_test, y_test)
winning_model.evaluate(x_test, y_test)
