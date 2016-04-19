import NK_FEMeshUtils

import time

start_time = time.time()
Reader = NK_FEMeshUtils.MeshReaders()
Mesh = Reader.readDynaMesh("../Taurus_35mph.k")
print("--- %s seconds ---" % (time.time() - start_time))
Mesh.InitAllObj()
print "Mesh.getMassByPartID()
print("--- %s seconds ---" % (time.time() - start_time))
