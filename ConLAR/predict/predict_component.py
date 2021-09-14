import json
import time
import os
import socket
import csv
import sys
import subprocess as sp
from threading import Thread, Event
from Queue import Empty
from utils.config import DefaultConfig
from execute.docker_interface import DockerInterface

class PredictComponent(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__config = DefaultConfig()
        self._stop = Event()
        fullpath = self.__config.full_path
        trainpath = self.__config.train
        predictpath = self.__config.predict
        outputpath = self.__config.output
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    @staticmethod
    def __sleep(sleep_time):
	if sleep_time is not 0:
		sp.call(["sleep", str(sleep_time)])
    def train(self):
 	#cmd = "sudo python3 /home/cdw/data/lstm.py"
        cmd = "sudo python3 " + trainpath
        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        output, _ = proc.communicate()
    def predict(self):
 	#cmd = "sudo python3 /home/cdw/data/predict.py"
        cmd = "sudo python3 " + predictpath
        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        output, _ = proc.communicate()
    def remain(self):
        fullpath = outputpath
        tfile = open(fullpath, "w")
        tfile.seek(0)
        tfile.truncate()  
        tfile.write("-1")
    def run(self):
        while not self.stopped():

            containers = DockerInterface.ps()
	    self.__sleep(3)
            for container in containers:
                print "try to predict container " + container["id"] + " detected"
                path = "/home/cdw/log/" + container["id"] + ".txt"
                nfile = open(path, "r+")
                lines = nfile.readlines()
                length = len(lines)
		print length
		if length > 12:
		    fullpath = "/home/cdw/dockercap-euc/" + "testdata.csv"
                    tfile = open(fullpath, "w")
                    tfile.seek(0)
                    tfile.truncate()  
		    tfile.flush()
                    tot = 0
                    for line3 in lines:
                        tot = tot + 1
                        #msg = time.ctime() + " " + res + "\n"
                        #file.write(msg)
                        if (tot >= length - 12):
                            res1 = line3.split()
                            ret = res1[5:6]
                            for a in ret:
			       aa = float(a.strip('%'))
			       print str(aa)
                            tfile.write(str(aa/100)+"\n")
			    tfile.flush()
                    self.predict()
		else:
                    self.remain()             	

        print
        "Terminating Predict Component"



