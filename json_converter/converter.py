from typing import List, Tuple, Callable
import os
import time
from ..utils import split_list, rm_suffix, rm_prefix, dedup_enter, categroy_judge
import tqdm
import json
import warnings


class ConverterBase:
    """Convert non jsonl file to jsonl"""

    def __init__(self, *args, **kwargs) -> None:
        self.kwargs = kwargs
        self.args = args

    def __call__(
        self, file_list: List[os.PathLike], output_dir: os.PathLike, mpi: int = None
    ) -> None:
        """ """
        part_id = 0
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if mpi:
            from mpi4py import MPI

            comm = MPI.COMM_WORLD
            part_num = comm.Get_size()
            part_id = comm.Get_rank()
            comm.Barrier()
            file_list = split_list(file_list, part_num, part_id)
        print(
            f"*****************{__name__} : The input files are ready.*******************"
        )
        time_id = time.strftime("%Y%m%d%H%M%S")
        output_path = os.path.join(
            output_dir, f"shiti_time_{time_id}_worker_{part_id:03d}.jsonl"
        )
        with open(output_path, "w", encoding="utf-8") as writer:
            for file_path in tqdm.tqdm(file_list, desc="dump file to jsonl"):
                print(
                    self._main_process(file_path, **self.kwargs),
                    file=writer,
                    flush=True,
                )
        print(
            f"*****************{__name__} : All the file were successfully converted!*******************"
        )

    def _main_process(
        self,
        file_path: os.PathLike,
        text_extract_fun: Callable[[str], Tuple[str, str, str, str, int]] = None,
        **dump_kwargs,
    ) -> str:
        text_extract_fun = (
            self._text_extract_model if not text_extract_fun else text_extract_fun
        )
        des, opts, ans, res, nmlc = text_extract_fun(file_path)
        try:
            prob_type = categroy_judge(des, opts, ans, nmlc)
            file_name = rm_suffix(os.path.basename(file_path))
            metadata = file_name.split("_")
            des = "Query: " + rm_prefix(des)
            ans = "Answer: " + ans

            try:
                json_line = {
                    "text": dedup_enter("\n".join([des, opts, ans])),
                    "meta": {
                        "id": metadata[0],
                        "subject": metadata[1],
                        "grade": metadata[2],
                        "about": metadata[3],
                        "resolution": res,
                        "type": prob_type,
                    },
                }
            except:
                json_line = {
                    "text": dedup_enter("\n".join([des, opts, ans])),
                    "meta": {"about": file_name, "resolution": res, "type": prob_type},
                }
            return json.dumps(json_line, **dump_kwargs)
        except Exception as exc:
            # print(exc)
            # raise Exception
            pass

    def _text_extract_model(
        self, file_path: os.PathLike
    ) -> Tuple[str, str, str, str, int]:
        """
        Arguments:
         - file_path : file path.

        Output:
         - arg[0] : description of the whole problems, if it has.
         - arg[1] : main part of the problems, for example the multiple choice or blank filling.
         - arg[2] : answers text.
         - arg[3] : resolution text for the whole problems.
         - arg[4] : the number of multiple choice. If it is 1, that means this problem is not a multiple choice.
        """
        warnings.warn(
            "This text extract function is not indentified, the programme will return a None value",
            ResourceWarning,
        )
        return None, None, None, None, None