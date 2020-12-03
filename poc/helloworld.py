from src.joopy import Joopy

# get: Send request to server and get data from it
# post: Send request to server with encrypted body (usually passwd or something that should be secret)
# put: Send request to server with data that would replace original data on remote
# delete: Send request to server to remove specific data

class myApp(Joopy):

    def __init__(self):
        super(myApp, self).__init__()

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
    @Joopy.post("/login")
    def login():
        # do something with login
        return b'login process'

    @Joopy.post("/database")
    def post_database():
        # do something with posting data
        return b'posting data'

    @Joopy.put("/database")
    def update():
        # do something to update data in dataset
        return b'updating'

    @Joopy.delete("/database")
    def remove():
        # remove data from database
        return b'removing'
'''
if __name__ == '__main__':
    myApp.runApp(provider=myApp)
