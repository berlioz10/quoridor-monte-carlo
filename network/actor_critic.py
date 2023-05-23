import torch
from torch import nn
from torch import optim
import numpy as np
from torch.nn import functional as F
import torch.multiprocessing as mp

from utils.consts import BOARD_PAWN_DIM, BOARD_WALL_DIM

class ActorCritic(nn.Module):
    def __init__(self):
        
        l1_dim = 750
        l2_dim = 750
        l3_actor_dim = 600
        l4_critic_dim = 500

        super(ActorCritic, self).__init__()
        self.l1 = nn.Linear(BOARD_PAWN_DIM * BOARD_PAWN_DIM * 2 + BOARD_WALL_DIM * BOARD_WALL_DIM, l1_dim)
        self.l2 = nn.Linear(l1_dim, l2_dim)
        self.l3 = nn.Linear(l2_dim, l3_actor_dim)
        self.actor_lin1 = nn.Linear(l3_actor_dim, BOARD_WALL_DIM * BOARD_WALL_DIM * 2 + 12)
        self.l4 = nn.Linear(l3_actor_dim, l4_critic_dim)
        self.critic_lin1 = nn.Linear(l4_critic_dim, 1)

    def forward(self, x):
        # x = F.normalize(x, dim=0)
        noise = torch.rand(x.shape) * 1e-2
        x = x + noise

        y = F.relu(self.l1(x))
        y = F.relu(self.l2(y))
        y = F.relu(self.l3(y))
        actor = F.log_softmax(self.actor_lin1(y), dim=0)
        # by detaching y, we mean that only the third layer will be affected by the critic
        # the other 2 layers will be modified by the actor
        c = F.relu(self.l4(y.detach()))
        critic = torch.tanh(self.critic_lin1(c))
        return actor, critic # return as a tuple