from src.joopy import Joopy

# get: Send request to server and get data from it
# post: Send request to server with encrypted body (usually passwd or something that should be secret)
# put: Send request to server with data that would replace original data on remote
# delete: Send request to server to remove specific data
"""
MVC API
"""
class controller(Joopy):
    def __init__(self):
        super(controller, self).__init__()

    @self.get("/")
    def home():
        return b'home'

    @self.get("/hello")
    def hello():
        return b'hello world'

    @self.get("/goodbye")
    def goodbye():
        return b'good bye'
    '''
    @self.post("/login")
    def login():
        # do something with login
        return b'login process'

    @self.post("/database")
    def post_database():
        # do something with posting data
        return b'posting data'

    @self.put("/database")
    def update():
        # do something to update data in dataset
        return b'updating'

    @self.delete("/database")
    def remove():
        # remove data from database
        return b'removing'
    '''

class myApp(controller):
    def __init__(self):
        super(myApp, self).__init__()    
        self.mvc(provider=super())
        
if __name__ == '__main__':
    myApp.runApp(provider=myApp)
