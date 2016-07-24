from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize('analyse.py'),
    )
setup(
    ext_modules=cythonize('pad.py'),
    )
setup(
    ext_modules=cythonize('pre_analysis.py'),
    )
