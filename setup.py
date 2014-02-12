from setuptools import setup

setup(
    name='repeat',
    py_modules=['repeat'],
    entry_points={
        'console_scripts': [
            'repeat = repeat:main',
        ],
    },
)
