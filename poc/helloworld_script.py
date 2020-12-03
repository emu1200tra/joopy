from src.joopy import Joopy

# get: Send request to server and get data from it
# post: Send request to server with encrypted body (usually passwd or something that should be secret)
# put: Send request to server with data that would replace original data on remote
# delete: Send request to server to remove specific data

class myApp(Joopy):
"""
Script API
"""
    def __init__(self):
        super(myApp, self).__init__()    

        self.get_script("/", lambda: b'home')

        self.get_script("/hello", lambda: b'hello world')

        self.get_script("/goodbye", lambda: b'good bye')

        '''
        post_script("/login", lambda x: b'login process')

        post_script("/database", lambda x: b'posting data')

        put_script("/database", lambda x: b'updating')

        delete_script("/database", lambda x: b'removing')
        '''
if __name__ == '__main__':
    myApp.runApp(provider=myApp)
