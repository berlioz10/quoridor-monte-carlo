
import torch
from game.game import Game
from network.actor_critic_conv import ActorCriticConv


def run_episode_conv(worker_env: Game, worker_model: ActorCriticConv):
    state = worker_env.get_convolutional_layer()
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

        state = worker_env.get_convolutional_layer()

    return values, logprobs, rewards
