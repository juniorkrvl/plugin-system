def main():
    call = {'call':{'component':'pluginmanager','method':'get_plugin_names'}}
    return {'view':'view-main', 'parameters':{'list':call}}