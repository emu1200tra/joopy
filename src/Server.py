'''
Base class for server.
'''
class Base():
    def __init__(self):
        super().__init__()
    
    def fireStart(self, apps):
        for app in apps:
            app.start(self)
    def fireReady(self, apps):
        for app in apps:
            app.ready(self)
    def fireStop(self, apps):
        for app in apps:
            app.stop()