# import Flask
from flask import Flask, Blueprint, render_template, url_for, render_template_string, jsonify, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import json
import requests

# pyinstaller
import os
import config as _
import importlib as importlib
from components import controller
from components.pluginmanager import PluginManager

app = Flask(__name__,template_folder='views/templates',static_folder='views/static')

app.config.from_object('flask_config')

# controller.register_components(app)

manager = PluginManager(controller.load_config())
manager.load_plugins()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/plugins")
def plugin_names():
    array = manager.get_plugin_names() 
    return json.dumps(array)

@app.route("/plugins/<name>/<method>")
def plugin(name,method):
    schema = manager.call_method(name,method)
    if schema['view']:
        schema['url'] = url_for('static',filename="elements/"+schema['view']+".html")
    return json.dumps(schema)


@app.route("/pluginmanager")
def pluginmanager():
    schema = manager.view()
    schema['url'] = ''
    if schema['view']:
        schema['url'] = url_for('static',filename="elements/" + schema['view'] + ".html")
    return json.dumps(schema)

@app.route("/resolve/<plugin>")
def resolve(plugin):
    plug = importlib.import_module('components.' + plugin)
    imports = controller.import_files(plug.main.plugin)
    content = controller.resolve_render_file(plug.main.plugin)
    template = render_template('base.html',imports=imports,content=content)

    location = url_for('core.static',filename='system-core.html')
    d = {'template' : location}
    return render_template_string(template, param=str(d))

@app.route('/call/<plugin>/<method>')
def call(plugin, method):
    url = url_for(plugin+'.'+method)
    response = requests.get(url)
    return response.text
    # json_response['url'] = url_for(plugin + '.static',filename=json_response['entry']+'.html')
    # return json.dumps(json)

@app.route('/url/<plugin>/<entry>')
def resolve_url(plugin,entry):
    return url_for(plugin+'.static',filename=entry + '.html')

# @app.route("/render/<plugin>",methods=['POST'])
# def render_view(plugin):



# resolve('core')

# import modules

# from resources.task.controller import mod_task

# plugin = importlib.import_module('plugins.task-plugin.main')

# lst = os.listdir('components')
# plugins = []
# for d in lst:
#     s = os.path.abspath('components') + os.sep + d
#     if os.path.isdir(s) and os.path.exists(s + os.sep + '__init__.py'):
#         plugins.append(d)

# for p in plugins:
#     mod = importlib.import_module('components.'+ p +'.main')
#     blueprint = mod.plugin 
#     app.register_blueprint(blueprint, url_prefix='/components/' + mod.name)
#     print mod.name

#from plugins.task_plugin import main
# from resources.foobar.controller import mod_foobar
    

# you can register other modules
#app.register_blueprint(plugin, url_prefix='/task')
# app.register_blueprint(mod_foobar)