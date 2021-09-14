import subprocess as sp
from execute.utils.config import CGroupConfig

class CGroupInterface:
    __config = CGroupConfig()

    @staticmethod
    def __build_path(resource, resource_file, container_id):
        cf = CGroupInterface.__config 
        return cf.path + str(resource) + "/" + \
            cf.group.replace("?CONTAINER_ID?", str(container_id)) + \
            str(resource_file)

    @staticmethod
    def set_cpu_quota(value, container_id):
        # value in %
        cpu_period = CGroupInterface.get_cpu_period(container_id)

        CGroupInterface.__set_resource("cpu", "cpu.cfs_quota_us", int(int(cpu_period) * (value / 100.0)), container_id)

    @staticmethod
    def set_memory(value, container_id):
        CGroupInterface.__set_resource("memory", "memory.limit_in_bytes", str(value) + "M", container_id)

    @staticmethod
    def get_cpu_period(container_id):
        return CGroupInterface.__get_resource("cpu", "cpu.cfs_period_us", container_id)

    @staticmethod
    def get_cpu_quota(container_id):
        return CGroupInterface.__get_resource("cpu", "cpu.cfs_quota_us", container_id)

    @staticmethod
    def __get_resource(resource, resource_file, container_id):
        path = CGroupInterface.__build_path(resource, resource_file, container_id)
        cmd = "cat " + path

        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        res, _ = proc.communicate()

        if res.strip() == "":
            raise ValueError("Path " + path + " doesn't lead to any value")

        return int(res.strip())

    @staticmethod
    def __set_resource(resource, resource_file, value, container_id):
        path = CGroupInterface.__build_path(resource, resource_file, container_id)
        cmd = "echo " + str(value) + " > " + path

        output = sp.call(["sh", "-c", cmd])
