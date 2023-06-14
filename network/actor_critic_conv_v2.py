import torch
from torch import nn
from torch import optim
import numpy as np
from torch.nn import functional as F
import torch.multiprocessing as mp

from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM

class ActorCriticConvV2(nn.Module):
    def __init__(self):
        super(ActorCriticConvV2, self).__init__()

        conv1_dim = 16
        conv2_dim = 32
        l1_dim = 250
        l2_actor_dim = 200
        l3_critic_dim = 150
        no_maxpool_used = 0

        self.conv1 = nn.Conv2d(3, conv1_dim, kernel_size=3, stride=1, padding=1)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv2 = nn.Conv2d(conv1_dim, conv2_dim, kernel_size=3, stride=1, padding=1)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.l1 = nn.Linear(conv2_dim * pow(BOARD_PAWN_DIM // pow(2, no_maxpool_used), 2), l1_dim)
        self.l2 = nn.Linear(l1_dim, l2_actor_dim)
        self.actor_lin1 = nn.Linear(l2_actor_dim, 2)
        self.actor_lin2 = nn.Linear(l2_actor_dim, 12)
        self.actor_lin3 = nn.Linear(l2_actor_dim, BOARD_WALL_DIM * BOARD_WALL_DIM * 2)

        self.l3= nn.Linear(l2_actor_dim, l3_critic_dim)
        self.critic_lin1 = nn.Linear(l3_critic_dim, 1)

    def forward(self, x):
        # commenting the normalization part, because the data can only be 0, 1 and 2. Normalization is not necessary
        # x = F.normalize(x, dim=0)

        x = self.conv1(x)
        x = F.leaky_relu(x, negative_slope=0.01)
        # x = self.maxpool1(x)
        x = self.conv2(x)
        x = F.leaky_relu(x, negative_slope=0.01)
        # x = self.maxpool2(x)
        
        x = torch.flatten(x)

        y = F.relu(self.l1(x))
        y = F.relu(self.l2(y))
        
        actor_prob = F.log_softmax(self.actor_lin1(y), dim=0)
        actor_moves = F.log_softmax(self.actor_lin2(y), dim=0)
        actor_walls = F.log_softmax(self.actor_lin3(y), dim=0)
        actor = (actor_prob, actor_moves, actor_walls)
        # by detaching y, we mean that only the third layer will be affected by the critic
        # the other 2 layers will be modified by the actor
        c = F.relu(self.l3(y.detach()))
        critic = torch.tanh(self.critic_lin1(c))
        return actor, critic # return as a tuple