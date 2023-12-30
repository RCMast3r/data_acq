from setuptools import setup, find_packages


setup(
    name="py_data_acq",
    version="1.0",
    packages=find_packages(),
    scripts=['test.py', 'broadcast-test.py']
)