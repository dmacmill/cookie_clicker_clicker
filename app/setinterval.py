# from contextlib import suppress

# import asyncio
# import time

# Also could have used this, and reworked the app to handle async:

# The current threading way has it's own issues, but it's simple enough, and I don't need it 
# to be complicated.

# async def setInterval(func, sec, *args, **kwargs):
#     while True:
#         await asyncio.sleep(sec)
#         await func(*args, **kwargs)


# class SetInterval:
#     """
#     A class that mimics the JavaScript setInterval method for Python, using threading.

#     From https://blog.timhartmann.de/2024/05/01/python-setinterval/

#     Attributes:
#         func (Callable): The function to be executed repeatedly.
#         sec (float): Time interval between function executions.
#         run_now (bool): immediately execute
#         args (list, optional): Positional arguments for the function.
#         kwargs (dict, optional): Keyword arguments for the function.
#     """
#     def __init__(self, func, sec, run_now=False, args=None, kwargs=None):
#         self.func = func
#         self.sec = sec
#         self.args = args if args is not None else []
#         self.kwargs = kwargs if kwargs is not None else {}
#         self.thread = None
#         self.start(run_now)

#     def start(self, run_now=False):
#         """
#         Starts or restarts the timer for function execution.

#         Args:
#             run_now (bool): If True, the function is executed immediately before starting the timer.
#         """
#         def func_wrapper():
#             self.func(*self.args, **self.kwargs)
#             self.start() # makes a new thread every run, bad.

#         if run_now:
#             self.func(*self.args, **self.kwargs)

#         self.thread = Timer(self.sec, func_wrapper)
#         self.thread.start()

#     def cancel(self):
#         """
#         Stops the timer, effectively ending repeated function execution.
#         """
#         if self.thread is not None:
#             self.thread.cancel()
#             self.thread = None