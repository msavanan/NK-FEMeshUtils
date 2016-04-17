import FE_Mesh
import FE_MeshReader

Reader = FE_MeshReader.MeshReaders()
Mesh = Reader.readDynaMesh("Taurus_35mph.k")
