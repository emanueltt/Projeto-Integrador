import cv2
import numpy as np
from .pose import Pose
from .line import Line
from .scene import Scene

class Rectangle(Pose):
    def __init__(self, x=0.0, y=0.0, rz=0.0, w=0.0, h=0.0):
        super(Rectangle,self).__init__(x, y, rz)
        self.extend([w, h])
        
    @property
    def w(self):
        return self[3]

    @w.setter
    def w(self, value):
        self[3] = value

    @property
    def h(self):
        return self[4]

    @h.setter
    def h(self, value):
        self[4] = value

    def __repr__(self):
        output = "Rectangle(x=%r, y=%r, rz=%r, w=%r, h=%r)" % tuple(self)
        return output

    def to_dict(self):
        """
        Returns Rectangle as dictionary with keys: x, y, rx, ry, rz
        """
        label = ["x", "y", "rz", "w", "h"]
        d = dict(zip(label, self))
        return d

    @property
    def corner_points(self):
        """
        Retruns the four coner-points of a rectangle.
        The poses are labeled clockwise.
        The rotation is increased clocwise
        """
        points_local = [Pose(x=0.0, y=0.0, rz=0.0), 
                        Pose(x=self.w, y=0.0, rz=90.0), 
                        Pose(x=self.w, y=self.h, rz=180.0), 
                        Pose(x=0.0, y=self.h, rz=270.0)]
        scene = Scene()
        scene.add(self,"rect",None)
        points_global = []
        for point in points_local:
            scene.add(point,"point","rect")
            points_global.append(scene.get_global("point"))
            scene.remove("point")
        return points_global

    @property
    def edge_lines(self):
        """
        Retruns the four edge-lines of a rectangle.
        The lines are labeled clockwise.
        """
        lines_local = [Line(x=0.5*self.w,y=0.0,rz=0.0,l=self.w),
                       Line(x=self.w,y=0.5*self.h,rz=90.0,l=self.h),
                       Line(x=0.5*self.w,y=self.h,rz=180.0,l=self.w),
                       Line(x=0.0,y=0.5*self.h,rz=-90.0,l=self.h)]
        scene = Scene()
        scene.add(self,"rect",None)
        lines_global = []
        for line in lines_local:
            scene.add(line,"line","rect")
            lines_global.append(scene.get_global("line"))
            scene.remove("line")
        return lines_global
            
    def crop_from_img(self, img):
        corner_points =  self.corner_points
        src_pts = [[point.x,point.y] for point in corner_points]
        src_pts = np.array(src_pts).astype('float32')
        dst_pts = np.array([[0,0],
                            [self.w-1, 0],
                            [self.w-1, self.h-1],
                            [0, self.h-1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(img, M, (int(self.w), int(self.h)))
        return warped