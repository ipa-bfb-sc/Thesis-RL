import numpy as np
import gym
import json

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD

#from DQN.dqn import DQNAgent
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from matplotlib import pyplot
from matplotlib.ticker import FuncFormatter
from keras.models import model_from_json

### discounted_rate comparison:0.1, 0.5, 0.99, in Boltzmann, 64


with open('save/history6_2018-06-20 10:43:24', 'r') as f:
    pp1_1 = json.load(f)
    f.close()

with open('save/history6_2018-06-20 10:59:28', 'r') as f:
    pp1_2 = json.load(f)
    f.close()

with open('save/history6_2018-06-20 11:13:41', 'r') as f:
    pp1_3 = json.load(f)
    f.close()

with open('save/history6_2018-06-20 11:28:06', 'r') as f:
    pp1_4 = json.load(f)
    f.close()

with open('save/history6_2018-06-20 11:41:54', 'r') as f:
    pp1_5 = json.load(f)
    f.close()


with open('save/history7_2018-06-20 10:43:28', 'r') as f:
    pp2_1 = json.load(f)
    f.close()

with open('save/history7_2018-06-20 10:59:35', 'r') as f:
    pp2_2 = json.load(f)
    f.close()

with open('save/history7_2018-06-20 11:13:45', 'r') as f:
    pp2_3 = json.load(f)
    f.close()

with open('save/history7_2018-06-20 11:28:39', 'r') as f:
    pp2_4 = json.load(f)
    f.close()

with open('save/history7_2018-06-20 11:43:02', 'r') as f:
    pp2_5 = json.load(f)
    f.close()



with open('save/history8_2018-06-20 10:43:33', 'r') as f:
    pp3_1 = json.load(f)
    f.close()

with open('save/history8_2018-06-20 11:48:57', 'r') as f:
    pp3_2 = json.load(f)
    f.close()

with open('save/history8_2018-06-20 12:43:49', 'r') as f:
    pp3_3 = json.load(f)
    f.close()

with open('save/history8_2018-06-20 13:58:47', 'r') as f:
    pp3_4 = json.load(f)
    f.close()

with open('save/history8_2018-06-20 14:25:12', 'r') as f:
    pp3_5 = json.load(f)
    f.close()

duration1 = (sum(pp1_1['duration'])+sum(pp1_2['duration'])+sum(pp1_3['duration'])+sum(pp1_4['duration'])+sum(pp1_5['duration']))/5
duration2 = (sum(pp2_1['duration'])+sum(pp2_2['duration'])+sum(pp2_3['duration'])+sum(pp2_4['duration'])+sum(pp2_5['duration']))/5
duration3 = (sum(pp3_1['duration'])+sum(pp3_2['duration'])+sum(pp3_3['duration'])+sum(pp3_4['duration'])+sum(pp3_5['duration']))/5

print('Duration1:{}, Duration2:{}, Duration3:{}'.format(duration1,duration2,duration3))

er_ave1 = [(pp1_1['episode_reward'][i] + pp1_2['episode_reward'][i]+pp1_3['episode_reward'][i]+pp1_4['episode_reward'][i]+pp1_5['episode_reward'][i])/5 for i in range(len(pp1_1['episode_reward']))]
er_ave2 = [(pp2_1['episode_reward'][i] + pp2_2['episode_reward'][i]+pp2_3['episode_reward'][i]+pp2_4['episode_reward'][i]+pp2_5['episode_reward'][i])/5 for i in range(len(pp2_1['episode_reward']))]
er_ave3 = [(pp3_1['episode_reward'][i] + pp3_2['episode_reward'][i]+pp3_3['episode_reward'][i]+pp3_4['episode_reward'][i]+pp3_5['episode_reward'][i])/5 for i in range(len(pp3_1['episode_reward']))]
#er_ave4 = [(pp4_1['episode_reward'][i] + pp4_2['episode_reward'][i]+pp4_3['episode_reward'][i]+pp4_4['episode_reward'][i]+pp4_5['episode_reward'][i])/5 for i in range(len(pp4_1['episode_reward']))]

#pyplot.subplot(2, 1, 1)

pyplot.figure(num=1, figsize=(20, 10),)
pyplot.xlabel('episodes', fontsize=24)
pyplot.ylabel('rewards per episode', fontsize=24)
pyplot.title('Discounted rate comparison', fontsize=24)

new_ticks = np.linspace(0, 3000, 30)
pyplot.xticks(new_ticks)
pyplot.plot(er_ave1, 'r', label='discount_rate=0.1')
pyplot.plot(er_ave2, 'g', label='discount_rate=0.5')
pyplot.plot(er_ave3, 'b', label='discount_rate=0.99')
pyplot.legend()
pyplot.savefig('save/pics/cartpole_discount_rate.png',bbox_inches='tight')


pyplot.figure(num=2, figsize=(8, 5),)
width = 0.2
x = np.arange(3)
duration_compare = [duration1,duration2,duration3]
fig, ax = pyplot.subplots()
rects1 = ax.bar(x, duration_compare, width)

pyplot.xticks(x, ('discount_rate=0.1', 'discount_rate=0.5', 'discount_rate=0.99'))
ax.set_ylabel('Duration')
ax.set_title('Training time with different discounted rate')
pyplot.savefig('save/pics/cartpole_duration_DR.png',bbox_inches='tight')
pyplot.show()
