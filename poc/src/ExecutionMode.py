from enum import Enum

class ExecutionMode(Enum):
    # Execute route handler in the event loop thread (non-blocking). Handler must never block.
    EVENT_LOOP = "EVENT_LOOP"
    
    # Execute handler in a worker/io thread (blocking). Handler is allowed to block.
    WORKER = "WORKER"

    """
    * Default execution mode.
    *
    * Automatically choose between {@link ExecutionMode#EVENT_LOOP} and {@link ExecutionMode#WORKER}.
    *
    * If route handler returns a `reactive` type, then Jooby run the route handler in the event-loop
    * thread. Otherwise, run the handler in the worker thread.
    *
    * A reactive type is one of:
    *
    * - {@link java.util.concurrent.CompletableFuture}.
    * - A reactive stream Publisher
    * - Rx types: Observable, Flowable, Single, Maybe, etc..
    * - Reactor types: Flux and Mono.
    """
    DEFAULT = "DEFAULT"