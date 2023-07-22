from docx_converter.executor.single_executor import SingleExecutor as single_executor
from docx_converter.executor.multiple_executor import MultipleExecutor as multi_executor
from docx_converter.json_converter import MdConverter as md_converter
from docx_converter.json_converter import HtmlConverter as html_converter
from docx_converter.json_converter import DocxConverter as docx_converter
import argparse
from docx_converter.utils import get_file_list
import warnings


def get_args() -> argparse.Namespace:
    parse = argparse.ArgumentParser()
    parse.add_argument("--file_dir", "-f", type=str)
    parse.add_argument("--output_dir", "-o", type=str)
    parse.add_argument(
        "--mpi",
        "-m",
        type=int,
        default=None,
        help="multiprocessing method used to process parallelly in different nodes by mpich tools",
    )
    parse.add_argument(
        "--cache_dir",
        "-c",
        type=str,
        help="Where cache files to be stored in and after the whole process they will be removed.",
    )
    parse.add_argument(
        "--suffix",
        "-s",
        type=str,
        default="docx",
        help="The specific files format suffix to be processed",
    )
    parse.add_argument(
        "--multiple_enable",
        "-me",
        action="store_true",
        help="Enable a multiple processing programme.",
    )
    parse.add_argument(
        "--num_proc",
        "-np",
        type=int,
        default=10,
        help="The number of consumer processor coresponded to a single producer.",
    )
    parse.add_argument(
        "--max_size",
        "-ms",
        type=int,
        default=300,
        help="The number of cache for multiple processing programme.",
    )
    args = parse.parse_args()
    return args


if __name__ == "__main__":
    converter = {"docx": docx_converter, "md": md_converter, "html": html_converter}
    args = get_args()
    try:
        assert args.file_dir and args.output_dir
    except:
        raise AttributeError(
            "No file_dir or output_dir is specified. Please check your input command line for '-f' and '-o' arguments."
        )
    suffix = args.suffix
    if not args.multiple_enable:
        worker = single_executor()
        worker(
            converter[suffix](ensure_ascii=False, tmp_cache=args.cache_dir),
            file_suffix=suffix,
            file_dir=args.file_dir,
            # fn_kwargs :
            mpi=args.mpi,
            output_dir=args.output_dir,
        )
    else:
        try:
            assert args.num_proc and args.max_size
        except:
            warnings.warn(
                "No num_pro or max_size arguments is found, using the default value",
                DeprecationWarning,
            )
        worker = multi_executor(rate=args.num_proc, max_size=args.max_size)
        worker.load_consumer(get_file_list, file_suffix=suffix, file_dir=args.file_dir)
        # 此处消费者函数可以省略输入文件，多进程管理器内部进行装载
        worker.load_consumer(
            converter[suffix](ensure_ascii=False, tmp_cache=args.cache_dir),
            mpi=args.mpi,
            output_dir=args.output_dir,
        )
        # run it
        worker()
