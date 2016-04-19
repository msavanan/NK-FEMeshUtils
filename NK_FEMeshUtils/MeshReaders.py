import subprocess
import logging
import FE_Mesh
import os
import numpy as np
from datetime import datetime
from numpy import cross, eye, dot
from scipy.linalg import expm3, norm
from getpass import getuser

class MeshReaders:
    def __init__(self):
        self.logger=logging.getLogger('MeshReaders')
        self.logger.info('MeshHandlers Object initialized')

    def readDynaMesh(self, file):
        nodesection = False
        elemsection = False
        elemthicksection = False
        partsection = False
        matsection1 = False
        matsection2 = False
        propsection1 = False
        propsection2 = False

        i=0
        self.logger.info("LS-Dyna Reader Started: "+file)

        Mesh=FE_Mesh.Mesh()
        Mesh.setMeshFile(file)
        Mesh.setMeshFormat("LS-Dyna")

        with open(file, "r") as f:
            for line in f:
                if "*KEYWORD" in line:
                    self.logger.debug("*KEYWORD found")

                if line.strip() == "*NODE":
                    self.logger.debug("*NODE keyword found")
                    nodesection = True
                elif (nodesection == True) and (not("$" in line or "*" in line)):
                    Mesh.addNode(line[0:8], line[9:24], line[25:40], line[41:56])
                elif "*" in line:
                    nodesection = False

                if line.strip() == "*ELEMENT_SHELL":
                    self.logger.debug("*ELEMENT_SHELL keyword found")
                    elemsection = True
                elif (elemsection == True) and (not("$" in line or "*" in line)):
                    Mesh.addElem(line[0:8], line[9:16], line[17:24], line[25:32], line[33:40], line[41:48])
                elif "*" in line:
                    elemsection = False

                if line.strip() == "*ELEMENT_SHELL_THICKNESS":
                    self.logger.debug("*ELEMENT_SHELL_THICKNESS keyword found")
                    elemthicksection = True
                    i=0
                elif (elemthicksection == True) and (not("$" in line or "*" in line)):
                    if i == 0:
                        n1=line[17:24]
                        n2=line[25:32]
                        n3=line[33:40]
                        n4=line[41:48]
                        Mesh.addElem(line[0:8], line[9:16], n1, n2, n3, n4)
                        i = i+1
                    elif i==1:
                        Mesh.addNodalThickness(n1,line[0:16])
                        Mesh.addNodalThickness(n2,line[17:32])
                        Mesh.addNodalThickness(n3,line[33:48])
                        Mesh.addNodalThickness(n4,line[49:64])
                        i = 0
                elif "*" in line:
                    elemthicksection = False

                if line.strip() == "*PART":
                    self.logger.debug("*PART Keyword Found")
                    partsection = True
                    i=0
                elif (partsection == True) and (not("$" in line or "*" in line)):
                    if i == 0: title=line.strip()
                    if i == 1:
                        part=line[0:10]
                        prop=line[11:20]
                        mat=line[21:30]
                        Mesh.addPart(part, title, prop, mat)
                    i=i+1
                elif "*" in line:
                    partsection = False


                if line.strip() == "*MAT_PIECEWISE_LINEAR_PLASTICITY" :
                    self.logger.debug("*MAT_PIECEWISE_LINEAR_PLASTICITY Keyword Found")
                    matsection1 = True
                    i=0
                elif (matsection1 == True) and (not("$" in line or "*" in line)):
                    if i == 0:
                        mat=line[0:10]
                        rho=line[11:20]
                        E=line[21:30]
                        Mesh.addMat(mat, rho, E)
                    i=i+1
                elif "*" in line:
                    matsection1 = False

                if line.strip() == "*MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE" :
                    self.logger.debug("*MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE Keyword Found")
                    matsection2 = True
                    i=0
                elif (matsection2 == True) and (not("$" in line or "*" in line)):
                    if i == 0: title=line.strip()
                    if i == 1:
                        mat=line[0:10]
                        rho=line[11:20]
                        E=line[21:30]
                        Mesh.addMat(mat, rho, E)
                    i=i+1
                elif "*" in line:
                    matsection2 = False

                if line.strip() == "*SECTION_SHELL":
                    self.logger.debug("*SECTION_SHELL Keyword Found")
                    propsection1 = True
                    i=0
                elif (propsection1 == True) and (not("$" in line or "*" in line)):
                    if i == 0:
                        prop=line[0:10]
                    if i == 1:
                        thick=line[0:10]
                        Mesh.addProp(prop, thick)
                    i=i+1
                elif "*" in line:
                    propsection1 = False

                if line.strip() == "*SECTION_SHELL_TITLE":
                    self.logger.debug("*SECTION_SHELL_TITLE Keyword Found")
                    propsection2 = True
                    i=0
                elif (propsection2 == True) and (not("$" in line or "*" in line)):
                    if i == 0: title=line.strip()
                    if i == 1: prop=line[0:10]
                    if i == 2:
                        thick=line[0:10]
                        Mesh.addProp(prop, thick)
                    i=i+1
                elif "*" in line:
                    propsection2 = False
        self.logger.info("LS-Dyna Mesh successfully read")
        self.logger.info("Number of Nodes: "+str(len(Mesh.Nodelist)))
        self.logger.info("Number of Elems: "+str(len(Mesh.Elemlist)))
        self.logger.info("Number of Props: "+str(len(Mesh.Proplist)))
        self.logger.info("Number of Mater: "+str(len(Mesh.Matlist)))
        self.logger.info("Number of Parts: "+str(len(Mesh.Partlist)))
        self.logger.info("Number of EThck: "+str(len(Mesh.Elementalthickness)))
        self.logger.info("Number of NThck: "+str(len(Mesh.Nodalthickness)))
        return Mesh

    def readRadiossMesh(self, file):
        nodesection = False
        SH3Nsection = False
        SHELLsection = False
        partsection = False
        matsection = False
        propsection = False

        i=0
        self.logger.info("Radioss Reader Started: "+file)

        Mesh=FE_Mesh.Mesh()
        Mesh.setMeshFile(file)
        Mesh.setMeshFormat("Radioss")

        with open(file, "r") as f:
            for line in f:
                if "#RADIOSS STARTER" in line:
                    self.logger.debug("#RADIOSS STARTER found")

                if "/NODE" in line[0:5]:
                    self.logger.debug("/NODE keyword found")
                    nodesection = True
                elif (nodesection == True) and (not("#" in line or "/" in line)):
                    Mesh.addNode(line[0:10], line[11:30], line[31:50], line[51:70])
                elif nodesection and "/" in line:
                    nodesection = False

                if "/SH3N" in line[0:5]:
                    self.logger.debug("/SH3N keyword found")
                    partid=line.strip().split("/")[2]
                    SH3Nsection = True
                elif (SH3Nsection == True) and (not("#" in line or "/" in line)):
                    #print [line[0:10], partid, line[11:20], line[21:30], line[31:40]]
                    Mesh.addElem(line[0:10], partid, line[11:20], line[21:30], line[31:40])
                    if line[91:100].strip() != "": Mesh.addElementalThickness(line[0:10],line[91:100])
                elif SH3Nsection and "/" in line:
                    SH3Nsection = False

                if "/SHELL" in line[0:6]:
                    self.logger.debug("/SHELL keyword found")
                    partid=line.strip().split("/")[2]
                    SHELLsection = True
                elif (SHELLsection == True) and (not("#" in line or "/" in line)):
                    #print [line[0:10], partid, line[11:20], line[21:30], line[31:40], line[41:50]]
                    Mesh.addElem(line[0:10], partid, line[11:20], line[21:30], line[31:40], line[41:50])
                    if line[91:100].strip() != "": Mesh.addElementalThickness(line[0:10],line[91:100])
                elif SHELLsection and "/" in line:
                    SHELLsection = False

                if "/PART" in line[0:5]:
                    self.logger.debug("/PART Keyword Found")
                    partid=line.strip().split("/")[2]
                    partsection = True
                    i=0
                elif (partsection == True) and (not("#" in line or "/" in line)):
                    if i == 0: title=line.strip()
                    elif i == 1:
                        prop=line[0:10]
                        mat=line[11:20]
                        Mesh.addPart(partid, title, prop, mat)
                    i=i+1
                elif partsection and "/" in line:
                    partsection = False

                if "/MAT/PLAS_TAB" in line[0:13]:
                    self.logger.debug("/MAT/PLAS_TAB Keyword Found")
                    matid=line.strip().split("/")[3]
                    matsection = True
                    i=0
                elif (matsection == True) and (not("#" in line or "/" in line)):
                    if i == 0: title=line.strip()
                    elif i == 1: rho=line[0:20]
                    elif i == 2:
                        E=line[0:20]
                        Mesh.addMat(matid, rho, E)
                    i=i+1
                elif matsection and "/" in line:
                    matsection = False

                if "/PROP/SHELL" in line[0:11]:
                    self.logger.debug("/PROP/SHELL Keyword Found")
                    propid=line.strip().split("/")[3]
                    propsection = True
                    i=0
                elif (propsection == True) and (not("#" in line or "/" in line)):
                    if i == 0: title=line.strip()
                    elif i == 3:
                        thick=line[21:40]
                        Mesh.addProp(propid, thick)
                    i=i+1
                elif propsection and "/" in line:
                    propsection = False

        self.logger.info("Radioss Mesh successfully read")
        self.logger.info("Number of Nodes: "+str(len(Mesh.Nodelist)))
        self.logger.info("Number of Elems: "+str(len(Mesh.Elemlist)))
        self.logger.info("Number of Props: "+str(len(Mesh.Proplist)))
        self.logger.info("Number of Mater: "+str(len(Mesh.Matlist)))
        self.logger.info("Number of Parts: "+str(len(Mesh.Partlist)))
        self.logger.info("Number of EThck: "+str(len(Mesh.Elementalthickness)))
        self.logger.info("Number of NThck: "+str(len(Mesh.Nodalthickness)))

        return Mesh

    def writeDynaMesh(self, Mesh, file):
        elemsection = False
        elemthicksection = False
        elemshellthicknesswritten = False
        elemshellwritten = False
        nodesection = False
        i=0

        ofile=open(file, "w")
        ofile.write("$ - Mubea TRB CAE - FE_Mesh_Handlers - writeDynaMesh\n")
        ofile.write("$ - Date/Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S')+"\n")
        ofile.write("$ - User: "+getuser()+"\n")

        self.logger.info("LS-Dyna Mesh will be written to: "+ file)
        self.logger.info("Baseline Input is taken from: "+ Mesh.getMeshFile())
        with open(Mesh.getMeshFile(), "r") as f:
            for line in f:
                if (elemsection == True) and (not("$" in line or "*" in line)):
                    if (int(line[9:16]) in Mesh.TRBProps):
                        if not elemshellthicknesswritten:
                            ofile.write("*ELEMENT_SHELL_THICKNESS\n")
                            elemshellthicknesswritten=True
                            elemthicksection=True
                            elemshellwritten=False
                        ofile.write(line)
                        #elem=Mesh.getElemObjByID(int(line[0:8]))
                        #numbernodes=len(set(Mesh.getElemlist()[int(line[0:8]][1:]))
                        n1=Mesh.getNodalThickness(int(line[17:24]))
                        n2=Mesh.getNodalThickness(int(line[25:32]))
                        n3=Mesh.getNodalThickness(int(line[33:40]))
                        n4=Mesh.getNodalThickness(int(line[41:48]))
                        s= "%16.8f"%n1+"%16.8f"%n2+"%16.8f"%n3+"%16.8f"%n4+"\n"
                        ofile.write(s)
                        i=i+1
                    else:
                        if not elemshellwritten:
                            ofile.write("*ELEMENT_SHELL\n")
                            elemthicksection=False
                            elemshellwritten=True
                            elemsection=True
                            elemshellthicknesswritten=False
                        ofile.write(line)
                elif (elemthicksection) and (not("$" in line or "*" in line)):
                    ofile.write(line)
                    #
                elif nodesection and (not("$" in line or "*" in line)):
                    nid=int(line[0:8])
                    x=float(Mesh.Nodelist[nid][0])
                    y=float(Mesh.Nodelist[nid][1])
                    z=float(Mesh.Nodelist[nid][2])
                    s= "%8i"%nid+"%16.10f"%x+"%16.10f"%y+"%16.10f"%z+"\n"
                    ofile.write(s)
                elif line.strip() == "*ELEMENT_SHELL":
                    self.logger.debug("*ELEMENT_SHELL found")
                    elemsection = True
                    elemthicksection = False
                    elemshellthicknesswritten = False
                    elemshellwritten = True
                    nodesection = False
                    self.logger.debug("state variables [elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]"+str([elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]))
                    ofile.write(line)
                elif line.strip() == "*ELEMENT_SHELL_THICKNESS":
                    i=0
                    self.logger.debug("*ELEMENT_SHELL_THICKNESS found")
                    elemsection = False
                    elemthicksection = True
                    elemshellthicknesswritten = True
                    elemshellwritten = False
                    nodesection = False
                    self.logger.debug("state variables [elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]"+str([elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]))
                    ofile.write(line)
                elif line.strip() == "*NODE":
                    self.logger.debug("*NODE found")
                    elemsection = False
                    elemthicksection = False
                    elemshellthicknesswritten = False
                    elemshellwritten = False
                    nodesection = True
                    self.logger.debug("state variables [elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]"+str([elemsection,elemshellwritten,elemthicksection,elemshellthicknesswritten,nodesection]))
                    ofile.write(line)
                elif "*" in line and not "*ELEMENT_SHELL" in line and not "*NODE" in line:
                    elemsection = False
                    nodesection = False
                    ofile.write(line)
                else:
                    ofile.write(line)
        ofile.close
        self.logger.info('Writing to LS-Dyna Mesh file completed')

    def writeRadiossMesh(self, Mesh, file):
        nodesection = False
        SH3Nsection = False
        SHELLsection = False
        partsection = False
        matsection = False
        propsection = False

        elemthick=False
        partid = 0
        i=0

        ofile=open(file, "w")
        self.logger.info("Radioss Mesh will be written to: "+ file)
        self.logger.info("Baseline Input is taken from: "+ Mesh.getMeshFile())
        with open(Mesh.getMeshFile(), "r") as f:
            if len(Mesh.Elementalthickness.keys())!=0: elemthick=True
            for line in f:
                if "#RADIOSS STARTER" in line:
                    ofile.write(line)
                    ofile.write("## - Mubea TRB CAE - FE_Mesh_Handlers - writeRadiossMesh\n")
                    ofile.write("## - Date/Time: "+datetime.now().strftime('%Y/%m/%d %H:%M:%S')+"\n")
                    ofile.write("## - User: "+getuser()+"\n")
                elif ((SH3Nsection == True) or (SHELLsection == True)) and (not("#" in line or "/" in line)):
                    elemid=int(line[0:10])
                    if elemthick:
                        if int(partid) in Mesh.TRBProps:
                            thick = Mesh.getElementalThickness(elemid)
                        else: thick = 0.0
                    else:
                        thick = 0.0
                    ofile.write(line[0:90]+"%10.8f"%thick+"\n")
                elif nodesection and (not("#" in line or "/" in line)):
                    nid=int(line[0:10])
                    x=float(Mesh.Nodelist[nid][0])
                    y=float(Mesh.Nodelist[nid][1])
                    z=float(Mesh.Nodelist[nid][2])
                    s= "%10i"%nid+"%20.14f"%x+"%20.14f"%y+"%20.14f"%z+"\n"
                    ofile.write(s)
                elif "/SH3N" in line[0:5]:
                    self.logger.debug("/SH3N found")
                    partid=line.strip().split("/")[2]
                    SH3Nsection = True
                    SHELLsection = False
                    nodesection = False
                    ofile.write(line)
                elif "/SHELL" in line[0:6]:
                    i=0
                    self.logger.debug("/SHELL found")
                    partid=line.strip().split("/")[2]
                    SH3Nsection = False
                    SHELLsection = True
                    nodesection = False
                    ofile.write(line)
                elif "/NODE" in line[0:5]:
                    self.logger.debug("/NODE found")
                    SH3Nsection = False
                    SHELLsection = False
                    nodesection = True
                    ofile.write(line)
                elif "/" in line:
                    SH3Nsection = False
                    SHELLsection = False
                    nodesection = False
                    ofile.write(line)
                else:
                    ofile.write(line)
        ofile.close
        self.logger.info('Writing Radioss Mesh file completed')
