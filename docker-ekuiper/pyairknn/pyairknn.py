from ekuiper import PluginConfig
from ekuiper.runtime import plugin
from label import labelIns

if __name__ == '__main__':
    c = PluginConfig("pyairknn", {}, {},
                     {"labelImageRknn": lambda: labelIns})
    plugin.start(c)
