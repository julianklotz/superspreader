from setuptools import find_packages, setup

setup(
    name="superspeader",
    version="0.0.1",
    packages=find_packages(),
    test_suite="tests.test_suite",
    url="",
    license="MIT",
    author="Bernhard Thull",
    author_email="post@julianklotz.de",
    description="Populate Django models from spreadsheets",
    install_requires=["openpyxl"],
)
