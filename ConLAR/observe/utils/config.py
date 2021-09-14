import os
from xml.etree import ElementTree

class Config:
    def __init__(self):
        self.update()

    def update(self):
        self.tree = ElementTree.parse(os.path.abspath("observe/config.xml"))

class DefaultConfig(Config):
	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)

		default = self.tree.getroot().find("default")


