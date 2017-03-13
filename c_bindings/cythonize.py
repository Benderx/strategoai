from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy


extensions = [Extension(
                "engine_commands",
                sources=["engine_commands.pyx"],
                extra_compile_args=["-fopenmp"],
                extra_link_args=["/openmp"]
            )]


setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()]
)



# commmand
# python cythonize.py build_ext --inplace


# Slowdowns
# cython .\engine_commands.pyx -a