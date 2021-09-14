import os
from xml.etree import ElementTree

class Config:
	def __init__(self):
		self.update()

	def update(self):
		self.tree = ElementTree.parse(os.path.abspath("predict/config.xml"))

class DefaultConfig(Config):

	def __init__(self):
		Config.__init__(self)
		self.update()

	def update(self):
		Config.update(self)
		default = self.tree.getroot().find("default")
		self.full_path = default.find("full_path")
		self.train = default.find("train")
		self.predict = default.find("predict")
		self.output = default.find("output")


