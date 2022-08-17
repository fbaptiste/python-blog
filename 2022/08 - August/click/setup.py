from setuptools import setup

setup(
    name="my-super-duper-cli",
    version="0.1.0",
    py_modules=["main"],
    install_requires=["click", "tabulate"],
    entry_points={"console_scripts": ["cli = main:main_cli"]},
)
