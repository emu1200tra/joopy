# Joopy

Joopy is a web framework for python built on WSGI server.

## Introduction
Joopy is re-enginnered from a Java-based web framework called [Jooby](https://jooby.io/) ([2.9.1](https://github.com/jooby-project/jooby/releases/tag/v2.9.1) version). The suffix "by" is replaced by "py" due to **py**thon.

Similarity, Joopy supports two ways to set routes: 
- Script API
- MVC API

### Hello World Example
In the following examples, we set HTTP GET method for the URL "/" and return the string "hello world" to user.

#### Script API
```python
from joopy.src.joopy import Joopy

class myApp(Joopy):
    def __init__(self):
        super(myApp, self).__init__()
        self.get("/", lambda ctx: "hello world")

if __name__ == "__main__":
    myApp.runApp(provider=myApp)
```
The Script API uses the lambda function to define routes.


#### MVC API
```python
from joopy.src.joopy import Joopy

class Controller(Joopy):
    def __init__(self):
        super(Controller, self).__init__()

        @self.get("/")
        def home(ctx):
            return "hello world"

class myApp(Controller):
    def __init__(self):
        super(myApp, self).__init__()    
        self.mvc(router=super())
        
if __name__ == "__main__":
    myApp.runApp(provider=myApp)
```
The MVC API uses the decorator to define routes.


## How to Use
The application in Joopy can have
- One or more routes
- Collection of operator over routes

### Route
A Route consists of three part:
1. HTTP method, such as GET, POST, etc
2. Path pattern, such as "/", "/foo", etc
3. Handler function

For example, 
```python
self.get("/", lambda ctx: "home")
```
We use `self.get()` for HTTP GET method. The Path pattern is define as "/". The Handler function is `lambda ctx: "home"`.

### Handler
Application logic goes inside a handler. A handler is a function that accepts a context object and produces a result.

For example, 
```python
self.get("/", lambda ctx: "home")
self.get("/hello", lambda ctx: "hello world")
self.get("/goodbye", lambda ctx: "good bye")
```
1. GET / ⇒ home
2. GET /hello ⇒ hello world
3. GET /goodbye ⇒ good bye

### Static Files
Static files such as HTML files can be the result of a handler.

For example, 
```python
from joopy.src.joopy import Joopy

class myApp(Joopy):
    def __init__(self):
        super(myApp, self).__init__()
        
        def demo_app(ctx):
            data = self.prepare_html("./demo.html")
            ctx.set_header("text/html")
            return data

        self.get("/demo", lambda ctx: demo_app(ctx))
    
    def prepare_html(self, path):
        file = open(path)
        lines = file.read()
        file.close()
        return lines

if __name__ == "__main__":
    myApp.runApp(provider=myApp)
```
GET /demo ⇒ ./demo.html

### Error Handler
If there is no handler for a request, Joopy produces a 404 response.
```
404 Not Found
```

### Decorator
Cross cutting concerns such as response modification, verification, security, tracing, etc. is available via Route.Decorator. A decorator takes the next handler in the pipeline and produces a new handler.

For example, to modify the response, we can
```python
from joopy.src.joopy import Joopy

class myApp(Joopy):
    def __init__(self):
        super(myApp, self).__init__()
        self.decorator(lambda _next: lambda ctx: _next.apply(ctx) + " decorator")
        self.get("/", lambda ctx: "home")
```
The expected response for URL "/" is "home decorator".

Another example is to compute the latency of response.
```python
import time
from joopy.src.joopy import Joopy

class myApp(Joopy):
    def __init__(self):
        super(myApp, self).__init__()
        
        def compute_latency(_next):
            def handler(ctx):
                t1 = time.time() # 1
                response = _next.apply(ctx) # 2
                t2 = time.time()
                print("latency = {:.2f} sec".format(t2-t1)) #3
                return response # 4
            return handler
        
        self.decorator(compute_latency)
        self.get("/", lambda ctx: "decorator")

if __name__ == "__main__":
    myApp.runApp(provider=myApp)
```
1. Saves start time
2. Proceed with execution
3. Compute and print latency
4. Returns a response

## One More Thing
If you like this project, please don't hestitate to star it. Thanks! :satisfied:   