import torch
from game.game import Game
from network.actor_critic import ActorCritic
from network.actor_critic_conv import ActorCriticConv
import multiprocessing as mp
from collections import Counter
import numpy as np
import random

from matplotlib import pyplot as plt

from network.workers import custom_worker, custom_worker_conv
from utils.consts import NO_WALLS, SAVED_NETWORKS_DIR
from utils.functions import Functions

if __name__ == '__main__':
    MasterNode = ActorCritic()
    MasterNode.share_memory()
    processes : list[mp.Process] = []
    # it would be prefered that you use a number of threads divizible by 4
    params = {
    'epochs': 10000,
    'n_workers': 8,
    'lr': 1e-4,
    'gamma': 0.90,
    'clc': 0.1,
    'eps': 0.7,
    'random_position': Functions.return_false,
    'custom_walls': Functions.return_number_of_walls,
    'human_turn': Functions.return_false
    }

    counter = mp.Value('i', 0)

    it = params['n_workers'] // 4

    ep_list = mp.Array('d', range(params['epochs'] * it))
    loss_list = mp.Array('d', range(params['epochs'] * it))
    # list3 = mp.Array('d', range(params['epochs'] * it))
    # list4 = mp.Array('d', range(params['epochs'] * it))

    for i in range(it):
        p = mp.Process(target=custom_worker, args=(i, MasterNode, ep_list, loss_list, params))
        p.start()
        processes.append(p)

        params['human_turn'] = Functions.return_true
        
    for p in processes:
        p.join()

    for p in processes:
        p.terminate()

    torch.save(MasterNode.state_dict(), SAVED_NETWORKS_DIR + "test2.pt")

    first_graph_dict = Counter(ep_list[0:params['epochs']])

    plt.subplot(2, 2, 1)
    plt.bar(first_graph_dict.keys(), first_graph_dict.values(), label='AI first turn episode length')
    plt.legend()
    plt.title("Episode length per epochs A2C first")

    second_graph_dict = Counter(ep_list[params['epochs']:])

    plt.subplot(2, 2, 2)
    plt.bar(second_graph_dict.keys(), second_graph_dict.values(), label='AI second turn episode length')
    plt.legend()
    plt.title("Episode length per epochs A2C second")

    plt.subplot(2, 1, 2)
    plt.plot(loss_list[0:params['epochs']], label='AI first turn loss')
    plt.plot(loss_list[params['epochs']:], label='AI second turn loss')
    plt.legend()
    plt.title("Loss per epochs")

    plt.show()