from docx_converter.executor.single_executor import SingleExecutor as work_run
from docx_converter.json_converter import MdConverter as md_converter
from docx_converter.json_converter import HtmlConverter as html_converter
from docx_converter.json_converter import DocxConverter as docx_converter

if __name__ == "__main__":
    converter = {"docx": docx_converter, "md": md_converter, "html": html_converter}
    suffix = "docx"
    work_run()(
        converter[suffix](ensure_ascii=False, tmp_cache="/workspace/tmp"),
        file_suffix=suffix,
    )
    # work_run()(
    #     converter[suffix],
    #     ensure_ascii=False,
    #     tmp_cache="/workspace/tmp",
    #     file_suffix=suffix,
    # )
