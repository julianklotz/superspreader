import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="superspreader",
    version="0.2.6",
    description="Load data from spreadsheets easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julianklotz/superspreader",
    author="Julian Klotz",
    author_email="post@julianklotz.de",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="excel, spreadsheets, import, csv, tsv, openpyxl",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["openpyxl>=3"],
    extras_require={
        "dev": ["pre-commit"],
        "test": ["coverage"],
    },
    project_urls={
        "Source": "https://github.com/julianklotz/superspreader",
    },
)
