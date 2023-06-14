import torch
from game.game import Game
import multiprocessing as mp
import numpy as np
import random

from matplotlib import pyplot as plt
from network.actor_critic_conv_v2 import ActorCriticConvV2

from network.workers_v2 import custom_worker_conv
from utils.consts import NO_WALLS, SAVED_NETWORKS_DIR
from utils.functions import Functions

if __name__ == '__main__':
    MasterNode = ActorCriticConvV2()
    MasterNode.share_memory()
    processes : list[mp.Process] = []
    # it would be prefered that you use a number of threads divizible by 4
    params = {
    'epochs': 50000,
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
        p = mp.Process(target=custom_worker_conv, args=(i, MasterNode, ep_list, loss_list, params))
        p.start()
        processes.append(p)

        params['human_turn'] = Functions.return_true
        
    for p in processes:
        p.join()

    for p in processes:
        p.terminate()

    torch.save(MasterNode.state_dict(), SAVED_NETWORKS_DIR + "test_v2.pt")

    figure, axis = plt.subplots(2, 1)
    
    axis[0].plot(ep_list[0:params['epochs']], label='AI first turn episode length')
    axis[0].plot(ep_list[params['epochs']:], label='AI second turn episode length')
    axis[0].legend()
    axis[0].set_title("Episode length per epochs")

    axis[1].plot(loss_list[0:params['epochs']], label='AI first turn loss')
    axis[1].plot(loss_list[params['epochs']:], label='AI second turn loss')
    axis[1].legend()
    axis[1].set_title("Loss per epochs")

    plt.show()