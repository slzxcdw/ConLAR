import os
from xml.etree import ElementTree

class Config:
    def __init__(self):
        self.update()

    def update(self):
        self.tree = ElementTree.parse(os.path.abspath("commons/config.xml"))

class MachineConfig:
    def __init__(self):
        self.cores = self.__get_cpu()
        self.memory = self.__get_memory()
        
    # return memory in bytes
    @staticmethod
    def __get_memory():
        import os
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")

    # return number of cores
    @staticmethod
    def __get_cpu():
        import multiprocessing
        return multiprocessing.cpu_count()

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

