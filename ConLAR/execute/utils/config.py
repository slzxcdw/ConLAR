import os
from xml.etree import ElementTree

class Config:
    def __init__(self):
        self.update()

    def update(self):
        self.tree = ElementTree.parse(os.path.abspath("execute/config.xml"))

class CGroupConfig(Config):
    def __init__(self):
        Config.__init__(self)

        self.update()

    def update(self):
        Config.update(self)

        cgroup = self.tree.getroot().find("cgroup")
        self.__path = cgroup.find("path").text
        self.__group = cgroup.find("group").text

    @property
    def path(self):
        return self.__path

    @property
    def group(self):
        return self.__group

