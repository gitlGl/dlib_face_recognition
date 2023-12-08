import os,importlib
class Plugins():
    def __init__(self):
        self.controls_class = {} 
        self.load_plugins()   
    def load_plugins(self):
        for file_name in os.listdir("src/plugins"):
            if not file_name.endswith(".py") or file_name.startswith("_"):
                continue
            plugin_name=os.path.splitext(file_name)[0]
            #仅支持xxx.xxx.module_name方式导入，
            #from .xxx import xxx
            #import .xxx.xxx错误使用方法
            plugin = importlib.import_module("src.plugins." +plugin_name)
            clazz = plugin.get_plugin_class()
            self.controls_class[clazz.label]=clazz
        return self.controls_class
