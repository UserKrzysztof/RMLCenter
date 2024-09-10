from itertools import count
import math
import random

import torch
import torch.nn as nn
from utils.reinforced_learning.model.enviroment.builder import EnvBuilder
from utils.reinforced_learning.model.network.builder import NetworkBuilder, Transition
from utils.reinforced_learning.plotters.movies import update_episode_recap
from utils.reinforced_learning.plotters.rewards import RewardPlotUpdater


class Model():
    def __init__(self, env_builer: EnvBuilder, network_builder: NetworkBuilder, plotter: RewardPlotUpdater) -> None:
        self.device = network_builder.device

        self.env = env_builer.env
        self.n_actions = self.env.action_space.n
        self.state, self.info = self.env.reset()
        self.n_observations = len(self.state)

        self.number_of_episodes = network_builder.number_of_episdes

        self.policy_net = network_builder.policy_network
        self.target_net = network_builder.target_network
        self.optimizer = network_builder.optimizer
        self.replay_memory = network_builder.replay_memory

        self.BATCH_SIZE = network_builder.BATCH_SIZE
        self.GAMMA = network_builder.GAMMA
        self.EPS_DECAY = network_builder.EPS_DECAY
        self.EPS_START = network_builder.EPS_START
        self.EPS_END = network_builder.EPS_END
        self.TAU = network_builder.TAU

        self.steps_done = 0
        self.episode_rewards = []

        self.plotter = plotter
        self.max_episode_recap_lenght = 1000

    def _select_action(self, state):
        sample = random.random()
        eps_threshold = self.EPS_END + (self.EPS_START - self.EPS_END) * \
            math.exp(-1. * self.steps_done / self.EPS_DECAY)
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                return self.policy_net(state).max(1).indices.view(1, 1)
        else:
            return torch.tensor([[self.env.action_space.sample()]], device=self.device, dtype=torch.long)
        
    def _optimize_model(self):
        if len(self.replay_memory) < self.BATCH_SIZE:
            return
        transitions = self.replay_memory.sample(self.BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)),
                                    device= self.device,
                                    dtype=torch.bool)
        
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(self.BATCH_SIZE, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1).values
        expected_state_action_values = (next_state_values * self.GAMMA) + reward_batch

        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values,expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()

        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()


    def train(self):
        for i_episode in range(self.number_of_episodes):
            frames = []

            state,info = self.env.reset()
            state = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)

            episode_reward = 0

            for t in count():
                action = self._select_action(state=state)
                observation, reward, terminated, truncated, _ = self.env.step(action=action.item())
                episode_reward += reward
                reward = torch.tensor([reward], device=self.device)
                done = terminated or truncated

                if terminated:
                    next_state = None
                else:
                    next_state = torch.tensor(observation, dtype=torch.float32,device=self.device).unsqueeze(0)

                self.replay_memory.push(state,action,next_state,reward)

                state=next_state

                self._optimize_model()

                target_net_state_dict = self.target_net.state_dict()
                policy_net_state_dict = self.policy_net.state_dict()
                for key in policy_net_state_dict:
                    target_net_state_dict[key] = policy_net_state_dict[key] * self.TAU + target_net_state_dict[key]* (1-self.TAU)
                self.target_net.load_state_dict(target_net_state_dict)

                if t < self.max_episode_recap_lenght: frames.append(self.env.render())
                if done:
                    update_episode_recap(i_episode, frames)
                    self.plotter.update_values(i_episode, episode_reward)
                    break