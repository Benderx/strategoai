from distutils.core import setup, Extension

# define the extension module
s = Extension('spam', sources=['spammodule.c'])

# run the setup
setup(ext_modules=[s])
