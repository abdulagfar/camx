from setuptools import setup
setup(
    name='camx',
    version='1.2.0',
    entry_points={
        'console_scripts': [
            'camx=camx:run'
        ]
    }
)