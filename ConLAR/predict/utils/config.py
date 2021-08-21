import os
from xml.etree import ElementTree

class Config:
	def __init__(self):
		self.update()

	def update(self):
		self.tree = ElementTree.parse(os.path.abspath("decide/config.xml"))

class DefaultConfig(Config):
	HALF = "half"
	ARX_FAIR = "arx-fair"
	ARX_PRIORITY = "arx-priority"
	ARX_THROUGHPUT = "arx-priority-throughput"
	ADAPTIVE_ARX_FAIR = "a-arx-fair"

	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)

		default = self.tree.getroot().find("default")
		self.__controller = default.find("controller").text
		self.__power_init = float(default.find("power_init").text)
		self.__power_cap = float(default.find("power_cap").text)
		self.__output = default.find("output").text

	@staticmethod
	def serialize(obj):
		return {"controller": obj.__controller, "power_init": obj.__power_init, "power_cap": obj.__power_cap, "output": obj.__output}
	@property
	def controller(self):
		return self.__controller

	@property
	def power_cap(self):
		return self.__power_cap

	@property
	def power_init(self):
		return self.__power_init

	@property
	def output(self):
		return self.__output
	

class ARXConfig(Config):
	"""docstring for ARXConfig"""
	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)

		arx = self.tree.getroot().find("arx")
		self.__a = float(arx.find("a").text)
		self.__b = float(arx.find("b").text)
		self.__p = float(arx.find("p").text)
		self.__power_avg = float(arx.find("power_avg").text)
		self.__power_sd = float(arx.find("power_sd").text)
		self.__quota_avg = float(arx.find("quota_avg").text)
		self.__quota_sd = float(arx.find("quota_sd").text)
		self.__quota_min = int(arx.find("quota_min").text)

	@staticmethod
	def serialize(obj):
		return {"a": obj.__a, "b": obj.__b, "p": obj.__p, "power_avg": obj.__power_avg, 
		"quota_avg": obj.__quota_avg, "quota_sd": obj.__quota_sd, "quota_min": obj.__quota_min }

	@property
	def a(self):
		return self.__a

	@property
	def b(self):
		return self.__b

	@property
	def p(self):
		return self.__p

	@property
	def power_avg(self):
		return self.__power_avg

	@property
	def power_sd(self):
		return self.__power_sd

	@property
	def quota_avg(self):
		return self.__quota_avg

	@property
	def quota_sd(self):
		return self.__quota_sd

	@property
	def quota_min(self):
		return self.__quota_min 


class RLSConfig(Config):
	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)

		rls = self.tree.getroot().find("rls")
		self.__lambda = float(rls.find("lambda").text)
		self.__delta = int(rls.find("delta").text)

	@property
	def lmd(self):
		return self.__lambda

	@property
	def delta(self):
		return self.__delta

class PartitionerConfig(Config):
	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)

		partitioner = self.tree.getroot().find("partitioner")
		self.__quota_container_min = int(partitioner.find("quota_container_min").text)
		self.__weight_high = float(partitioner.find("weight_high").text)
		self.__weight_low = float(partitioner.find("weight_low").text)

	@property
	def quota_container_min(self):
		return self.__quota_container_min

	@property
	def weight_high(self):
		return self.__weight_high

	@property
	def weight_low(self):
		return self.__weight_low