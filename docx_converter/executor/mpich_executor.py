from .executor import ExecutorBase


class MpichExecutor(ExecutorBase):
    '''
    Multiple processor based on mpich software.
    '''
    def __init__(self, *exec_args, **exec_kwargs) -> None:
        super().__init__(*exec_args, **exec_kwargs)

    def __call__(self, arg_call, *fn_args, **fn_kwargs):
        return super().__call__(arg_call, *fn_args, **fn_kwargs)
