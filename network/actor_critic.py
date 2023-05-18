import torch
from torch import nn
from torch import optim
import numpy as np
from torch.nn import functional as F
import torch.multiprocessing as mp

from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM

class ActorCritic(nn.Module):
    def __init__(self):
        super(ActorCritic, self).__init__()
        self.l1 = nn.Linear(BOARD_WALL_DIM * BOARD_WALL_DIM + BOARD_PAWN_DIM * BOARD_PAWN_DIM, 200)
        self.l2 = nn.Linear(200, 200)
        self.actor_lin1 = nn.Linear(200, BOARD_WALL_DIM * BOARD_WALL_DIM * 2 + 4)
        self.l3 = nn.Linear(200, 150)
        self.critic_lin1 = nn.Linear(150, 1)

    def forward(self, x):
        x = F.normalize(x, dim=0)
        y = F.relu(self.l1(x))
        y = F.relu(self.l2(y))
        actor = F.log_softmax(self.actor_lin1(y), dim=0)
        # by detaching y, we mean that only the third layer will be affected by the critic
        # the other 2 layers will be modified by the actor
        c = F.relu(self.l3(y.detach()))
        critic = torch.tanh(self.critic_lin1(c))
        return actor, critic # return as a tuple