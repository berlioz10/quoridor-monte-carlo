import torch
from torch import nn
from torch import optim
import numpy as np
from torch.nn import functional as F
import torch.multiprocessing as mp

from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM

class ActorCriticConv(nn.Module):
    def __init__(self):
        super(ActorCriticConv, self).__init__()

        conv1_dim = 32
        conv2_dim = 64
        l1_dim = 250
        l2_actor_dim = 200
        l3_critic_dim = 150
        no_maxpool_used = 0

        self.conv1 = nn.Conv2d(3, conv1_dim, kernel_size=3, stride=1, padding=1)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
        self.dropout1 = nn.Dropout(0.0)

        self.conv2 = nn.Conv2d(conv1_dim, conv2_dim, kernel_size=3, stride=1, padding=1)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
        self.dropout2 = nn.Dropout(0.0)

        self.l1 = nn.Linear(conv2_dim * pow(BOARD_PAWN_DIM // pow(2, no_maxpool_used), 2), l1_dim)
        self.l2 = nn.Linear(l1_dim, l2_actor_dim)
        self.actor_lin1 = nn.Linear(l2_actor_dim, BOARD_WALL_DIM * BOARD_WALL_DIM * 2 + 12)

        self.l3= nn.Linear(l2_actor_dim, l3_critic_dim)
        self.critic_lin1 = nn.Linear(l3_critic_dim, 1)

    def forward(self, x):
        # commenting the normalization part, because the data can only be 0, 1 and 2. Normalization is not necessary
        # x = F.normalize(x, dim=0)

        x = self.conv1(x)
        x = F.relu(x)
        # x = self.maxpool1(x)
        x = self.conv2(x)
        x = F.relu(x)
        # x = self.maxpool2(x)
        
        x = torch.flatten(x)

        y = F.relu(self.l1(x))
        y = self.dropout1(y)
        y = F.relu(self.l2(y))
        y = self.dropout2(y)
        actor = F.log_softmax(self.actor_lin1(y), dim=0)
        # by detaching y, we mean that only the third layer will be affected by the critic
        # the other 2 layers will be modified by the actor
        c = F.relu(self.l3(y.detach()))
        critic = torch.tanh(self.critic_lin1(c))
        return actor, critic # return as a tuple