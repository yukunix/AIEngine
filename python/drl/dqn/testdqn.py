'''
Created on 4 May 2017

@author: Yukun
'''
import gym
from drl.dqn.dqn import DQN
from drl.dqn.Environment import Environment

# Hyper Parameters
ENV_NAME = 'CartPole-v0'
EPISODE = 10000 # Episode limitation
STEP = 300 # Step limitation in an episode
TEST = 10 # The number of experiment test every 100 episode

class GynEnv(Environment):
    
    def __init__(self):
        self.gym_env = gym.make(ENV_NAME)
    
    @property
    def state_dim(self):
        return self.gym_env.observation_space.shape[0]
    
    @property
    def action_dim(self):
        return self.gym_env.action_space.n
    
    def reset(self):
        return self.gym_env.reset()
    
    def render(self, *args, **kwargs):
        return self.gym_env.render(*args, **kwargs)
    
    def step(self, action):
        return self.gym_env.step(action)
        

def test_tfdqn2():
    # initialize OpenAI Gym env and dqn agent
    env = GynEnv(); 
    agent = DQN(env)

    for episode in range(EPISODE):
        # initialize task
        state = env.reset()
        # Train 
        for step in range(STEP):
            action = agent.egreedy_action(state) # e-greedy action for train
            next_state,reward,done,_ = env.step(action)
            # Define reward for agent
            reward_agent = -1 if done else 0.1
            agent.perceive(state,action,reward,next_state,done)
            state = next_state
            if done:
                break
        # Test every 100 episodes
        if episode % 100 == 0:
            total_reward = 0
            for i in range(TEST):
                state = env.reset()
                sub_reward = 0;
                for j in range(STEP):
#                     env.render()
                    action = agent.action(state) # direct action for test
                    state,reward,done,_ = env.step(action)
                    total_reward += reward
                    sub_reward += reward
                    if done:
                        print('sub reward: ', sub_reward)
                        break
            ave_reward = total_reward/TEST
            print('episode: ',episode,'Evaluation Average Reward:',ave_reward)
            if ave_reward >= 200:
                break

    # save results for uploading
    #env.monitor.start('gym_results/CartPole-v0-experiment-1',force = True)
    for i in range(100):
        state = env.reset()
        total_reward = 0
        for j in range(200):
            env.render()
            action = agent.action(state) # direct action for test
            state,reward,done,_ = env.step(action)
            total_reward += reward
            if done:
                print('total reward:', total_reward)
                break
    #env.monitor.close()
    

if __name__ == '__main__':
    test_tfdqn2()
