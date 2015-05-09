from itertools import imap
from setuptools import setup, find_packages
import py

def get_requirements():
    reqs_file = "requirements.txt"
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, imap(lambda line: line.strip(), reqs_file))
            return reqs
    except IOError:
        pass
    return []

setup(
    name='galenpy',
    version=py.__version__,
    url='https://github.com/valermor/galen-api-ports',
    author='valerio morsella',
    author_email='valerio.morsella@skyscanner.net',
    package_data={'galenpy': ['service/*.jar', 'pythrift/*-remote', 'utils/*.config']},
    description='Porting of the Galen Framework API to Python',
    long_description=open('py/README.rst').read(),
    install_requires=get_requirements(),
    package_dir={'':'py'},
    packages=['galenpy', 'galenpy.utils', 'galenpy.pythrift'],
    license = 'Apache License 2.0'
)
