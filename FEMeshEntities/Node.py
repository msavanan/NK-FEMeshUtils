#!/usr/bin/env python
"""
python implementation of FE Node
"""
class Node:
    def __init__(self, NodeID, *coord):
        self.NodeID = NodeID
        self.thickness = 0.0
        self.x = coord[0][0]
        self.y = coord[0][1]
        self.z = coord[0][2]

    def setCoord(self,*coord):
        self.x = coord[0][0]
        self.y = coord[0][1]
        self.z = coord[0][2]

    def setThickness(self, thick):
        self.thickness=thick

    def getID(self):
        return self.NodeID

    def getCoord(self):
        return [self.x, self.y, self.z]
        
    def getThickness(self):
        return self.thickness
