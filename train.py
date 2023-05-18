import torch
from game.game import Game
from networks.actor_critic import ActorCritic
import multiprocessing as mp
import numpy as np
import random

from networks.workers import simple_worker

if __name__ == '__main__':
    MasterNode = ActorCritic()
    MasterNode.share_memory()
    processes : list[mp.Process] = []
    # it would be prefered that you use a number of threads divizible by 4
    params = {
    'epochs':1000,
    'n_workers':16,
    }

    counter = mp.Value('i', 0)
    for i in range(params['n_workers'] / 4):
        p = mp.Process(target=simple_worker, args=(i, MasterNode, counter, params))
        p.start()
        processes.append(p)

    for i in range(params['n_workers'] / 4):
        p = mp.Process(target=simple_worker, args=(i, MasterNode, counter, params))
        p.start()
        processes.append(p)

    for i in range(params['n_workers'] / 4):
        p = mp.Process(target=simple_worker, args=(i, MasterNode, counter, params))
        p.start()
        processes.append(p)

    for i in range(params['n_workers'] / 4):
        p = mp.Process(target=simple_worker, args=(i, MasterNode, counter, params))
        p.start()
        processes.append(p)
        
    for p in processes:
        p.join()

    for p in processes:
        p.terminate()