from deep_rl import *

def dqn_pixel(**kwargs):
    generate_tag(kwargs)
    kwargs.setdefault('log_level', 0)
    kwargs.setdefault('n_step', 1)
    kwargs.setdefault('replay_cls', UniformReplay)
    kwargs.setdefault('async_replay', False)
    config = Config()
    config.merge(kwargs)

    config.task_fn = lambda: Task(config.game)
    config.eval_env = config.task_fn()

    config.optimizer_fn = lambda params: torch.optim.RMSprop(
        params, lr=0.00025, alpha=0.95, eps=0.01, centered=True)
    config.network_fn = lambda: VanillaNet(config.action_dim, NatureConvBody(in_channels=config.history_length))
    # config.network_fn = lambda: DuelingNet(config.action_dim, NatureConvBody(in_channels=config.history_length))
    config.random_action_prob = LinearSchedule(1.0, 0.01, 1e6)
    config.batch_size = 32
    config.discount = 0.99
    config.history_length = 4
    config.max_steps = int(2e7)
    replay_kwargs = dict(
        memory_size=int(1e6),
        batch_size=config.batch_size,
        n_step=config.n_step,
        discount=config.discount,
        history_length=config.history_length,
    )
    config.replay_fn = lambda: ReplayWrapper(config.replay_cls, replay_kwargs, config.async_replay)
    config.replay_eps = 0.01
    config.replay_alpha = 0.5
    config.replay_beta = LinearSchedule(0.4, 1.0, config.max_steps)

    config.state_normalizer = ImageNormalizer()
    config.reward_normalizer = SignNormalizer()
    config.target_network_update_freq = 10000
    # config.exploration_steps = 50000
    config.exploration_steps = 100
    config.sgd_update_frequency = 4
    config.gradient_clip = 5
    config.double_q = True
    config.async_actor = False
    run_steps(DQNAgent(config))

if __name__ == '__main__':
    mkdir('log')
    mkdir('tf_log')
    # set_one_thread()
    random_seed()
    # -1 is CPU, a positive integer is the index of GPU
    select_device(-1)
    # select_device(0)
    game = 'PongNoFrameskip-v4'
    # dqn_feature(game=game, n_step=1, replay_cls=UniformReplay, async_replay=True, noisy_linear=True)
    # quantile_regression_dqn_feature(game=game)
    # categorical_dqn_feature(game=game)
    # rainbow_feature(game=game)
    # a2c_feature(game=game)
    # n_step_dqn_feature(game=game)
    # option_critic_feature(game=game)

    # game = 'HalfCheetah-v2'
    # game = 'Hopper-v2'
    # a2c_continuous(game=game)
    # ppo_continuous(game=game)
    # ddpg_continuous(game=game)
    # td3_continuous(game=game)

    # game = 'BreakoutNoFrameskip-v4'
    dqn_pixel(game=game, n_step=1, replay_cls=PrioritizedReplay, async_replay=True)