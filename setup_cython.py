from distutils.core import setup
from Cython.Build import cythonize

modules = cythonize("cNK_FEMeshUtils/*.py")

setup(
    name = 'cNK_FEMeshUtils',
    version = '0.1',
    description = 'Python Implementation to work with FE Mesh Data.',
    author = 'N. Klinke',
    author_email = 'niklas.klinke@googlemail.com',
    license = "GPL3",
    ext_modules = modules,
)
