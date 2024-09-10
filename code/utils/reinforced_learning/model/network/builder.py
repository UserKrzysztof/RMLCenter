from collections import deque, namedtuple
import random
import torch 
import torch.nn as nn
import torch.optim as optim

import sys, inspect
import re

class NetworkBuilder():
    def __init__(self) -> None:
        super().__init__()
        non_linear_weighted = ".*(LU)|(Hardshrink)|(Hardsigmoid)|(Hardtanh)|(Hardswish)|(Logsigmoid)|(Multiheadattention)|(Mish)|(Softplus)|(Softshrink)|(Softsign)|(Tanh)|(Tanhshrink)|(Threshold).*"
        non_linear_other = ".*(Softmin)|(Softmax)|(Softmax2d)|(LogSoftmax)|(AdaptiveLogSoftmaxWithLoss).*"
        vision = ".*(PixelShuffle)|(PixelUnshuffle)|(Upsample)|(UpsamplingNearest2d)|(UpsamplingBilinear2d).*"
        self.LAYERS_GROUPS = {
            ".*(Conv)|((F|f)old).*": "Convolution Layers",
            ".*Pool.*": "Pooling Layers",
            ".*Pad.*": "Padding Layers",
            non_linear_weighted : "Non-linear Activations (weighted sum, nonlinearity)",
            non_linear_other: "Non-linear Activations (other)",
            ".*Norm.*": "Normalization Layers",
            ".*(RNN)|(LSTM)|(GRU).*": "Recurrent Layers",
            ".*Transformer.*": "Transformer Layers",
            ".*((L|l)inear)|(Identity).*": "Linear Layers",
            ".*Dropout.*": "Dropout Layers",
            ".*Embedding.*": "Sparse Layers",
            vision: "Vision Layers",
            ".*ChannelShuffle.*": "Shuffle Layers",
            ".*(P|p)arallel.*": "DataParallel Layers (multi-GPU, distributed)"
        }
        self.layers = self._get_layers_groups()
        self.policy_network = None
        self.target_network = None
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else
            "mps" if torch.backends.mps.is_available() else
            "cpu"
        )
        self.replay_memory = None
        self.optimizer = None
        self.BATCH_SIZE = None
        self.GAMMA = None
        self.EPS_START = None
        self.EPS_END = None
        self.TAU = None
        self.number_of_episdes = None

        
    def _get_layers_groups(self) -> list[tuple[str, list[str]]]:
        groups = []
        elements = get_available_elements()
        for group in self.LAYERS_GROUPS:
            if any(char.isdigit() for char in group):
                   continue
            group_id = re.compile(group)
            layers = list(filter(group_id.match, elements))
            groups.append((self.LAYERS_GROUPS[group], layers))

        return groups
    
    def get_layers(self):
        return self.layers
    
    def build(self, layers):
        layers = [getattr(nn, layer_name)(*params) for (layer_name, params) in layers]
        self.policy_network = nn.Sequential(*layers).to(device=self.device)
        self.target_network = nn.Sequential(*layers).to(device=self.device)
        self.target_network.load_state_dict(self.policy_network.state_dict())

    def set_replay_memory(self, capacity):
        self.replay_memory = ReplayMemory(capacity)

    def set_optimizer(self, lr, amsgrad):
        self.optimizer = optim.AdamW(self.policy_network.parameters(), lr=lr, amsgrad=amsgrad)

    def set_episode(self, BATCH_SIZE, GAMMA, EPS_START, EPS_END, EPS_DECAY, TAU, number_of_episodes):
        self.BATCH_SIZE = BATCH_SIZE
        self.GAMMA = GAMMA
        self.EPS_START = EPS_START
        self.EPS_DECAY = EPS_DECAY
        self.EPS_END = EPS_END
        self.TAU = TAU
        self.number_of_episdes = number_of_episodes


def get_available_elements():
    elements = inspect.getmembers(nn, inspect.isclass)
    for i, e in enumerate(elements):
        elements[i] = e[0]
    return elements

def get_params_for_layer_name(layer_name:str):
    return dict(inspect.signature(getattr(nn, layer_name)).parameters)


def get_options():
    options = {
        "NUMBER_OF_EPISODES": ("number of opisodes", int, 50),
        "REPLAY_MEMORY_CAPACITY": ("replay memory capacity", int, 10000),
        "BATCH_SIZE": ("batch size", int, 128),
        "GAMMA": ("discount factor for future rewards", float, 0.99),
        "EPS_START": ("starting value of epsilon for epsilon-greedy exploration", float, 0.9),
        "EPS_END": ("minimum value of epsilon", float, 0.05),
        "EPS_DECAY": ("decay rate of epsilon", int, 1000),
        "TAU": ("soft update rate for target network", float, 0.005),
        "LR": ("learning rate for the optimizer", float, 1e-4)
        }

    signature_dict = {
        key: inspect.Parameter(
            name=key,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=value[2],
            annotation=value[1]
        )
        for key, value in options.items()
    }
    return signature_dict, options



Transition = namedtuple('Transition', ('state', 'action', 'next_state','reward'))
class ReplayMemory(object):
    def __init__(self, capacity) -> None:
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save transition"""
        self.memory.append(Transition(*args))

    def sample(self,batch_size):
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)
    

