"""
--------------------------------------------------------------------------------------
--------------------------FE Mesh Handler---------------------------------------------
--------------------------------------------------------------------------------------
This Module was created for handling Mesh Data. Data is stored in Dictionaries.
Due to the Hashtable structure accessing specific data is quite fast.
Nevertheless Mass / Volume calculation for a single part in a large assembly mesh is slow
Therefore it is better to use the ObjectStructure and the Part.getPartMass() Method

"""
import numpy as np
import logging

class Node:
    thickness=0.0

    def __init__(self, NodeID, *coord):
        self.NodeID = NodeID
        self.x = coord[0][0]
        self.y = coord[0][1]
        self.z = coord[0][2]

    def getCoord(self):
        return [self.x, self.y, self.z]

    def setCoord(self,*coord):
        self.x = coord[0][0]
        self.y = coord[0][1]
        self.z = coord[0][2]

    def getID(self):
        return self.NodeID

    def setThickness(self, thick):
        self.thickness=thick

    def getThickness(self):
        return self.thickness

class Elem:
    def __init__(self, ElemID):
        self.ElemID = ElemID

class Tria(Elem):
    thickness=0.0
    def __init__(self, ElemID, PartID, Node1, Node2, Node3):
        self.ElemID = ElemID
        self.PartID = PartID
        self.Node1 = Node1
        self.Node2 = Node2
        self.Node3 = Node3

    def getNodes(self):
        return [self.Node1, self.Node2, self.Node3]

    def getID(self):
        return self.ElemID

    def getNodelist(self):
        return [self.Node1, self.Node2, self.Node3]

    def calcThickness(self):
        tempthick=0.0
        for node in self.getNodelist():
            tempthick=tempthick+node.getThickness()
        self.thickness = tempthick/3

    def getThickness(self):
        return self.thickness

    def getArea(self):
        a = np.array([self.Node1.x, self.Node1.y, self.Node1.z])
        b = np.array([self.Node2.x, self.Node2.y, self.Node2.z])
        c = np.array([self.Node3.x, self.Node3.y, self.Node3.z])
        return 0.5 * np.linalg.norm(np.cross(b-a, c-a ))

    def getVolume(self):
        if self.thickness!=0.0:
            return self.getArea()*self.thickness

class Quad(Elem):
    thickness=0.0
    def __init__(self, ElemID, PartID, Node1, Node2, Node3, Node4):
        self.ElemID = ElemID
        self.PartID = PartID
        self.Node1 = Node1
        self.Node2 = Node2
        self.Node3 = Node3
        self.Node4 = Node4

    def getNodes(self):
        return [self.Node1, self.Node2, self.Node3, self.Node4]

    def getID(self):
        return self.ElemID

    def getNodelist(self):
        return [self.Node1, self.Node2, self.Node3, self.Node4]

    def calcThickness(self):
        tempthick=0.0
        for node in self.getNodelist():
            tempthick=tempthick+node.getThickness()
        self.thickness = tempthick/4
        return self.thickness


    def getThickness(self):
        return self.thickness

    def getArea(self):
        a = np.array([self.Node1.x, self.Node1.y, self.Node1.z])
        b = np.array([self.Node2.x, self.Node2.y, self.Node2.z])
        c = np.array([self.Node3.x, self.Node3.y, self.Node3.z])
        d = np.array([self.Node4.x, self.Node4.y, self.Node4.z])
        return 0.5 * np.linalg.norm(np.cross(c-a, d-b ))

    def getVolume(self):
        if self.thickness!=0.0:
            return self.getArea()*self.thickness

class Part:
    def __init__(self, PartID, title, Mat, Prop):
        self.TRBbool=False
        self.PartID=PartID
        self.Mat=Mat
        self.Prop=Prop
        self.title=title
        self.ElemObj=[]
        self.Elemlist={}
        self.Nodelist={}

    def addElem(self, Elem):
        self.ElemObj.append(Elem)
        self.Elemlist[Elem.getID()]=Elem
        for node in Elem.getNodelist():
            self.Nodelist[node.getID()]=node

    def getNumElem(self):
        return len(self.ElemObj)

    def getElemObj(self):
        return self.ElemObj

    def getElemlist(self):
        return self.Elemlist

    def getNodelist(self):
        return self.Nodelist

    def getPartArea(self):
        Area=0.0
        for elem in self.ElemObj:
            Area=Area+elem.getArea()
        return Area

    def getPartVolume(self):
        Volume=0.0
        if self.isTRB():
            for elem in self.ElemObj:
                Volume=Volume+elem.getVolume()
        else:
            Volume = self.Prop.thickness*self.getPartArea()
        return Volume

    def getPartMass(self):
        return self.Mat.Rho*self.getPartVolume()

    def getPartID(self):
        return self.PartID

    def getPartname(self):
        return self.title

    def setTRB(self, _TRBbool):
        self.TRBbool=_TRBbool

    def isTRB(self):
        return self.TRBbool

class Material:
    MatID=0
    Rho=0.0
    E=0.0

    def __init__(self, MatID, Rho, E):
        self.MatID=MatID
        self.Rho=float(Rho)
        self.E=float(E)

