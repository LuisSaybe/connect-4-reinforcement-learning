from src.environment.connect_4.environment import Environment

class EpisodeGenerator:
    def __init__(self, agent_policy, adversary_policy, agent_first):
        self.agent_policy = agent_policy
        self.adversary_policy = adversary_policy
        self.agent_first = agent_first

    def getMany(self, n):
        return [ self.get() for i in range(n) ]

    def get(self):
        environment = Environment()

        is_agents_turn = self.agent_first
        policy_index = 0
        episode = []

        while True:
            policy = self.agent_policy if is_agents_turn else self.adversary_policy
            player = Environment.AGENT if is_agents_turn else Environment.ADVERSARY

            available_actions = environment.getAvailableActions()
            state = environment.getState()

            if len(available_actions) == 0:
                if not is_agents_turn:
                    episode.append((state, None, 0))
                break

            action = policy.getAction(state, available_actions)

            (x, y) = environment.drop(action, player)

            if environment.connects(x, y, player):
                if is_agents_turn:
                    previous_state = episode[-1][0]
                    episode[-1] = (previous_state, action, 0)
                    episode.append((state, None, 1))
                else:
                    episode.append((state, None, -1))
                break
            elif is_agents_turn:
                if len(episode) == 0:
                    episode.append((state, action, None))
                else:
                    previous_state = episode[-1][0]
                    episode[-1] = (previous_state, action, 0)
            else:
                if len(episode) == 0:
                    episode.append((state, None, None))
                else:
                    episode.append((state, None, 0))

            is_agents_turn = not is_agents_turn

        return episode
