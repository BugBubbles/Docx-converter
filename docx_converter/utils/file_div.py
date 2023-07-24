import os
from typing import List, Any, Optional
import tqdm
import itertools


def _get_balanced_part_nums(total, part_size):
    base = int(total / part_size)
    remainder = total % part_size
    return [base + int(i < remainder) for i in range(part_size)]


def _balanced_ranges(total, part_size):
    balanced_part_nums = _get_balanced_part_nums(total, part_size)
    ranges = []
    start = 0
    for part_num in balanced_part_nums:
        end = start + part_num
        ranges.append((start, end))
        start = end
    return ranges


def split_list(file_list: List[Any], n: int, i: int) -> List[Any]:
    """
    with the total `n` nodes worker setting, return the distributed files for worker indexing at `i` .
    """
    ranges = _balanced_ranges(len(file_list), n)
    start, end = ranges[i]
    return file_list[start:end]


def get_file_list(
    file_dir: os.PathLike, file_suffix: str, input_file_path_list: Optional[str] = None
) -> List[os.PathLike]:
    """
    Arguments:
     - `file_dir` : 包含全部文件的大目录
     - `input_file_path_list` : 全部文件的路径，按逗号分隔
     - `file_suffix` : 后缀名
    """
    file_list = []
    if input_file_path_list == None:
        for f_dir, _, f_list in tqdm.tqdm(
            os.walk(file_dir), desc="fetch file path", unit="it"
        ):
            for f in f_list:
                if f.endswith(file_suffix):
                    file_list.append(os.path.join(f_dir, f))
    else:
        for f in input_file_path_list.split(","):
            if f.endswith(file_suffix):
                file_list.append(f)
    return file_list


def get_file_list_stream(
    file_dir: os.PathLike,
    file_suffix: str,
    input_file_path_list: Optional[List[str]] = None,
):
    """
    scan the whole file by a streaming process to save computer resource.
    Arguments:
     - `file_dir` : 包含全部文件的大目录
     - `input_file_path_list` : 全部文件的路径，按逗号分隔
     - `file_suffix` : 后缀名
    """
    if input_file_path_list == None:
        for f_dir, _, f_list in tqdm.tqdm(
            os.walk(file_dir), desc="fetch file path", unit="it"
        ):
            for f in f_list:
                if f.endswith(file_suffix):
                    yield os.path.join(f_dir, f)
    else:
        for sub_file in input_file_path_list:
            yield from get_file_list_stream(sub_file, file_suffix)


def get_file_list_stream_batch(
    file_dir: os.PathLike,
    file_suffix: str,
    input_file_path_list: Optional[List[str]] = None,
    batch_size: Optional[int] = 300,
):
    """
    scan the whole file by a streaming process to save computer resource, yield batches by customized size.
    Arguments:
     - `file_dir` : 包含全部文件的大目录
     - `input_file_path_list` : 全部文件的路径，按逗号分隔
     - `file_suffix` : 后缀名
     - `batch_size` : the customizable batch size for user.
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least one")
    it = iter(get_file_list_stream(file_dir, file_suffix, input_file_path_list))
    while batch := tuple(itertools.islice(it, batch_size)):
        yield batch


if __name__ == "__main__":
    test_dir = "/workspace/docx2md/docx_converter"
    for lines in get_file_list_stream_batch(test_dir, ".py",batch_size=10):
        print(lines)
