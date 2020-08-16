import sys
import os
import datetime
import time
import tensorflow as tf

from environment.connect_4.environment import Environment
from environment.connect_4.episode_generator import EpisodeGenerator
from policy.q_epsilon_greedy import QEpsilonGreedyPolicy

iterations = int(sys.argv[1])
log_every = int(sys.argv[2])

MODEL_PATH = '/tmp/project/logs/model.h5'

if os.path.isfile(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print('Loaded model from ', MODEL_PATH)
else:
    model = tf.keras.Sequential([
      tf.keras.layers.Conv2D(
        filters=1,
        input_shape=(Environment.ROWS, Environment.COLUMNS, 3),
        kernel_size=3,
        padding='same',
        activation='relu'
      ),
      tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        strides=None,
        padding="valid"
      ),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(7, activation='tanh'),
    ])

    model.compile(
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
      loss='mean_squared_error',
      metrics=['accuracy']
    )

    print(MODEL_PATH, 'is not a file, creating new model')

def collect():
    agent_policy = QEpsilonGreedyPolicy(model, 0.1)
    generator = EpisodeGenerator(agent_policy, agent_policy)
    (agent_episode, adversary_episode) = generator.get()

    x = []
    y = []

    for episode in [agent_episode, adversary_episode]:
        final_reward = episode[-1][2]
        states = list(map(lambda sar : sar[0], episode))
        predictions = model.predict(tf.one_hot(states, dtype='float32', depth=3)).tolist()

        for index in range(len(episode) - 1):
            state = episode[index][0]
            action = episode[index][1]
            values = predictions[index]
            values[action] = final_reward

            x.append(state)
            y.append(values)

    return x, y

episode_summary_writer = tf.summary.create_file_writer(
    'logs/' + datetime.datetime.now().strftime("summary-%Y%m%d-%H%M%S")
)

for step in range(iterations):
    print(step, '/', iterations)
    x, y = collect()

    callbacks = []

    if step % log_every == 0:
        def on_epoch_end(_, logs):
            with episode_summary_writer.as_default():
                tf.summary.scalar('loss', logs.get('loss'), step=step + 1)
                tf.summary.scalar('accuracy', logs.get('accuracy'), step=step + 1)

        callbacks=[
          tf.keras.callbacks.LambdaCallback(on_epoch_end=on_epoch_end)
        ]

        model.save(MODEL_PATH)

    model.fit(
      x=tf.one_hot(x, dtype='float32', depth=3),
      y=tf.constant(y, shape=(len(y), Environment.COLUMNS)),
      callbacks=callbacks
    )

    #tf 2 leaks memory, try to update to 2.2 on release
    tf.keras.backend.clear_session()
