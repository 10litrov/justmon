from distutils.core import setup

setup(
    name='justmon',
    version='0.0.1',
    packages=['justmon', 'justmon.static', 'twisted.plugins'],
    url='https://github.com/10litrov/justmon',
    license='',
    author='Ivan Phrolov',
    author_email='10litrov@gmail.com',
    description='A simple python program for host monitoring',
    requires=['twisted']
)
