import os
import json
import importlib


class PluginManager():

    config = None
    installed = []
    disabled = []

    def __init__(self,config):
        self.config = config
    
    def load_plugins(self):
        
        for plugin in self.config["plugins"]["installed"]:
            mod = importlib.import_module('components.plugins.'+plugin+'.app')
            module = {'name':plugin, 'instance':mod, 'path':os.path.dirname(mod.__file__)}
            self.installed.append(module)

        for instance in self.installed:
            print instance['name']

    def get_plugin(self, name):
        plugin = [x for x in self.installed if x['name'] == name][0]
        return plugin
    
    def get_plugin_names(self):
        return [x['name'] for x in self.installed]

    def call_method(self, name, method,params=[]):
        p = self.get_plugin(name)
        if p:
            inst = p['instance']
            met = getattr(inst,method)
            if len(params) > 0:
                met(*params)
            else:
                met()

    def view(self):
        view = {'view':'core-list','parameters':{'list':self.get_plugin_names()}}
        return view

if __name__ == '__main__':
    with open('../config.json') as file_config:
        config = json.load(file_config)
    
    pluginM = PluginManager(config)
    pluginM.load_plugins()
    pluginM.call_method('wheather','hello')
    pluginM.call_method('wheather','hello',['Junior'])


        
            

    
