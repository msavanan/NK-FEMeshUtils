import NK_FEMeshUtils

import time

start_time = time.time()
Reader = NK_FEMeshUtils.MeshReaders()
Mesh = Reader.readDynaMesh("../Taurus_35mph.k")
print "Reader Done: {0}".format(time.time() - start_time)
start_time = time.time()

Mesh.InitAllObj()
print "InitAllObj Done: {0}".format(time.time() - start_time)
start_time = time.time()

for PartID,PartObj in Mesh.getPartlistObj().iteritems():
    print "PartId: {0}, Mass: {1}".format(PartID,PartObj.getPartMass())
    
print "PrintMasses Done: {0}".format(time.time() - start_time)
