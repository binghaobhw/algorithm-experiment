#!/usr/bin/env python
# coding: utf-8
import time


class Timer(object):
    def __init__(self):
        self.time_ = 0.
        self.start_ = 0.

    def reset(self):
        self.time_ = 0.
        self.start_ = 0.

    def start(self):
        self.start_ = time.clock()

    def end(self):
        self.time_ += time.clock() - self.start_


def timing(timer):
    """Decorator for timing.

    Example:
    timer = Timer()
    @timing(timer)
    def foo():
        pass

    :param timer:
    """

    def real_timing(function):
        def advice(*args, **kwargs):
            timer.start()
            result = function(*args, **kwargs)
            timer.end()
            return result
        return advice
    return real_timing
