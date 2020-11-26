from src.joopy import Joopy

@Joopy.get("/")
def home():
    return b'home'

@Joopy.get("/hello")
def hello():
    return b'hello world'


@Joopy.get("/goodbye")
def goodbye():
    return b'good bye'


if __name__ == '__main__':
    Joopy.runApp()
