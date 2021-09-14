from execute.cgroup_interface import CGroupInterface
from execute.docker_interface import DockerInterface
import time
import subprocess as sp
class ResourcesSource:

    def __init__(self):
        pass

    @staticmethod
    def get_resources():        
        containers = DockerInterface.ps()

        for container in containers:
            try:
                print "container " + container["id"] + " detected"
                cmd = "docker stats --no-stream {0} |awk 'NR==2 {{print $3}}'".format(container["id"])
                proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
                res, _ = proc.communicate()
                if res.strip() == "":
                    raise ValueError("command doesn't lead to any value")
                print res
                path = "/home/cdw/log/"
                full_path = path + container["id"] + ".txt"
		print(full_path)
                file = open(full_path,"a")
                msg = time.ctime() + " " + res
                file.write(msg)
		file.flush()
		print msg
                path1 = "/home/cdw/log/"
                full_path1 = path1 + "full" + container["id"] + ".txt"
                file1 = open(full_path1,"a")
                msg = time.ctime() + " " + res
                file1.write(msg)
		file1.flush()
                container["cpu_period"] = CGroupInterface.get_cpu_period(container["id"])
                container["cpu_quota"] = CGroupInterface.get_cpu_quota(container["id"])

                if container["cpu_quota"] == -1:
                    container["cpu_quota"] = container["cpu_period"] * 2

            except ValueError:
                print "Container " + str(container["id"]) + " not found"
                containers.remove(container)

        if len(containers) == 0:
            raise RuntimeError("No more container available")

        return containers

