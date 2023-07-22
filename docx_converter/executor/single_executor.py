from .executor import ExecutorBase
from ..utils import get_file_list
import warnings
from ..utils import SmallBatchWarning
from typing import Callable, List, Optional
import os


class SingleExecutor(ExecutorBase):
    def __call__(
        self,
        func: Callable[..., None],
        file_dir: os.PathLike,
        file_suffix: str,
        file_list: Optional[List[os.PathLike]] = None,
        **fn_kwargs
    ):
        """
        Process totally on one thread with one processor.\\
        Arguments:
         -  `func` : callable functions with no return to be called.
         - `file_dir` : the file directory.
         - `file_suffix` : the suffix specified in directory, reasuring only this format files to be processed.
         - `file_list` : files path list, this arguments will overwrite the file directory's information.
         - `**fn_kwargs` : input arguments for the callabel functions.
        """
        file_list = get_file_list(
            file_dir=file_dir, file_suffix=file_suffix, input_file_path_list=file_list
        )
        if len(file_list) < 10:
            warnings.warn(
                "The small batch of input files is deprecated", SmallBatchWarning
            )

        func(file_list, **fn_kwargs)
