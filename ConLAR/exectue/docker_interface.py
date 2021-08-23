class DockerInterface:
    def __init__(self):
        pass

    @staticmethod
    def run(image, background=True, cpu_quota=None):
        cmd = "docker run "
        if background is True:
            cmd += "-d "
        else:
            cmd += "--rm=true "

        if cpu_quota is not None:
            cmd += "--cpu-quota="+str(cpu_quota) + " "
        cmd += str(image)

        return DockerInterface.__cmd__(cmd).strip()

    @staticmethod
    def stop(container_id):
        cmd_stop = "docker stop " + str(container_id)
        cmd_rm = "docker rm " + str(container_id)

        DockerInterface.__cmd__(cmd_stop)
        DockerInterface.__cmd__(cmd_rm)

    @staticmethod
    def kill(container_id):
        cmd_kill = "docker kill " + str(container_id)
        cmd_rm = "docker rm " + str(container_id)

        DockerInterface.__cmd__(cmd_kill)
        DockerInterface.__cmd__(cmd_rm)

    @staticmethod
    def ps():
        cmd_ps = "docker ps --no-trunc"

        output = DockerInterface.__cmd__(cmd_ps)

        result = []
        lines = output.split("\n")
        i = 0
        for line in lines:
            record = {}
            if i == 0:
                i += 1
            else:
                if line != "":
                    elements = line.split(" ")
                    j = 0
                    for element in elements:
                        if element != "":
                            if j == 0:
                                record["id"] = element
                                j += 1
                            elif j == 1:
                                record["image"] = element
                                break

                    record["command"] = line.split("\"")[1]

                    result.append(record)
        return result

    @staticmethod
    def __cmd__(cmd):
        import subprocess as sp

        proc = sp.Popen(["sh", "-c", cmd], stdout=sp.PIPE)
        output, _ = proc.communicate()

        if proc.returncode is not 0:
            raise NameError
        return output