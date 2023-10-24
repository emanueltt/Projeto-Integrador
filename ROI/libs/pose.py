import numpy as np

class Pose(list):
    def __init__(self, x=0.0, y=0.0, rz=0.0):
        super(Pose, self).__init__()
        self.extend([x, y, rz])

    def __add__(self, other):
        try:
            combined = zip(self, Pose(*other))
            result = Pose(*[a+b for a, b in combined])
        except TypeError:
            o = float(other)
            result = Pose(*[a+o for a in self])
        return result

    def __sub__(self, other):
        try:
            combined = zip(self, Pose(*other))
            result = Pose(*[a-b for a, b in combined])
        except TypeError:
            o = float(other)
            result = Pose(*[a-o for a in self])
        return result

    def __mul__(self, other):
        try:
            combined = zip(self, Pose(*other))
            result = Pose(*[a*b for a, b in combined])
        except TypeError:
            o = float(other)
            result = Pose(*[a*o for a in self])
        return result

    def __div__(self, other):
        try:
            combined = zip(self, Pose(*other))
            result = Pose(*[a/float(b) for a, b in combined])
        except TypeError:
            o = float(other)
            result = Pose(*[a/o for a in self])
        return result

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def rz(self):
        return self[2]

    @rz.setter
    def rz(self, value):
        self[2] = value
    
    def __repr__(self):
        output = "Pose(x=%r, y=%r, rz=%r)" % tuple(self)
        return output

    def to_dict(self):
        """
        return Pose as dictionary with keys: x, y, rx
        """
        label = ["x", "y", "rz"]
        d = dict(zip(label, self))
        return d

    def to_3x3(self):
        """
        Convert pose to 3x3 homogeneous transformation matrix.
        """
        sZ = np.sin(np.radians(self.rz))
        cZ = np.cos(np.radians(self.rz))
        T = np.array(
            [[cZ, -sZ, self.x ],
                [sZ,  cZ, self.y ],
                [0. , 0., 1 ]])
        return T

    @classmethod
    def from_3x3(self,T):
        """
        Converts 3x3 homogeneous transformation matrix to pose.
        """
        pose = Pose()
        pose.x = T[0,2]
        pose.y = T[1,2]
        pose.rz = np.degrees(np.arctan2(T[1,0],T[0,0]))
        return pose