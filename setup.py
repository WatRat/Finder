from setuptools import setup

setup(
   name='finder',
   version='1',
   description='This python script is designed to easily find and process many files',
   author='Bohdan Belskiy',
   author_email='bogdanbelskiylntu@gmail.com',
   packages=['finder'],
   install_requires=['progress'],
   entry_points={
      'console_scripts': ['Finder = finder.Finder:run'],
   }
)
