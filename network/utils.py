
import torch

from game.game import Game
from network.actor_critic import ActorCritic
from torch.nn import functional as F


def run_episode(worker_env: Game, worker_model: ActorCritic):
    state = torch.from_numpy(worker_env.get_linear_state()).float()
    values, logprobs, rewards = [],[],[]
    done = False

    if worker_env.human_turn:
        worker_env.make_random_move()
    
    while done == False:
        policy, value = worker_model(state)
        values.append(value)
        logits = policy.view(-1)
        action_dist = torch.distributions.Categorical(logits=logits)
        action = action_dist.sample()
        logprob_ = policy.view(-1)[action]
        logprobs.append(logprob_)
        reward, done = worker_env.step(action.detach().numpy())
        rewards.append(reward)
        if not done:
            _, done = worker_env.make_random_move()

        state = torch.from_numpy(worker_env.get_linear_state()).float()

    return values, logprobs, rewards


def update_params(worker_opt: torch.optim.Adam, values, logprobs, rewards, clc=0.1, gamma=0.98):
    rewards = torch.Tensor(rewards).flip(dims=(0,)).view(-1)
    logprobs = torch.stack(logprobs).flip(dims=(0,)).view(-1)
    values = torch.stack(values).flip(dims=(0,)).view(-1)
    Returns = []
    ret_ = torch.Tensor([0])
    # calculate the discounted reward
    for r in range(rewards.shape[0]):
        ret_ = rewards[r] + gamma * ret_
        Returns.append(ret_)
    Returns = torch.stack(Returns).view(-1)
    Returns = F.normalize(Returns, dim=0)
    # Actor loss
    actor_loss = -1 * logprobs * (Returns - values.detach())
    # Critic loss
    critic_loss = torch.pow(values - Returns, 2)
    
    loss = actor_loss.sum() + clc * critic_loss.sum()
    
    loss.backward()
    worker_opt.step()

    return loss, len(rewards)
