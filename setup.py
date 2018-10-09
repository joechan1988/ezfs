from setuptools import setup

setup(
    name='ezfs',
    version='1.0',
    packages=['ezfs'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        ezfs=ezfs.main:cli
    ''',
)
