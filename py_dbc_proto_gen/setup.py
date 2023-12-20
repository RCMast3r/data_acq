from setuptools import setup, find_packages


setup(
    name="dbc_proto_gen",
    version="1.0",
    packages=find_packages(),
    scripts=['ht_dbc_proto_creator.py']
)