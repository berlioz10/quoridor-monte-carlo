import random

import torch
from game.game import Game
from network.actor_critic import ActorCritic
import multiprocessing as mp
from network.actor_critic_conv import ActorCriticConv

from network.utills import run_episode, update_params
from network.utils_conv import run_episode_conv

def custom_worker(t, worker_model: ActorCritic, ep_list: mp.Array, loss_list: mp.Array, params):
    worker_env = Game()
    worker_env.custom_reset(human_turn=params['human_turn'](), random_position=params['random_position'](), custom_walls=params['custom_walls']())

    worker_opt = torch.optim.Adam(lr=params['lr'], params=worker_model.parameters())
    worker_opt.zero_grad()
    for i in range(params['epochs']):
        worker_opt.zero_grad()
        
        values, logprobs, rewards = run_episode(worker_env, worker_model)
        
        loss, eplen = update_params(worker_opt, values, logprobs, rewards, gamma=params['gamma'])

        ep_list[t * params['epochs'] + i] = eplen
        loss_list[t * params['epochs'] + i] = loss

        if rewards[-1] == -30:
            print("Process " + str(t) + " epoch " + str(i) + ": " + '\033[0;31;40m' + str(rewards) + '\033[0;0;0m')
        else:
            print("Process " + str(t) + " epoch " + str(i) + ": " + str(rewards))

        worker_env.custom_reset(human_turn=params['human_turn'](), random_position=params['random_position'](), custom_walls=params['custom_walls']())


def custom_worker_conv(t, worker_model: ActorCriticConv, ep_list: mp.Array, loss_list: mp.Array, params):
    worker_env = Game()
    
    worker_env.custom_reset(human_turn=params['human_turn'](), random_position=params['random_position'](), custom_walls=params['custom_walls']())
    
    worker_opt = torch.optim.Adam(lr=params['lr'], params=worker_model.parameters())
    worker_opt.zero_grad()
    for i in range(params['epochs']):
        worker_opt.zero_grad()
        
        values, logprobs, rewards = run_episode_conv(worker_env, worker_model)
        if rewards[-1] == -30:
            print("Process " + str(t) + " epoch " + str(i) + ": " + '\033[0;31;40m' + str(rewards) + '\033[0;0;0m')
        else:
            print("Process " + str(t) + " epoch " + str(i) + ": " + str(rewards))
        
        loss, eplen = update_params(worker_opt, values, logprobs, rewards, clc=params['clc'], gamma=params['gamma'])

        ep_list[t * params['epochs'] + i] = eplen
        loss_list[t * params['epochs'] + i] = loss

        worker_env.custom_reset(human_turn=params['human_turn'](), random_position=params['random_position'](), custom_walls=params['custom_walls']())