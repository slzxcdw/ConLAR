import subprocess
import json
import time
import sys

from threading import Thread, Event
from sources.resources_source import ResourcesSource
from utils.config import DefaultConfig

class ObserveComponent(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.__resources_source = ResourcesSource()
		self.__config = DefaultConfig()
		self._stop = Event()
	
	def stop(self):
		self._stop.set()
	
	def stopped(self):
		return self._stop.isSet()

	@staticmethod
	def __sleep(sleep_time):
		if sleep_time is not 0:
			subprocess.call(["sleep", str(sleep_time)])

	def run(self):
		while not self.stopped():
			try:
				resources = self.__resources_source.get_resources()
			except RuntimeError:
				print "no container detected"
			self.__sleep(3)

		print "Terminating Observe Component"
