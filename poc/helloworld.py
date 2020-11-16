from poc.src.joopy import runApp
from poc.src.joopy import get


@get("/hello")
def hello():
    return b'hello world'


@get("/goodbye")
def goodbye():
    return b'good bye'


if __name__ == '__main__':
    runApp()
