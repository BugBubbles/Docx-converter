from docx_converter.executor.single_executor import SingleExecutor as executor
from docx_converter.json_converter import MdConverter as md_converter
from docx_converter.json_converter import HtmlConverter as html_converter
from docx_converter.json_converter import DocxConverter as docx_converter
import argparse


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
    args = parse.parse_args()
    return args


if __name__ == "__main__":
    converter = {"docx": docx_converter, "md": md_converter, "html": html_converter}
    args = get_args()
    suffix = args.suffix
    worker = executor()
    worker(
        converter[suffix](ensure_ascii=False, tmp_cache=args.cache_dir),
        file_suffix=suffix,
        file_dir=args.file_dir,
        # fn_kwargs :
        mpi=args.mpi,
        output_dir=args.output_dir,
    )
