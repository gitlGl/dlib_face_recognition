from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'test',ext_modules = cythonize('conver.pyx',compiler_directives={'language_level' : "3"}))
