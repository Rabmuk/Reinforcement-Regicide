# import gymnasium as gym
import math
import random
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from regicideAI import RegicideGame_AI

LOAD_MODEL = True
num_episodes = 2_500
CYCLE_LIMIT = 5_000
MAX_MEM = 20_000

MODEL_NAME = 'model3'
MODEL_PKL_PATH = './' + MODEL_NAME + '_.pkl'
CYCLE_LIMIT_LOG_PATH = './' + MODEL_NAME + '_games_hit_cycle_lim.log'
FINAL_SCORE_LOG_PATH = './' + MODEL_NAME + '_final_scores.log'
FINAL_SCORE_CSV_PATH = './' + MODEL_NAME + '_final_scores.csv'

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the ``AdamW`` optimizer
BATCH_SIZE = 512
GAMMA = 0.9
EPS_START = 0.3
EPS_END = 0.0
EPS_DECAY = 20
TAU = 0.005
LR = 1e-4

# increase randomness to avoid deadlocks
# INVALID_BACKOFF_FACTOR = 1.01
INVALID_BACKOFF_STATIC = 2

# env = gym.make("CartPole-v1")
env = RegicideGame_AI()

# Get number of actions from gym action space
n_actions = env.action_space
# Get the number of state observations
state, info = env.reset()
n_observations = len(state)

episode_final_score = []

# if GPU is to be used
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer2_5 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer2_5(x))
        return self.layer3(x)


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

policy_net = DQN(n_observations, n_actions).to(device)
if LOAD_MODEL:
    try:
        policy_net.load_state_dict(torch.load(MODEL_PKL_PATH, weights_only=True))
        policy_net.eval()
    except FileNotFoundError as e:
        print('Model not loaded, file could not be found')

target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

def save_model_to_file():
    print('Saving Model')
    torch.save(policy_net.state_dict(), MODEL_PKL_PATH)

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(MAX_MEM)

steps_done = 0
    
def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(state).max(1).indices.view(1, 1)
    else:
        rand_index = random.randint(0,env.action_space-1)
        return torch.tensor([[rand_index]], device=device, dtype=torch.long)

def state_to_str(state)->str:
    state = state[0].int()
    labels = ['Deck','Discard','Enemies','Current E','E HP','E Att','is_p_turn','p_index']
    for player in env.players:
        labels.append(player.name + ' cc')
    for i in range(1,env.active_player.hand_limit+1):
        labels.append(f'card {i}')
    return_list = [
        f'{title}:{state[index]}'
        for index, title in enumerate(labels)
    ]

    return ', '.join(return_list)

def log_cycle_limit_game(state):
    global CYCLE_LIMIT_LOG_PATH
    info = state_to_str(state)
    with open(CYCLE_LIMIT_LOG_PATH, 'a') as file:
        file.write('\n\n')
        file.write(f'Abondoning episode because t limit reached. t = {t}')
        file.write('\n')
        file.write(str(state))
        file.write('\n')
        file.write(info)


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
                                    
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1).values
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1).values
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

for i_episode in range(1, num_episodes+1):
    print(f'Starting Episode #{i_episode}')

    # start of episode go for 0 randomness
    steps_done = EPS_DECAY

    # Initialize the environment and get its state
    state, info = env.reset()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    for t in count():
        if t % 500 == 0:
            print (f'Episode: {i_episode} Cycle {t}')

        if t > CYCLE_LIMIT:
            log_cycle_limit_game()
            break

        action = select_action(state)
        observation, reward, done, invalid_action = env.step(action)

        if invalid_action:
            # steps_done /= INVALID_BACKOFF_FACTOR
            steps_done -= INVALID_BACKOFF_STATIC
            steps_done = max(0,int(steps_done))
        
        reward = torch.tensor([reward], device=device)

        next_state = None
        if not done:
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)

        if done:
            print(f'Game #{i_episode} has ended')
            info = (env.game_result, len(env.enemies), env.steps_taken, env.invalid_steps_taken)
            episode_final_score.append(info )
            # print to CSV
            with open(FINAL_SCORE_CSV_PATH, 'a') as csv_file:
                csv_file.write('\n')
                csv_file.write(','.join(map(str,info)))
            break

    if i_episode > 1 and i_episode % 20 == 0:
        save_model_to_file()

print('Complete')
print(episode_final_score)
