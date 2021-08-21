import json
import time
import os
import socket
import csv
import sys
import subprocess as sp
from threading import Thread, Event
from Queue import Empty
from decide.utils.config import DefaultConfig
from commons.interfaces.docker_interface import DockerInterface

class PredictComponent(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__config = DefaultConfig()
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    @staticmethod
    def __sleep(sleep_time):
	if sleep_time is not 0:
		sp.call(["sleep", str(sleep_time)])
    def train(self):
        if os.path.exists('/home/cdw/dockercap-euc/model.h5'):
            os.remove('/home/cdw/dockercap-euc/model.h5')
 	cmd = "sudo python3 /home/cdw/data/lstm.py"
        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        output, _ = proc.communicate()
    def predict(self):
 	cmd = "sudo python3 /home/cdw/data/predict.py"
        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        output, _ = proc.communicate()
    def remain(self):
        fullpath = "/home/cdw/dockercap-euc/" + "predict.csv"
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
                if length > 10000:
                    #fullpath = "/home/cdw/log/" + "train" + container["id"] + ".csv"
		    fullpath = "/home/cdw/dockercap-euc/" + "traindata.csv"
                    tfile = open(fullpath, "w")
                    tfile.seek(0)
                    tfile.truncate()  
                    tfile.write("value\n")
		    tfile.flush()
                    for line3 in lines:
                        #msg = time.ctime() + " " + res + "\n"
                        #file.write(msg)
                        res1 = line3.split()
                        ret = res1[5:6]
                        for a in ret:
			    aa = float(a.strip('%'))
			    print str(aa)
                            tfile.write(str(int(aa*100))+"\n")
			    tfile.flush()
		    nfile.seek(0)
		    nfile.truncate()
		    self.train()
		elif length > 12:
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



