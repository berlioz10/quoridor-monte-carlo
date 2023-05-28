
import math
import torch
from game.game import Game
from montecarlo.montecarlo import MonteCarlo
from network.actor_critic_conv import ActorCriticConv


def run_episode(worker_env: Game, worker_model: ActorCriticConv):
    values, logprobs, rewards = [],[],[]
    done = False

    if worker_env.human_turn:
        worker_env.make_random_move()
    
    state = worker_env.get_convolutional_layer()

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

def run_episode_monte_carlo(worker_env: MonteCarlo, worker_model: ActorCriticConv):
    values, logprobs, rewards = [],[],[]
    done = False

    no_runs_monte_carlo = 2000
    
    if not worker_env.root.game.human_turn:
        worker_env.run(no_runs_monte_carlo)
        worker_env.make_next_move()
    else:
        worker_env.run(no_runs_monte_carlo // 10)
    
    worker_env.root.game.print_game()
    
    state = worker_env.root.game.get_convolutional_layer_reversed()

    while done == False:
        policy, value = worker_model(state)
        values.append(value)
        logits = policy.view(-1)
        action_dist = torch.distributions.Categorical(logits=logits)
        action = action_dist.sample()
        logprob_ = policy.view(-1)[action]
        logprobs.append(logprob_)
        reward, done = worker_env.let_player_make_next_action(Game.reverse_action(action.detach().numpy()))
        print("A2C's move: " + str(Game.convert_action_into_move(Game.reverse_action(action.detach().numpy()))))
        worker_env.root.game.print_game()
        
        rewards.append(reward)
        if not done:
            worker_env.run(no_runs_monte_carlo)
            done = worker_env.make_next_move()
        no_runs_monte_carlo -= math.floor(no_runs_monte_carlo / 10)

        worker_env.root.game.print_game()

        state = worker_env.root.game.get_convolutional_layer_reversed()

    return values, logprobs, rewards