from compat import *
import renpy
import curry

class UFunction(renpy.ui.Action):
    "Like Function, but make sure to update screen"
    def __init__(self, f, *args, **kw_args):
        super(UFunction, self).__init__()
        self.f = curry.curry(f)(*args, **kw_args)
    def __call__(self):
        r = self.f.__call__()
        renpy.exports.restart_interaction()
        return r
