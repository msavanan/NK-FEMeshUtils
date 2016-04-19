from Element import Element
import numpy as np
class Quad(Element):
    def __init__(self, ElemID, PartID, Node1, Node2, Node3, Node4):
        self.thickness = 0.0
        self.ElemID = ElemID
        self.PartID = PartID
        self.Nodes = [Node1, Node2, Node3, Node4]

    def UpdateThicknessFromNodes(self):
        tempthick=0.0
        for node in self.getNodes():
            tempthick=tempthick+node.getThickness()
        self.thickness = tempthick/4
        return self.thickness

    def getArea(self):
        a = np.array([self.Node1.x, self.Node1.y, self.Node1.z])
        b = np.array([self.Node2.x, self.Node2.y, self.Node2.z])
        c = np.array([self.Node3.x, self.Node3.y, self.Node3.z])
        d = np.array([self.Node4.x, self.Node4.y, self.Node4.z])
        return 0.5 * np.linalg.norm(np.cross(c-a, d-b ))
