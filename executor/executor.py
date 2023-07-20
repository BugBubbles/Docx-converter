import argparse
from typing import Callable
from typing import Callable, Any


class ExecutorBase:
    def __init__(self, *exec_args, **exec_kwargs) -> None:
        self.exec_args = exec_args
        self.exec_kwargs = exec_kwargs

    @property
    def get_args(self) -> argparse.Namespace:
        parse = argparse.ArgumentParser()
        parse.add_argument("--file_dir", "-d", type=str)
        parse.add_argument("--output_dir", "-o", type=str)
        parse.add_argument("--mpi", "-m", type=int, default=None)
        args = parse.parse_args()
        return args

    def __call__(self, func: Callable[[Any], None], *fn_args, **fn_kwargs):
        raise NotImplementedError


if __name__ == "__main__":
    print(ExecutorBase().get_args)
