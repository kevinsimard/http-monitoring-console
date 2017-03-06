from setuptools import find_packages, setup

setup(
    name='HttpMonitoring',
    version='0.1.0',
    author='Kevin Simard',
    author_email='kev.simard@gmail.com',
    packages=find_packages(),
    scripts=[
        'bin/http-generator',
        'bin/http-monitor'
    ],
    requires=[
        'apache_log_parser',
        'faker',
        'pypubsub',
        'pytz',
        'typing'
    ]
)
