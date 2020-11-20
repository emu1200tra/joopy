from src.joopy import Joopy
'''
Base class for server.
'''
class Base():
    def __init__(self):
        super().__init__()
    
    def fireStart(self, apps: List[Joopy]):
        for app in apps:
            app.start_with_server(self)
    def fireStop(self, apps: List[Joopy]):
        for app in apps:
            app.ready(self)