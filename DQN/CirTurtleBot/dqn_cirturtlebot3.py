#!/usr/bin/env python
import time

import numpy as np
import gym
import json

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input
from keras.optimizers import Adam, RMSprop

# from rl.agents.dqn import DQNAgent
from DQN.dqn import DQNAgent
from common.policy import BoltzmannQPolicy, EpsGreedyQPolicy, EpsDisGreedyQPolicy
# from rl.policy import BoltzmannQPolicy, EpsGreedyQPolicy
# from rl.memory import SequentialMemory
from common.memory import SequentialMemory

from matplotlib import pyplot
from keras.models import model_from_json
# from rl.callbacks import TestLogger, TrainEpisodeLogger, TrainIntervalLogger, Visualizer, CallbackList, FileLogger
from common.callbacks import TestLogger, TrainEpisodeLogger, TrainIntervalLogger, Visualizer, CallbackList, FileLogger
import environments
from datetime import datetime

timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# import gym_gazebo


if __name__ == '__main__':
    ENV_NAME = 'GazeboCircuit2TurtlebotLidar-v1'
    # ENV_NAME = 'GazeboCircuit2TurtlebotLidarNn-v1'

    # Get the environment and extract the number of actions.
    env = gym.make(ENV_NAME)
    np.random.seed(234)
    env.seed(234)
    nb_actions = env.action_space.n
    print('action numbers:{}'.format(nb_actions))
    # Next, we build a very simple model.
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))

    # model.add(Flatten(input_shape=(1, 5)))
    # model.add(Dense(16, input_dim=5, activation='relu'))
    model.add(Dense(24))
    model.add(Activation('relu'))
    model.add(Dense(24))
    model.add(Activation('relu'))
    model.add(Dense(24))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())

    # serialize model to JSON
    model_save = model.to_json()
    with open("save/NNmodel1.json", "w") as json_file:
        json_file.write(model_save)

    print("Saved model to disk!")

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=50000, window_length=1)
    # policy1 = BoltzmannQPolicy()
    policy1 = EpsDisGreedyQPolicy(eps=0.05, eps_decay=0.999)
    policy2 = BoltzmannQPolicy(tau=0.8)
    callback1 = FileLogger(filepath='save/nhistory1_{}'.format(timenow), interval=1)
    callback2 = FileLogger(filepath='save/nhistory2_{}'.format(timenow), interval=1)
    callback3 = FileLogger(filepath='save/nhistory3_{}'.format(timenow), interval=1)
    callback4 = FileLogger(filepath='save/nhistory4_{}'.format(timenow), interval=1)
    callback5 = FileLogger(filepath='save/nhistory5_{}'.format(timenow), interval=1)

    # dqn1 = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
    #               target_model_update=1e-2, policy=policy1)
    # dqn1.compile(Adam(lr=1e-3), metrics=['mae'])
    # history1 = dqn1.fit(env, nb_epsteps=5000, visualize=False, callbacks=[callback1], verbose=2)

    dqn2 = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, batch_size=32, nb_steps_warmup=1000,
                    target_model_update=1e-3, policy=policy2)
    dqn2.compile(Adam(lr=0.001), metrics=['mse'])
    # dqn2.save_weights('save/dqn_blotzmann0.8_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    history2 = dqn2.fit(env, nb_steps=200000, visualize=False, callbacks=[callback3], verbose=2)

    time.sleep(1800)

    # dqn3 = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
    #               target_model_update=1e-2, policy=policy1, enable_double_dqn=False)
    # dqn3.compile(Adam(lr=1e-3), metrics=['mae'])
    # history3 = dqn3.fit(env, nb_epsteps=100, visualize=False, callbacks=[callback3], verbose=2)

    # dqn4 = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
    #               target_model_update=1e-2, policy=policy2, enable_double_dqn=False)
    # dqn4.compile(Adam(lr=1e-3), metrics=['mae'])
    # history4 = dqn4.fit(env, nb_epsteps=100, visualize=False, callbacks=[callback4], verbose=2)

    # print(history1.history.keys())
    # print(len(history1.history['policy_config']))
    # print(history1.history['policy_config']['config'])
    # pyplot.plot(history1.history['policy_config']['eps'])
    # pyplot.show()

    # pyplot.subplot(2, 1, 1)
    # pyplot.plot(history.history['nb_episode_steps'], history.history['episode_reward'])

    '''
    pyplot.figure()
    pyplot.subplot(2, 1, 1)
    pyplot.plot(history1.history['episode_reward'], 'r--',history3.history['episode_reward'], 'b--')

    pyplot.subplot(2, 1, 2)
    #pyplot.plot(history1.history['nb_steps'], history1.history['episode_reward'], 'r', history2.history['nb_steps'], history2.history['episode_reward'], 'g')
    pyplot.plot(history2.history['episode_reward'], 'r', history4.history['episode_reward'], 'b')
    pyplot.show()

    #pyplot.savefig('save/BoltzmannQPolicy')
    '''

    # After training is done, we save the final weights.
    # dqn1.save_weights('save/dqn1_{}_weights_test.h5f'.format(ENV_NAME), overwrite=True)
    #dqn2.save_weights('save/dqn5_{}.h5f'.format(timenow), overwrite=True)
    # dqn3.save_weights('save/dqn3_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    # dqn4.save_weights('save/dqn4_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    #print('Weights saved!')

