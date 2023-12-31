from typing import List, Tuple, Callable
import os
import time
from ..utils import split_list, rm_suffix, rm_prefix, dedup_enter, categroy_judge
import tqdm
import json
import warnings
from ..tex_translator.hand_translator import HandTranslator as hand_translator
from ..tex_translator.tex_translator import TexTranslator as tex_translator


class ConverterBase:
    """Convert non jsonl file to jsonl"""

    def __init__(self, tmp_cache: os.PathLike, *args, **kwargs) -> None:
        self.tmp_cache = tmp_cache if tmp_cache else "/tmp/.convert_cache"
        if not os.path.exists(self.tmp_cache):
            os.mkdir(self.tmp_cache)
        # self.tmp_cache = os.path.join(self.tmp_cache, time.strftime("%Y%m%d%H%M%S"))
        self.kwargs = kwargs
        self.args = args
        if not os.path.exists(self.tmp_cache):
            os.mkdir(self.tmp_cache)
        self.suffix=time.strftime("%Y%m%d%H%M%S")
    def __call__(
        self,
        file_list: List[os.PathLike],
        output_dir: os.PathLike,
        mpi: int = None,
        id_proc: int = 0,
        suffix: str = None,
    ) -> None:
        """
        ### Arguments:
         - `mpi` : mpich based multiple processor.
         - `id_proc` : hashable index to label a single sub process.
         - `prefix` : optional prefix to name the output JSONlines file, default is time when the class initialized.
        """
        suffix = suffix if suffix else self.suffix
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if mpi:
            from mpi4py import MPI

            comm = MPI.COMM_WORLD
            part_num = comm.Get_size()
            id_proc = comm.Get_rank()
            comm.Barrier()
            file_list = split_list(file_list, part_num, id_proc)
        print(
            f"*****************{__name__} : The input files are ready.*******************"
        )
        output_path = os.path.join(
            output_dir, f"shiti_worker_{id_proc:03d}_{suffix}.jsonl"
        )
        with open(output_path, "a", encoding="utf-8") as writer:
            for file_path in tqdm.tqdm(file_list, desc="dump file to jsonl"):
                try:
                    print(
                        self._main_process(file_path, **self.kwargs),
                        file=writer,
                        flush=True,
                    )
                except KeyboardInterrupt:
                    print("debug kill")
                    break
                except Exception:
                    continue
        print(
            f"*****************{__name__} : All the file were successfully converted!*******************"
        )

    def clean(self):
        """这种函数以后考虑使用上下文实现"""
        os.system(f"rm -r {self.tmp_cache}")

    def _main_process(
        self,
        file_path: os.PathLike,
        text_extract_fun: Callable[[str], Tuple[str, str, str, str, int]] = None,
        **dump_kwargs,
    ) -> str:
        text_extract_fun = (
            self._text_extract_model if not text_extract_fun else text_extract_fun
        )
        try:
            des, opts, ans, res, nmlc = text_extract_fun(file_path)
            prob_type = categroy_judge(des, opts, ans, nmlc)
            file_name = rm_suffix(os.path.basename(file_path))
            metadata = file_name.split("_")
            des = "Query: " + rm_prefix(des)
            ans = "Answer: " + rm_prefix(ans)
            text = hand_translator()("\n".join([des, opts, ans]))
            res = hand_translator()(res)
            text = tex_translator()(text)
            res = tex_translator()(res)
            text = dedup_enter(text)
            res = dedup_enter(res)
            try:
                json_line = {
                    "text": text,
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
                    "text": text,
                    "meta": {"about": file_name, "resolution": res, "type": prob_type},
                }
            return json.dumps(json_line, **dump_kwargs)
        except:
            raise Exception

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

    # @staticmethod
    # def run(
    #     file_list: List[os.PathLike],
    #     output_dir: os.PathLike,
    #     mpi: int = None,
    #     id_proc: int = 0,
    #     prefix: str = None,
    # ):
    #     return __call__(file_list, output_dir, mpi, id_proc, prefix)
