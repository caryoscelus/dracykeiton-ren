init -1 python:
    class UFunction(Action):
        "Like Function, but make sure to update screen"
        def __init__(self, f, *args, **kw_args):
            super(UFunction, self).__init__()
            self.f = Function(f, *args, **kw_args)
        def __call__(self):
            r = self.f.__call__()
            renpy.restart_interaction()
            return r
