from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
# from Cython.Build import cythonize

ext_modules =[Extension("NK_FEMeshUtils", ["*.py"])]

setup(
    name = 'NK_FEMeshUtils',
    version = '0.1',
    description = 'Python Implementation to work with FE Mesh Data',
    author = 'N. Klinke',
    author_email = 'niklas.klinke@googlemail.com',
    license = "GPL3",
    packages = ["NK_FEMeshUtils"]
)