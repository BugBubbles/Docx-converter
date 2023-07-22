class ExecutorBase:
    def __init__(self, *exec_args, **exec_kwargs) -> None:
        self.exec_args = exec_args
        self.exec_kwargs = exec_kwargs

    def __call__(self, arg_call, *fn_args, **fn_kwargs):
        raise NotImplementedError
