from .executor import ExecutorBase
from ..utils import get_file_list
import warnings
from ..utils import SmallBatchWarning
from typing import Callable, List


class SingleExecutor(ExecutorBase):
    def __call__(
        self, func: Callable[[List[str], str, int], None], *fn_args, **fn_kwargs
    ):
        input_args = self.get_args
        file_dir, output_dir, mpi = (
            input_args.file_dir,
            input_args.output_dir,
            input_args.mpi,
        )
        assert file_dir != None
        assert output_dir != None
        assert fn_kwargs["file_suffix"] != None
        file_suffix = fn_kwargs.pop("file_suffix")
        file_list = get_file_list(
            file_dir=file_dir,
            file_suffix=file_suffix,
        )
        if len(file_list) < 10:
            warnings.warn(
                "The small batch of input files is deprecated", SmallBatchWarning
            )

        func(file_list, output_dir, mpi=mpi)
