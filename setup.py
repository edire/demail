# setup.py placed at root directory
from setuptools import setup
setup(
    name='my-email-edire',
    version='0.0.1',
    author='Eric Di Re',
    description='Custom package for sending emails.',
    url='https://github.com/edire/my_email.git',
    python_requires='>=3.6',
    packages=['my_email'],
    install_requires=['yagmail']
)