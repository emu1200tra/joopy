from poc.src import wsgi

# class joopy:
#     def __init__(self):
#         print("hello")


routers = {}


def runApp():
    wsgi.start(routers)


def get(route):
    def decorator(func):
        routers[route] = ("GET", func)
        return func
    return decorator
