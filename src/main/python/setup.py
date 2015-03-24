from itertools import imap
from setuptools import setup, find_packages

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
    name='galen-py',
    version='0.1.0',
    author='valerio morsella',
    author_email='valerio.morsella@skyscanner.net',
    packages=find_packages(exclude=["test*"]),
    description='Porting of the Galen Framework API to python.',
    long_description=open('README').read(),
    install_requires=get_requirements(),
)
