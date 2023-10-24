import numpy as np
from .pose import Pose
from .scene import Scene

class Line(Pose):
    def __init__(self, x=0.0, y=0.0, rz=0.0, l=0.0):
        super(Line,self).__init__(x, y, rz)
        self.extend([l])
        
    @property
    def l(self):
        return self[3]

    @l.setter
    def l(self, value):
        self[3] = value

    def __repr__(self):
        output = "Line(x=%r, y=%r, rz=%r, l=%r)" % tuple(self)
        return output

    def to_dict(self):
        """
        Returns Line as dictionary with keys: x, y, rx, l
        """
        label = ["x", "y", "rz", "l"]
        d = dict(zip(label, self))
        return d

    @property
    def end_points(self):
        """
        Retruns the two end-Poses of the line
        """
        start = Pose(x=-0.5*self.l, y=0.0)
        end = Pose(x=0.5*self.l, y=0.0)
        scene = Scene()
        scene.add(self,"line",None)
        scene.add(start,"start","line")
        scene.add(end,"end","line")
        start = scene.get_global("start")
        end = scene.get_global("end")
        return [start,end]

    @classmethod
    def get_intersection_point(self, line1, line2):
        """
        Calculates the intersection point between two lines.
        The rotation is zero.
        """

        x1,y1,rz1 = line1.x,line1.y,line1.rz
        x2,y2,rz2 = line2.x,line2.y,line2.rz

        if rz1 == rz2:
            return None
            
        A1 = float(round(np.tan(np.deg2rad(rz1)),8))
        A2 = float(round(np.tan(np.deg2rad(rz2)),8))
        b1 = y1 - A1*x1
        b2 = y2 - A2*x2
            
        a = np.array ( ( (-A1, 1), (-A2, 1) ) )
        b = np.array ( (b1, b2) )
        x, y = np.linalg.solve(a,b)
        
        return Pose(x=x, y=y)

    @classmethod
    def from_end_points(self, start, end):
        """
        Calculates the intersection point between two lines.
        Rotation is zero.
        """
        diff = end - start
        l = np.linalg.norm([diff.x,diff.y])
        center = start + diff * 0.5
        rz = np.degrees(np.arctan2(diff.y,diff.x))
        return Line(x=center.x,y=center.y,rz=rz,l=l)