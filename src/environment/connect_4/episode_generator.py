import random

from environment.connect_4.environment import Environment

class EpisodeGenerator:
    def __init__(self, policy_a, policy_b):
        self.policy_a = policy_a
        self.policy_b = policy_b

    def get(self, current_agent_is_a = random.choice([True, False])):
        environment_a = Environment()
        environment_b = Environment()
        a_sars = [(None, None, None)]
        b_sars = [(None, None, None)]

        while True:
            if current_agent_is_a:
                agent = self.policy_a
                agent_environment = environment_a
                adversary_environment = environment_b
                agent_sars = a_sars
                adversary_sars = b_sars
            else:
                agent = self.policy_b
                agent_environment = environment_b
                adversary_environment = environment_a
                agent_sars = b_sars
                adversary_sars = a_sars

            available_actions = agent_environment.getAvailableActions()
            state = agent_environment.getState()

            if len(available_actions) == 0:
                agent_sars[-1] = (state, 0, Environment.DEFAULT_REWARD)
                adversary_sars[-1] = (adversary_environment.getState(), None, Environment.DEFAULT_REWARD)
                break

            action = agent.getAction(state, available_actions)

            agent_sars[-1] = (state, action, agent_sars[-1][2])

            (x, y) = agent_environment.drop(action, Environment.AGENT)
            adversary_environment.drop(action, Environment.ADVERSARY)

            if agent_environment.connects(x, y, Environment.AGENT):
                agent_sars.append((agent_environment.getState(), None, Environment.WIN_REWARD))
                adversary_sars[-1] = (adversary_environment.getState(), None, Environment.LOSE_REWARD)
                break

            agent_sars.append((None, None, Environment.DEFAULT_REWARD))
            current_agent_is_a = not current_agent_is_a

        return (a_sars, b_sars)
