from typing import List

from .todo import *
from .Route import Route
from .ExecutionMode import ExecutionMode
from .handler.send_char_sequence import SendCharSequence
from .handler.worker_handler import WorkerHandler
from .reified import Reified


class Pipeline:
    @staticmethod
    def compute(loader: ClassLoader, route: Route, mode: ExecutionMode, \
        executor: Executor, initializer: ContextInitializer, responseHandler: List[ResponseHandler]) -> Route.Handler:
        returnType = route.get_return_type() # Type
        _type = Reified.raw_type(returnType) # Class<?> 

        ''' Strings: '''
        # if (_type is str): # TODO: CharSequence class in javas # CharSequence.class.isAssignableFrom(type)
        return Pipeline.__next(mode, executor, Pipeline.__decorate(route, initializer, SendCharSequence(route.get_pipeline())), True)

    @staticmethod
    def __decorate(route: Route, initializer: ContextInitializer, handler: Route.Handler) -> Route.Handler:
        pipeline = handler # Handler
        # if route.isHttpHead():
            # pipeline = HeadResponseHandler(pipeline)
        if initializer is None:
            return pipeline
        return PostDispatchInitializerHandler(initializer, pipeline)

    @staticmethod
    def __next(mode: ExecutionMode, executor: Executor, handler: Route.Handler, blocking: bool) -> Route.Handler:
        if executor is None:
            if mode == ExecutionMode.WORKER:
                return WorkerHandler(handler)
            if mode == ExecutionMode.DEFAULT and blocking:
                return WorkerHandler(handler)
            return handler
        return DispatchHandler(handler, executor)