# -*- coding: UTF-8 -*-
import json
import time
import os
import sys
import logging
import math
from threading import Thread, Event
from Queue import Empty
import random
import subprocess as sp
from commons.interfaces.cgroup_interface import CGroupInterface
from commons.interfaces.docker_interface import DockerInterface
import numpy as np
class ActComponent(Thread):
	def __init__(self):
		Thread.__init__(self)
		self._stop = Event()
                self.cur_t = 0
	        self.p = 0.05
	def stop(self):
		self._stop()
        def console_out(self,logFilename):
    # Define a Handler and a format which output to file
            logging.basicConfig(
                level=logging.DEBUG,  
                format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', 
                datefmt='%Y-%m-%d %A %H:%M:%S',  
                filename=logFilename, 
                filemode='w') 
            console = logging.StreamHandler()  
            console.setLevel(logging.INFO)  
            formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)  
	
	def stopped(self):
		return self._stop.isSet()
        @staticmethod
        def __sleep(sleep_time):
                if sleep_time is not 0:
                    sp.call(["sleep", str(sleep_time)])
        def rlg(self,name,cur,tar,predict):
               update_times = 1
               if (self.cur_t == 0):
                   CGroupInterface.set_cpu_quota(value=100, container_id=name)
               self.cur_t = self.cur_t + 1
               cpuInterval = 5
               minEpsilon = 0.05  
               cpuMax = 20 
               actionMax = 3
               actionBias = 1  
               minCpu = 5
               maxCpu = 100
               q_table = np.zeros((cpuMax, actionMax))
               p_table = np.zeros((cpuMax, actionMax, cpuMax))  
               c_table = np.zeros((cpuMax))
               qAlpha = 0.1  
               cAlpha = 0.1  
               logging.info('\t \t main algorithm times start: ' + str(self.cur_t))
               cpuquota = CGroupInterface.get_cpu_quota(container_id=name) / 1000
               if cpuquota < 0:
                    cpuquota = 100
	       if cpuquota < 5:
                    cpuquota = 5
               logging.info('\tcpuquota:' + str(cpuquota))
               cpuIndex = math.floor(cpuquota / cpuInterval)
               if cpuIndex >= cpuMax:
                    cpuIndex = cpuMax - 1
               state = (int)(cpuIndex)
               logging.debug('\tencoding current state :' + '\tcpuIndex:' + str(cpuIndex))
               if cpuIndex < 0 or cpuIndex >= cpuMax :
                    logging.info('Index error')
                    cpuIndex = 100
               epsilon = minEpsilon
               logging.info('epsilon:' + str(epsilon))
               action = 0  
               if random.random() < epsilon:
                    action = math.floor(random.random() * 3)
                    logging.info('random select action(0~2):' + str(action))
               else:
                    min_value = np.min(q_table[state])
                    result = np.where(q_table[state] == min_value)[0]
                    if len(result) == 1:
                           action = np.where(q_table[state] == min_value)[0][0]
                    else:
                           label = math.floor(random.random() * len(result))
                           action = np.where(q_table[state] == min_value)[0][(int)(label)]
               logging.info('choose min action:' + str(action))
               logging.debug(str(q_table[state]))
               last_share = cpuquota;
               if (action == 0) :
                   last_share = (last_share + predict) / 2
               if (action == 1) :
                   last_share = last_share
               if (action == 2) :
                   last_share = last_share * (1 + p)
               logging.info('last cpuquota:' + str(cpuquota))
               logging.info('last share:' + str(last_share))
               if last_share < 5: 
                      last_share = 5
               if last_share > 100:
                      last_share = 100
               last_action = action - actionBias
               logging.info('last cpu:' + str(last_share) + ' last_action:' + str(last_action))
               msg = time.ctime() + " " + str(name) + " " + str(last_share) + "\n"
               fullpath1 = "/home/cdw/dockercap-euc/" + "config.txt"
               cfile = open(fullpath1,"a")
               cfile.write(msg)
               cfile.flush()
               CGroupInterface.set_cpu_quota(value=last_share, container_id=name)
               logging.info('execute')
               time.sleep(10)
               logging.info('execute over, get new state')
               cpuquota = CGroupInterface.get_cpu_quota(container_id=name) / 1000
               if cpuquota < 0:
                    cpuquota = 100
	       if cpuquota < 5:
                    cpuquota = 5
               logging.info('\tcpuquota:' + str(cpuquota))
               cpuIndex = math.floor(cpuquota / cpuInterval)
               if cpuIndex >= cpuMax:
                    cpuIndex = cpuMax - 1
               logging.debug('\tencoding current state :' + '\tcpuIndex:' + str(cpuIndex))
               stateNext = (int)(cpuIndex)
               if cpuIndex < 0 or cpuIndex >= cpuMax :
                    logging.info('Index error')
               cpuquota = CGroupInterface.get_cpu_quota(container_id=name) / 1000
               if cpuquota < 0:
                    cpuquota = 100
               costPerf = 0
               penalty = 0
               if cur>tar: penalty = 1;
               costApp = cpuquota / (cpuInterval *20);
               totalCost =  -0.1*costApp -0.9*penalty;
               logging.info('\ttotalCost:' + str(totalCost))
               print("state:" + str(state) + " " +str(stateNext))
               p_table[(int)(state), (int)(action), (int)(cpuIndex)] += 1
               c_table[stateNext] = (1 - cAlpha) * c_table[stateNext] + cAlpha * totalCost
               for i in range(update_times):
                 logging.info('update times:' + str(i))
                 for s in range(cpuMax):
                  for a in range(actionMax):
                    ncpu = s
                    totalExpectation = 0
                    totalCount = np.sum(p_table[s][a])
                    if totalCount == 0: 
                        continue
                    cpuIndex = ncpu + a - actionBias
                    if cpuIndex < 0 or cpuIndex >= cpuMax:  
                        continue
                    logging.debug(
                        'ready to update state(' + str(ncpu) + ','  + str(a) + ')')
                    result = np.where(p_table[s][a] != 0)
                    result1 = result[0]
                    for i in range(len(result1)):
                        cpuIndex = int(result1[i])
                        probability = p_table[s][a][cpuIndex] / totalCount
                        state = (int)(cpuIndex)
                        cost = c_table[state]
                        minActionValue = np.min(q_table[state])
                        totalExpectation += probability * (cost + qAlpha * minActionValue)
                    logging.info('previous Q table:' + str(q_table[s][a]))
                    q_table[s][a] = totalExpectation
               q_file = open('q_table.txt', 'wb')
               p_file = open('p_table.txt', 'wb')
               c_file = open('c_table.txt', 'wb')
               np.save(q_file, q_table)
               np.save(p_file, p_table)
               np.save(c_file, c_table)
               q_file.close()
               p_file.close()
               c_file.close()

	def run(self):
                self.console_out('logging.log')
                logging.info('RL algorithm start')
		while not self.stopped():
                     target = 10000
                     avgpath = "/home/cdw/log/" + "avgtime.txt"
                     afile = open(avgpath,"r")
                     lines = afile.readlines()
                     nowv =  10000
                     if len(lines) == 1:
                         nowv = (float)(lines[0])
                     fullpath = "/home/cdw/RLOPRE/" + "predict.csv"
                     pfile = open(fullpath, "r")
                     lines = pfile.readlines()
                     value = -1
                     if len(lines) == 1:
                         value = (float)(lines[0])
                     if (value < 0): value = 100
                     if value < 0.05: value = 0.05
                     print "read predict value" + str(value)
                     containers = DockerInterface.ps()
                     for container in containers:
                         self.rlg(container["id"],nowv,target,value*100)		
		print "Terminating RL Component"


