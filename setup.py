# setup.py placed at root directory
from setuptools import setup
setup(
    name='demail',
    version='0.0.5',
    author='Eric Di Re',
    description='Custom package for sending emails.',
    url='https://github.com/edire/demail.git',
    python_requires='>=3.9',
    packages=['demail'],
    install_requires=['yagmail', 'sendgrid']
)