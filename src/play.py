import tensorflow as tf

from policy.q_epsilon_greedy import QEpsilonGreedyPolicy
from environment.connect_4.environment import Environment

model = tf.keras.models.load_model('/tmp/project/logs/model.h5')
agent = QEpsilonGreedyPolicy(model, 0)
environment = Environment()
response = None

while response != 'y' and response != 'n':
    response = input('Do you want to go first? y/n\n')

player = Environment.ADVERSARY if response == 'y' else Environment.AGENT

while True:
    available_actions = environment.getAvailableActions()

    if len(available_actions) == 0:
        print('Tie\n')
        break

    if player == Environment.AGENT:
        state = environment.getState()
        action = agent.getAction(state, available_actions)
    else:
        action = None

        while action not in available_actions:
            try:
                action = int(input('Choose a move: 1 - 7\n'))
            except:
                action = None
            else:
                action -= 1

    (x, y) = environment.drop(action, player)

    print(environment, '\n\n')

    if environment.connects(x, y, player):
        winner = 'Agent' if player == Environment.AGENT else 'You'
        print(winner, 'wins\n')
        break

    player = Environment.ADVERSARY if player == Environment.AGENT else Environment.AGENT
