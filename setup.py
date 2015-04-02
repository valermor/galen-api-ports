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
    name='galenapi',
    version='0.1.0',
    url='https://github.com/valermor/galen-api-ports',
    author='valerio morsella',
    author_email='valerio.morsella@skyscanner.net',
    py_modules=['galenapi'],
    package_data={'galenapi': ['service/*.jar'], '': ['*.sh'], '': ['*.config']},
    description='Porting of the Galen Framework API to Python',
    long_description=open('README').read(),
    install_requires=get_requirements(),
    package_dir={'galenapi':'py/galenapi'},
    packages=['galenapi'],
)
