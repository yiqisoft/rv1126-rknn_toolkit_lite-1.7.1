from detect import detectIns
from ekuiper import PluginConfig
from ekuiper.runtime import plugin

if __name__ == '__main__':
    c = PluginConfig("pyrknn", {}, {},
                     {"objectDetect": lambda: detectIns})
    plugin.start(c)