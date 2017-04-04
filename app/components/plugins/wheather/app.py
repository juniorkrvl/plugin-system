def hello(name=''):
    print 'hello %s' % name

def return_wheater():
    wh = ['10','11','13']
    view = {'view':'core-list','parameters':{'wheather':wh}}
    return view