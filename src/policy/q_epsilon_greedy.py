import tensorflow as tf
import random
import numpy

class QEpsilonGreedyPolicy:
    def __init__(self, model, greedy_probability):
        self.model = model
        self.greedy_probability = greedy_probability

    def getAction(self, state, available_actions):
        random_action = numpy.random.choice([True, False], p=[self.greedy_probability, 1 - self.greedy_probability])

        if random_action:
            return random.choice(available_actions)

        state_tensor = tf.constant([ state ], dtype='float32', shape=(1, 6 * 7))
        values = self.model.predict(state_tensor).tolist()[0]

        indexes = range(len(values))
        available_indexes = list(filter(lambda i : i in available_actions, indexes))
        maximum_value = max(map(lambda i : values[i], available_indexes))
        maximum_indexes = list(filter(lambda i : values[i] == maximum_value, available_indexes))

        return random.choice(maximum_indexes)
