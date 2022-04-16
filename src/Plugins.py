import os,sys
class Plugins():
    def __init__(self,path):
        self.path = path#path
        sys.path.append(self.path)#加入查找路径
        self.controls_class = {} 
        self.load_plugins()   
    def load_plugins(self):
        for file_name in os.listdir(self.path):
            if not file_name.endswith(".py") or file_name.startswith("_"):
                continue
            plugin_name=os.path.splitext(file_name)[0]
            plugin = __import__(plugin_name)
            clazz = plugin.get_plugin_class()
            self.controls_class[clazz.label]=clazz
        return self.controls_class