class Property:
    thickness=0.0

    def __init__(self, PropID, thickness):
        self.PropID=PropID
        self.thickness=thickness

class Mesh:
    # This Class is handling FE Meshes

    def __init__(self):
        # Variables for Mesh Import
        self.Nodelist={}
        self.Nodalthickness={}
        self.Elementalthickness={}
        self.Elemlist={}
        self.PartElemlist={}
        self.Partlist={}
        self.Matlist={}
        self.Proplist={}
        self.PartObjList={}
        self.TRBProps=[]

        self.Meshfile=""
        self.Meshformat=""

        self.logger=logging.getLogger('Mesh')
        self.logger.info('Mesh Object initialized')

    def addNode(self, NodeID, x, y, z):
        self.Nodelist[int(NodeID)]=[float(x), float(y), float(z)]

    def addElem(self, ElemID, PartID, *Nodes):
        if len(Nodes)==3:
            self.Elemlist[int(ElemID)]=[int(PartID), int(Nodes[0]), int(Nodes[1]), int(Nodes[2])]
        elif len(Nodes)==4:
            self.Elemlist[int(ElemID)]=[int(PartID), int(Nodes[0]), int(Nodes[1]), int(Nodes[2]), int(Nodes[3])]
        if not int(PartID) in self.PartElemlist:
            self.PartElemlist[int(PartID)]=[int(ElemID)]
        else:
            self.PartElemlist[int(PartID)].append(int(ElemID))

    def addNodalThickness(self, NodeID, thickness):
        self.Nodalthickness[NodeID]=float(thickness)

    def addElementalThickness(self, ElemID, thickness):
        self.Elementalthickness[ElemID]=float(thickness)

    def getNodalThickness(self, NodeID):
        return self.Nodalthickness[NodeID]

    def getElementalThickness(self, ElemID):
        return self.Elementalthickness[ElemID]

    def addPart(self, PartID, title, PropID, MatID):
        self.Partlist[int(PartID)]=[title, int(PropID), int(MatID)]

    def addMat(self, MatID, Rho, E):
        self.Matlist[int(MatID)]=[Rho, E]

    def addProp(self, PropID, Thickness):
        self.Proplist[int(PropID)]=[float(Thickness)]

    def InitPartObj(self, PartID):
        self.logger.info('Initialize Part: '+str(PartID))

        if self.Nodelist=={}:
            self.logger.error("Missing Nodes. Please check Input")
            raise Exception("Missing Nodes. Please check Input")
        elif self.Elemlist=={}:
            self.logger.error("Missing Elements. Please check Input")
            raise Exception("Missing Elements. Please check Input")
        else:
            matid = 0
            rho = 7.9E-9
            e = 210000
            propid = 0
            thickness = 1.0
            propid=0
            matid=0
            title="GenericPart"

            if self.Matlist=={} :
                self.logger.warning("Missing Material Definition. Please check Input. Steel Values in Ton mm s set as default")

            if self.Proplist=={}:
                self.logger.warning("Missing Property Definition. Please check Input. 1 mm constant used as default")

            if self.Partlist=={}:
                self.logger.warning("Missing Part Definition. Please check Input. Generic Part will be created")

            if self.Matlist!={} and self.Proplist!={} and self.Partlist=={}:
                matid=self.Partlist[PartID][2]
                propid=self.Partlist[PartID][1]
                title=self.Partlist[PartID][0]
                rho=self.Matlist[matid][0]
                e=self.Matlist[matid][1]
                thickness=self.Proplist[propid][0]

            prop=Property(propid, thickness)
            mat=Material(matid, rho, e)
            part=Part(PartID, title, mat, prop)

            for elem in self.Elemlist.iteritems():
                #print elem[0]
                if elem[1][0] == PartID:
                    if len(elem[1])==5:
                        node1=Node(elem[1][1], self.Nodelist[elem[1][1]])
                        node2=Node(elem[1][2], self.Nodelist[elem[1][2]])
                        node3=Node(elem[1][3], self.Nodelist[elem[1][3]])
                        node4=Node(elem[1][4], self.Nodelist[elem[1][4]])
                        quad=Quad(elem[0], elem[1][0], node1, node2, node3, node4)
                        part.addElem(quad)
                    elif len(elem[1])==4:
                        node1=Node(elem[1][1], self.Nodelist[elem[1][1]])
                        node2=Node(elem[1][2], self.Nodelist[elem[1][2]])
                        node3=Node(elem[1][3], self.Nodelist[elem[1][3]])
                        tria=Tria(elem[0], elem[1][0], node1, node2, node3)
                        part.addElem(tria)
            self.PartObjList[PartID]=part
            self.logger.info("Part "+str(part.getPartID())+" initialized with "+str(part.getNumElem())+" Elements.")
        return part

    def InitAllObj(self):
        self.logger.info("Initall started")
        for PartID, Partvalues in self.Partlist.iteritems():
            matid=Partvalues[2]
            propid=Partvalues[1]
            title=Partvalues[0]

            if propid in self.Proplist.keys() and matid in self.Matlist.keys():
                rho=self.Matlist[matid][0]
                e=self.Matlist[matid][1]
                thickness=self.Proplist[propid][0]

                prop=Property(propid, thickness)
                mat=Material(matid, rho, e)

                part=Part(PartID, title, mat, prop)
                self.logger.info("Part created: "+str(PartID))

                for elem in self.Elemlist.iteritems():
                    #print elem[0]
                    if elem[1][0] == PartID:
                        if len(elem[1])==5:
                            node1=Node(elem[1][1], self.Nodelist[elem[1][1]])
                            node2=Node(elem[1][2], self.Nodelist[elem[1][2]])
                            node3=Node(elem[1][3], self.Nodelist[elem[1][3]])
                            node4=Node(elem[1][4], self.Nodelist[elem[1][4]])
                            quad=Quad(elem[0], elem[1][0], node1, node2, node3, node4)
                            part.addElem(quad)
                        elif len(elem[1])==4:
                            node1=Node(elem[1][1], self.Nodelist[elem[1][1]])
                            node2=Node(elem[1][2], self.Nodelist[elem[1][2]])
                            node3=Node(elem[1][3], self.Nodelist[elem[1][3]])
                            tria=Tria(elem[0], elem[1][0], node1, node2, node3)
                            part.addElem(tria)
            self.PartObjList[PartID]=part

    def setMeshFile(self,file):
        self.Meshfile=file

    def setMeshFormat(self,format):
        self.MeshFormat=format

    def getMeshFormat(self):
        return self.MeshFormat

    def getMeshFile(self):
        return self.Meshfile

    def getNodelist(self):
        return self.Nodelist

    def getElemlist(self):
        return self.Elemlist

    def getMassByPartID(self,PartID):
        MatID=self.Partlist[PartID][2]
        density=self.Matlist[MatID][2]
        return self.getVolumeByPartID(PartID)*density

    def getVolumeByPartID(self,PartID):
        # This Method is very slow compared to object strucutre!
        vol = 0.0
        #for ElemID, ElemData in self.getElemlist().iteritems():
        #    if ElemData[0] == PartID:
        for ElemID in self.PartElemlist[PartID]:
            vol = vol + self.getVolumeByElemID(ElemID)
        return vol

    def getAreaByPartID(self,PartID):
        area = 0.0
        for ElemID, ElemData in self.getElemlist().iteritems():
            if ElemData[0] == PartID:
                area = area + self.getAreaByElemID(ElemID)
        return area

    def getAreaByElemID(self,ElemID):
        area = 0.0
        nodesOfElem = self.getNodesByElemID(ElemID)
        a = np.array(self.getNodeByID(nodesOfElem[0]))
        b = np.array(self.getNodeByID(nodesOfElem[1]))
        c = np.array(self.getNodeByID(nodesOfElem[2]))
        if len(nodesOfElem)==3:
            d = c
        elif len(nodesOfElem)==4:
            d = np.array(self.getNodeByID(nodesOfElem[3]))
        area = area + 0.5 * np.linalg.norm(np.cross(c-a, d-b ))
        return area

    def getVolumeByElemID(self,ElemID):
        area = self.getAreaByElemID(ElemID)
        if ElemID in self.Elementalthickness.keys():
            vol = area * self.getElementalThickness(ElemID)
        else:
            PartID=self.Elemlist[ElemID][0]
            PropID=self.Partlist[PartID][1]
            pthick=self.Proplist[PropID][0]
            vol = area * pthick
        return vol

    def getNodeObjByID(self, NodeID):
        for part in self.PartObjList.itervalues():
            if NodeID in part.Nodelist.keys():
                return part.Nodelist[NodeID]

    def getElemObjByID(self, ElemID):
        part=self.PartObjList[self.Elemlist[ElemID][0]]
        if ElemID in part.Elemlist.keys():
            return part.Elemlist[ElemID]

    def getNodeByID(self, NodeID):
        return self.Nodelist[NodeID]

    def getNodesByElemID(self, ElemID):
        return self.Elemlist[ElemID][1:]

    def getElemByID(self, ElemID):
        return self.Elemlist[ElemID]

    def getPartlistObj(self):
        return self.PartObjList

    def getPartByID(self,PartID):
        return self.PartObjList[PartID]

    def getRectangleBounds(self):
        # This Method gives you the Edge Values of the sourrounding rectangle
        # It is created in order to help positioning a blank file or calculating scrap
        Nodes = {'NodeId': np.array(self.Nodelist.keys(), dtype=int), 'coord': np.array(self.Nodelist.values(), dtype=float)}
        xmin=np.amin(Nodes['coord'][:,0])
        xmax=np.amax(Nodes['coord'][:,0])
        ymin=np.amin(Nodes['coord'][:,1])
        ymax=np.amax(Nodes['coord'][:,1])
        zmin=np.amin(Nodes['coord'][:,2])
        zmax=np.amax(Nodes['coord'][:,2])
        self.logger.debug("Bounds of Outer Box: "+ str([xmin,xmax,ymin,ymax,zmin,zmax]))
        return [xmin,xmax,ymin,ymax,zmin,zmax]
