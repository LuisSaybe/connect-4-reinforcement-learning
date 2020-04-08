import tensorflow as tf
import random

class QEpsilonGreedyPolicy:
    def __init__(self, model, greedy_probability):
        self.model = model
        self.greedy_probability = greedy_probability

    def getAction(self, state, available_actions):
        random_action = random.choices([True, False], [self.greedy_probability, 1 - self.greedy_probability])[0]

        if random_action:
            return random.choice(available_actions)

        state_tensor = tf.one_hot([state], dtype='float32', depth=3)
        prediction = self.model.predict(state_tensor)
        values = prediction.tolist()[0]

        maximum_action_value = max(map(lambda i : values[i], available_actions))
        maximum_indexes = list(filter(lambda i : values[i] == maximum_action_value, available_actions))

        if len(maximum_indexes) == 0:
            print('state', state)
            print('available_actions', available_actions)
            print('values', values)
            print('maximum_action_value', maximum_action_value)
            print('maximum_indexes', maximum_indexes)
            raise

        return random.choice(maximum_indexes)
