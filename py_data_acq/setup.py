from setuptools import setup, find_packages


setup(
    name="py_data_acq",
    version="1.0",
    packages=find_packages(),
    scripts=[
        "runner.py",
        "can-broadcast-test.py",
        "serial-broadcast-test.py",
        "data_acq_service.py",
        "server_runner.py",
    ],
)
