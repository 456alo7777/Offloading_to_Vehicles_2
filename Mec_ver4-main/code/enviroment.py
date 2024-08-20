#from code.config import Config, DATA_DIR, RESULT
import numpy as np
import pandas as pd
import gym
from gym import spaces
from gym.utils import seeding
import copy
import os
from VEC_util import getRateTransData
from  config import *
from MyGlobal import MyGlobals

class BusEnv(gym.Env):

    def __init__(self,env):
        self.env = env
        self.guess_count = 0
        self.number = 1
        self.n_tasks_in_node = [0] * (NUM_ACTION)
        self.n_tasks_delay_allocation = [0] * (NUM_ACTION)
        #self.n_tasks_drop_allocation = [0] * (NUM_ACTION)
        self.n_tasks_extra_allocation = [0] * (NUM_ACTION)
        self.n_tasks_sum_extra_allocation = [0] * (NUM_ACTION)
        self.action_space = spaces.Discrete(NUM_ACTION)
        self.observation_space = spaces.Box(0, 100, [NUM_STATE])
        
       
        data900 = self.preprocessBusLoction("xe1.xlsx")
        data901 = self.preprocessBusLoction("xe2.xlsx")
        data902 = self.preprocessBusLoction("xe3.xlsx")
        data903 = self.preprocessBusLoction("xe4.xlsx")
        data904 = self.preprocessBusLoction("xe5.xlsx")
        self.data_bus = {"900":data900 , "901":data901 , "902":data902 , "903":data903 , "904":data904}
        self.index_of_episode = -1 
        self.observation = np.array([-1])
        
        
        try:
            os.makedirs(RESULT_DIR + MyGlobals.folder_name)
            print(MyGlobals.folder_name)
        except OSError as e:
            print(e)
            
            
            
            
        #======== DEFINE FILE TO WRITE ON
        self.reward_files = open(
            RESULT_DIR + MyGlobals.folder_name + "reward.csv", "w")
        self.drop_files = open(
            RESULT_DIR + MyGlobals.folder_name + "drop_task.csv", "w")
        self.delay_files = open(
            RESULT_DIR + MyGlobals.folder_name + "delay.csv", "w")
        self.server_allocation = open(
            RESULT_DIR + MyGlobals.folder_name + "server_allocation.csv", "w")
        self.delay_allocation = open(
            RESULT_DIR + MyGlobals.folder_name + "delay_allocation.csv", "w")
        #self.drop_allocation = open(RESULT_DIR + MyGlobals.folder_name + "drop_allocation.csv","w")
        self.extra_allocation = open(
            RESULT_DIR + MyGlobals.folder_name + "extra_allocation.csv", "w")
        self.sum_extra_allocation = open(
            RESULT_DIR + MyGlobals.folder_name + "sum_extra_allocation.csv", "w")
        
        self.folder = RESULT_DIR + MyGlobals.folder_name
        self.rewardfiles = open(self.folder + "MAB_5phut_env.csv","w")
        self.quality_result_file = open(self.folder + "n_quality_tasks.csv","w")
        self.configuration_result_file = open(self.folder + "thongso.csv","w")
        self.node_computing = open(self.folder + "chiatask.csv","w")
        self.node_computing.write("somay,distance,may0,may1,may2,may3,may4,may5,reward\n")

        
        self.sum_reward = 0
        self.sum_reward_accumulate = 0
        self.sum_drop = 0
        self.sum_delay = 0
        self.nreward = 0
        self.nstep = 0
        
        
        tempstr = "server"
        for i in range(1, NUM_EDGE_SERVER):
            tempstr += ",bus" + str(i)
        tempstr += ",cloud"
        self.server_allocation.write(tempstr + '\n')
        self.delay_allocation.write(tempstr + '\n')
        #self.drop_allocation.write(tempstr + '\n')
        self.extra_allocation.write(tempstr + '\n')
        self.sum_extra_allocation.write(tempstr + '\n')
        self.reward_files.write('reward,reward_accumulate\n')
        self.drop_files.write('drop\n')
        self.delay_files.write('delay,delay_avg\n')
        self.quality_result_file.write("good,medium,bad\n")

        self.seed()
        
        
        
    def modifyEnv(self):
        ...
        #TODO

    #--------------------------
    
    def replay(self):
        data900 = self.preprocessBusLoction("xe1.xlsx")
        data901 = self.preprocessBusLoction("xe2.xlsx")
        data902 = self.preprocessBusLoction("xe3.xlsx")
        data903 = self.preprocessBusLoction("xe4.xlsx")
        data904 = self.preprocessBusLoction("xe5.xlsx")
        data905 = self.preprocessBusLoction("xe6.xlsx")
        self.data_bus = {"900": data900, "901": data901, "902": data902, "903": data903, "904": data904}
        self.index_of_episode = -1
        
    def setTest(self):
        self.replay()
        self.index_of_episode = 121
        
    def readexcel(self, number_bus, time):
        data = self.data_bus[str(number_bus)]

        after_time = data[data[:,1] >= time]
        pre_time = data[data[:,1]<=time]
        if len(after_time) == 0:
            return 1.8
        las = after_time[0]
        first = pre_time[-1]
        
        #weighted average of the distance
        if las[1] != first[1]:
            distance = (las[0] * (las[1]-time) + first[0] * (-first[1]+time)) / (las[1]-first[1])
        else:
            distance = las[0] 
        return distance

    def step(self, action):
        # for i in observation:
        #     print(observation)
        time_delay = 0
        
        #logic block when computing node is bus node
        if action>0 and action<NUM_EDGE_SERVER: #TODO
            
            distance_req = self.observation[(action-1)*2]
            old_waiting_queue = self.observation[1+(action-1)*2]
            Rate_trans_req_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_req,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)

            new_waiting_queue = self.observation[-3] / (List_COMPUTATION[action-1]) + max(self.observation[-2]/(Rate_trans_req_data),  # size of task / rate
                      old_waiting_queue)
  
            distance_response = self.readexcel(
                900+action-1, self.observation[1+(action-1)*2]+self.time)

            Rate_trans_res_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_response,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)
            time_delay = new_waiting_queue + \
                self.queue[0][3]/(Rate_trans_res_data)

            self.observation[1+(action-1)*2] = new_waiting_queue
            self.node_computing.write("{},{},{},{},{},{}".format(action,0,self.observation[9],self.observation[1],self.observation[4],self.observation[7]))

        #logic block when computing node is server
        elif action == 0:
            
            self.observation[-4] += self.observation[-3] / \
                (COMPUTATIONAL_CAPACITY_LOCAL)
            #import pdb;pdb.set_trace()

            time_delay = self.observation[-4]
            self.node_computing.write("{},{},{},{},{},{}".format(action,0,self.observation[9],self.observation[1],self.observation[4],self.observation[7]))
            
            
        self.n_tasks_in_node[action] = self.n_tasks_in_node[action]+1
        self.n_tasks_in_node[action] = self.n_tasks_in_node[action]+1
        # reward = max(0,min((2*self.observation[13]-time_delay)/self.observation[13],1))
        self.sum_delay = self.sum_delay + time_delay
        extra_time = min(0, self.observation[-1] - time_delay)
        self.n_tasks_extra_allocation[action] += extra_time
        reward = extra_time
        

        #check length of queue at this time and update state
        if len(self.queue) == 0 and len(self.data) != 0:
            self.queue = copy.deepcopy(
                self.data[self.data[:, 0] == self.data[0][0]])
            self.queue = self.queue[self.queue[:, 2].argsort()]


            # position of cars
            for a in range(NUM_VEHICLE):
                self.observation[a*2] = self.readexcel(900+a, self.data[0][0])

            time = self.data[0][0] - self.time
            
            
            for i in range(NUM_VEHICLE):
                self.observation[2 * i +
                                 1] = max(0, self.observation[2 * i + 1]-time)
            self.observation[-4] = max(0, self.observation[-4]-time)
            self.time = self.data[0][0]
            self.data = self.data[self.data[:,0]!=self.data[0,0]]
        
        if len(self.queue)!=0:
            
            self.observation[-3] = self.queue[0][1]
            self.observation[-2] = self.queue[0][2]
            self.observation[-1] = self.queue[0][4]
        
        #check end of episode?
        done = len(self.queue) == 0 and len(self.data) == 0

        
        self.sum_reward += reward
        self.sum_reward_accumulate += reward
        if self.observation[-1] < time_delay:
            self.sum_drop += 1
            #self.n_tasks_drop_allocation[action] += 1
        self.nreward += 1
        self.nstep += 1
        
        
        #====== KHONG  BIET CO CAN THIET KHONG
        if done:
            print(self.n_tasks_in_node)
            tempstr = ','.join([str(elem) for elem in self.n_tasks_in_node])
            self.server_allocation.write(tempstr+"\n")
            tempstr = ','.join([str(elem/nb_step) if nb_step else '0' for elem, nb_step in zip(
                self.n_tasks_delay_allocation, self.n_tasks_in_node)])
            self.delay_allocation.write(tempstr+"\n")
            #tempstr = ','.join([str(elem) for elem in self.n_tasks_drop_allocation])
            # self.drop_allocation.write(tempstr+"\n")
            tempstr = ','.join([str(elem/nb_step) if nb_step else '0' for elem, nb_step in zip(
                self.n_tasks_extra_allocation, self.n_tasks_in_node)])
            self.extra_allocation.write(tempstr+"\n")
            tempstr = ','.join([str(elem)
                               for elem in self.n_tasks_sum_extra_allocation])
            self.sum_extra_allocation.write(tempstr+"\n")
            # self.quality_result_file.write("{},{},{}\n".format(self.n_quality_tasks[0],self.n_quality_tasks[1],self.n_quality_tasks[2]))

            # check end of program? to close files
            avg_reward = self.sum_reward/self.nstep
            avg_reward_accumulate = self.sum_reward_accumulate/self.nreward
            self.reward_files.write(
                str(avg_reward)+','+str(avg_reward_accumulate)+"\n")
            self.drop_files.write(str(self.sum_drop/self.nstep)+"\n")
            self.delay_files.write(
                str(self.sum_delay)+','+str(self.sum_delay/self.nstep)+"\n")
            #print(self.sum_drop, self.nstep)
            self.old_avg_reward = self.sum_reward/self.nstep
            self.sum_reward = 0
            self.nstep = 0
            self.sum_drop = 0
            self.sum_delay = 0
            # if self.index_of_episode == 200:
            #     self.quality_result_file.close()
            #     self.server_allocation.close()
            #     self.node_computing.close()

        # observation has distance, queue, static queue, input, computation, deadline
        return self.observation, reward, done, {"number": self.number, "guesses": self.guess_count}
    
    
    def estimate(self, action):
        time_delay = 0
        deadline = self.observation[-1]
        #action += 1

        # bus
        if action > 0 and action < NUM_EDGE_SERVER:
            # v(A, F)
            distance_req = self.observation[(action-1)*2]
            old_waiting_queue = self.observation[1+(action-1)*2]
            Rate_trans_req_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_req,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)

            # print('rate:', Rate_trans_req_data, distance_req)
            # waiting queue                        # computation required / computation

            time_before_return = self.observation[-3] / (List_COMPUTATION[action-1])       \
                + max(self.observation[-2]/(Rate_trans_req_data),  # size of task / rate
                      old_waiting_queue)
        # base station
        elif action == 0:
            # queue time += size of task / computation
            time_before_return = self.observation[-4] + \
                self.observation[-3]/(COMPUTATIONAL_CAPACITY_LOCAL)
        # cloud
        else:
            time_before_return = (self.queue[0][2]) / TRANS_RATE_EDGE_TO_CLOUD + \
                self.observation[-3]/(COMPUTATIONAL_CAPACITY_CLOUD)

        return time_before_return, self.observation
    
    
    def predict_reward(self):
        time_delay = 0
        deadline = self.observation[-1]
        reward = dict()
        
        #logic block when computing node is bus node
        
        
        for action in range(1, NUM_VEHICLE+1):
            distance_req = self.observation[(action-1)*2]
            old_waiting_queue = self.observation[1+(action-1)*2]
            Rate_trans_req_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_req,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)

            # print('rate:', Rate_trans_req_data, distance_req)
            # waiting queue                        # computation required / computation

            new_waiting_queue = self.observation[-3] / (List_COMPUTATION[action-1])       \
                + max(self.observation[-2]/(Rate_trans_req_data),  # size of task / rate
                      old_waiting_queue)
            # print(self.observation[1+(action-1)*2])
            distance_response = self.readexcel(
                900+action-1, self.observation[1+(action-1)*2]+self.time)

            Rate_trans_res_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_response,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)
            time_delay = new_waiting_queue + \
                self.queue[0][3]/(Rate_trans_res_data)

            self.observation[1+(action-1)*2] = new_waiting_queue

                
            extra_time = min(0, self.observation[-1] - time_delay)
            self.n_tasks_extra_allocation[action] += extra_time

            #reward = 1 if (self.observation[-1] >= time_delay) else -100
            #reward = -time_delay
            reward = extra_time
            # reward[str(action)] = max(0,min((2*self.observation[13]-time_delay)/self.observation[13],1))
        
        #logic block when computing node is server
        action = 0

        time_delay = self.observation[-4]
        reward[str(action)] = max(0,min((2*self.observation[-1]-time_delay)/self.observation[-1],1))
        return reward
    
    
    def get_average_reward(self):
        avg_reward = 0
        try:
            avg_reward = self.sumreward/ self.nreward
        except:
            pass
        return avg_reward

    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        if self.index_of_episode == -1:
            self.index_of_episode = 0
            self.data = pd.read_csv(os.path.join(DATA_TASK, "datatask{}.csv".format(
                self.index_of_episode)), header=None).to_numpy()


            self.n_quality_tasks = [0, 0, 0]
            self.queue = copy.deepcopy(
                self.data[self.data[:, 0] == self.data[0][0]])
            self.queue = self.queue[self.queue[:, 2].argsort()]
            self.data = self.data[self.data[:, 0] != self.data[0][0]]
            self.result = []
            self.time_last = self.data[-1][0]
            self.time = self.queue[0][0]

            # first observation of agent about evironment

            self.observation = np.zeros(2 + 2 * NUM_EDGE_SERVER)
            for i in range(NUM_EDGE_SERVER - 1):
                self.observation[2 *
                                 i] = self.readexcel(900 + i, self.queue[0][0])
            self.observation[-3] = self.queue[0][1]
            self.observation[-2] = self.queue[0][2]
            self.observation[-1] = self.queue[0][4]

            return self.observation

        self.result = []
        self.number = 0
        self.guess_count = 0

        self.n_quality_tasks = [0, 0, 0]
        self.n_tasks_in_node = [0] * NUM_ACTION
        self.n_tasks_delay_allocation = [0] * NUM_ACTION
        self.n_tasks_extra_allocation = [0] * NUM_ACTION
        self.n_tasks_sum_extra_allocation = [0] * NUM_ACTION
        self.index_of_episode = self.index_of_episode + 1
        self.data = pd.read_csv(os.path.join(DATA_TASK, "datatask{}.csv".format(
            self.index_of_episode)), header=None).to_numpy()

        self.queue = copy.deepcopy(
            self.data[self.data[:, 0] == self.data[0][0]])
        self.queue = self.queue[self.queue[:, 2].argsort()]
        self.data = self.data[self.data[:, 0] != self.data[0][0]]
        self.time = self.queue[0][0]
        for i in range(NUM_EDGE_SERVER - 1):
            self.observation[2 * i] = self.readexcel(900 + i, self.queue[0][0])
            self.observation[2 * i + 1] = max(
                0, self.observation[2 * i + 1]-(self.time-self.time_last))
        self.observation[-4] = max(0, self.observation[-4] -
                                   (self.time-self.time_last))
        self.observation[-3] = self.queue[0][1]
        self.observation[-2] = self.queue[0][2]
        self.observation[-1] = self.queue[0][4]

        self.time_last = self.data[-1][0]

        return self.observation
        
    def render(self,mode='human'):
        pass
    
    
    def preprocessBusLoction(self, excel_file):
        a = pd.read_excel(os.path.join(DATA_DIR, excel_file)).to_numpy()
        a = a[:500, 9:11]
        temp = np.zeros(a.shape)
        temp[:, 1] = a[:500, 1].min()
        a -= temp
        return a
    
    
class NoFogEnv(BusEnv):
    def __init__(self):
        super().__init__()


