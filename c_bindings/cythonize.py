from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("engine_commands.pyx"),
    include_dirs=[numpy.get_include()]
)



# commmand
# python cythonize.py build_ext --inplace


# Slowdowns
# cython .\engine_commands.pyx -a