# from setuptools import setup
from distutils.core import setup

setup(name='ConcretePy',
      version='0.1.1',
      description='Reinforced Concrete Design Application',
      url='https://github.com/MarioRaul/ConcretePy',
      author='Mario Freitas',
      author_email='mariofreitas.enc@gmail.com',
      license='MIT',
      packages=['C:\Python34\Lib\site-packages\ConcretePy'],
      install_requires=[
          'numpy',
          'matplotlib', 'ConcretePy'
      ],
      zip_safe=False)
