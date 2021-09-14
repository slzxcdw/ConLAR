import os
from xml.etree import ElementTree

class Config:
    def __init__(self):
        self.update()

    def update(self):
        self.tree = ElementTree.parse(os.path.abspath("allocate/config.xml"))

class DefaultConfig(Config):
	def __init__(self):
		Config.__init__(self)

		self.update()

	def update(self):
		Config.update(self)
		default = self.tree.getroot().find("default")
		self.cur_response = default.find("cur_response").text
		self.thre_response = (int)(default.find("thre_response").text)
                self.vio_path = default.find("vio_path").text
                self.predict_path = default.find("predict_path").text
                self.name = default.find("container_name").text
                self.cfg = default.find("cfg").text
