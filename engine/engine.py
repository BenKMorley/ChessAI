import tensorflow as tf


# Make a seperate model for white and black
model_white = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(14, 8, 8)),
    tf.keras.layers.Dense(896, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model_black = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(14, 8, 8)),
    tf.keras.layers.Dense(896, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model_white.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

# Let's watch the untrained model in action


model_white.evaluate(x_test, y_test)
