import sys

from setuptools import setup


# Required packages.  argparse was introduced into the standard library
# in Python 2.7; mock was introduced in Python 3.3.
required_packages = ["six"]
if sys.version_info < (2, 7):
    required_packages.append("argparse")
    required_packages.append("unittest")
if sys.version_info < (3, 3):
    required_packages.append("mock")


setup(
    name='repeat',
    version='0.1.0',
    author="Mark Dickinson",
    author_email="dickinsm@gmail.com",
    url="https://github.com/mdickinson/repeat",
    license="Apache license",
    description=(
        "Repeat a command indefinitely or for a fixed number of iterations"),
    py_modules=['repeat'],
    platforms=["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    entry_points={
        'console_scripts': [
            'repeat = repeat:main',
        ],
    },
    install_requires=required_packages,
)
