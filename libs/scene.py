import numpy as np
from .pose import Pose
import copy

class Scene():
    def __init__(self):
        self.elements = {}
        self.hierarchy = {}
        
    def get_element(self,name):
        return self.elements[name]

    def get_parent(self,name):
        parent = self.hierarchy[name]
        if parent is None:
            return None
        else: 
            return self.elements[parent]

    def get_childs(self,name):
        childs = []
        for key, value in self.hierarchy.items():
            if value == name:
                childs.append(self.elements[key])
        return childs
    
    def add(self,element,name,parent):
        self.elements[name] = element
        self.hierarchy[name] = parent
        
    def remove(self,name):
        del(self.elements[name])
        del(self.hierarchy[name])
        
    def get_local(self,name):
        element = copy.copy(self.elements[name])
        return element
    
    def get_global(self, name):
        element = self.elements[name]
        parent_name = self.hierarchy[name]
        M = self.elements[name].to_3x3()
        while parent_name is not None:
            parent = self.elements[parent_name]
            M_parent = parent.to_3x3()
            M = np.dot(M_parent,M)
            parent_name = self.hierarchy[parent_name]
        pose_abs = Pose.from_3x3(M)
        ret = copy.copy(element)
        ret[0:3] = pose_abs[0:3]
        return ret
        
    def from_to_local(self,a,b):
        p1 = get_global(a)
        p2 = get_global(b)
        M = np.dot(np.linalg.inv(p1.to_3x3()),p2.to_3x3())
        return Pose.from_3x3(M)

    def from_to_global(self,a,b):
        p1 = get_global(a)
        p2 = get_global(b)
        return p2-p1
        
    def update_global_pose(self,name,pose,changer):
        """
        Updates the "pose" of the element "name" by changing the local pose of "changer".
        """
        diff = from_to_global(name,changer)
        global_new = diff + pose
        parent_name = self.hierarchy[changer]
        if parent_name is None:
            self.remove(changer)
            self.add(global_new,changer,None)
        else:
            self.add(global_new,"global_new",None)
            diff_local = from_to_local(parent_name,"global_new")
            self.remove("global_new")
            self.remove(changer)
            self.add(a,changer,parent_name)