import setuptools

setuptools.setup(
    name="docx_converter",
    version="1.4.0",
    author="Tschen Boffee",
    include_package_data=True,
    packages=setuptools.find_packages(where='./docx_converter'),
    description="A small tool for converting math formular included docx file into formatted jsonlines",
)
