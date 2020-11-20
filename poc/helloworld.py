from src.joopy import runApp
from src.joopy import get

@get("/")
def home():
    return b'home'

@get("/hello")
def hello():
    return b'hello world'


@get("/goodbye")
def goodbye():
    return b'good bye'


if __name__ == '__main__':
    runApp()
