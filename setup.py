from distutils.core import setup
from Cython.Build import cythonize
#python setup.py build_ext --inplace
setup(name = 'test',ext_modules = cythonize('conver.pyx',compiler_directives={'language_level' : "3"}))
