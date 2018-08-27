# -*- encoding: utf-8 -*-
from release.init import Init


class Configer():

    def __init__(self):
        self.__init__ = Init()
        self.__config_params__ = self.__init__.get_params()
        self.__config_params__["server_hosts"] = {
            server: self.__host_ref__(self.__config_params__["hosts"], self.__split_list__(hosts))
            for server, hosts in self.__config_params__["server_hosts"].items()
        }

    def get_params(self, key, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return self.__config_params__[key]
        else:
            return self.__config_params__[key][args[0]]

    def __split_list__(self, str):
        return str.split(',')

    def __host_ref__(self, dict, lists):
        params = []
        try:
            for list in lists:
                params.append(dict[list])
        except Exception as e:
            pass
        return params



if __name__ == "__main__":
    configer = Configer()
    params = configer.get_params("path_local_target")
    print(params)
