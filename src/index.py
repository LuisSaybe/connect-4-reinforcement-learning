import tensorflow as tf

states = list(range(10))

policy_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(4, input_shape=(1,), activation='softmax'),
])
policy_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

with tf.Session() as sess:
    out = policy_model.predict(
        tf.constant([
            [1.0]
        ], dtype='float32'),
        steps=1
    )

    print(out)
