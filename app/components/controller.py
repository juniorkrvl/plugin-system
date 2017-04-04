import os
import importlib
import json
from flask import url_for
import codecs

def register_components(app):
    lst = os.listdir('components')
    plugins = []
    for d in lst:
        s = os.path.abspath('components') + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + '__init__.py'):
            plugins.append(d)

    for p in plugins:
        mod = importlib.import_module('components.'+ p +'.main')
        blueprint = mod.plugin 
        app.register_blueprint(blueprint, url_prefix='/components/' + mod.name)
        print mod.name

def register_plugins(app):
    lst = os.listdir('components')
    plugins = []
    for d in lst:
        s = os.path.abspath('components') + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + '__init__.py'):
            plugins.append(d)

    for p in plugins:
        mod = importlib.import_module('components.'+ p +'.main')
        blueprint = mod.plugin 
        app.register_blueprint(blueprint, url_prefix='/components/' + mod.name)
        print mod.name

def load_config(plugin):
    path = plugin.root_path
    with open(os.path.join(path,'config.json')) as f:
        config = json.load(f)
    return config


def import_files(plugin):
    config = load_config(plugin)  
    imports = config['imports']
    
    family = config['family']
    name = config['name']
    url = ''

    # List current plugin elements to import 
    lst = os.listdir(plugin.static_folder)
    for e in lst:
        url += resolve_url_imports(family, name, e)

    # Then import dependencies packs
    for i in imports:
        array = i.split('.')
        if array[0] == 'base':
            url += resolve_url_imports('base','base',array[1])
        else:
            plug = importlib.import_module(array[0] + '.' + array[1])
            url += import_files(plug.main.plugin)

    return url


def resolve_render_file(plugin):
    config = load_config(plugin)
    with codecs.open(os.path.join(plugin.root_path,'templates',config['render']), 'r') as content_file:
        content = content_file.read()
    return content


def resolve_url_imports(type_from, import_from, file_from):
    if type_from == 'base':
        print 'static.'+file_from 
        url = url_for('static',filename= file_from + '.html')
    else:
        print import_from + '.static.' + file_from
        url = url_for(import_from + '.static',filename= file_from)
        # url = '../' + type_from + '/' + import_from + '/templates/elements/' + file_from + '.html'

    return '<link rel="import" href="' + url + '">\n'  

def load_config():
    with open('config.json','r') as file_config:
        config = json.load(file_config)
    return config

