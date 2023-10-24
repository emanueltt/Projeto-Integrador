import cv2
import numpy as np
from .line import Line
from sklearn import linear_model

class LineDetectorAll():
    """
    Detects a horizonatal line by the following sequence.
    1. Calculate vertical gradient by sobel-filter with ksize
    2. Extraction of the max indize for each gradient column
    3. Ransac line-fit over the indizes
    """

    def __init__(self, ksize: int = 3, dark_to_bright: bool = True, poly_or_ran: bool = True, vertical: bool = False):
        self._ksize = ksize
        self._dark_to_bright = dark_to_bright
        self._poly_or_ran = poly_or_ran
        self._ransac: object = linear_model.RANSACRegressor()
        self._vertical = vertical

    @property
    def ksize(self):
        return self._ksize

    @property
    def dark_to_bright(self):
        return self._dark_to_bright

    @property
    def poly_or_ran(self):
        return self._poly_or_ran

    def detect(self, img):
        if self._vertical:
            # 1)
            sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=self.ksize)

            # 2)
            if self._dark_to_bright:
                x_points = np.argmax(sobel_x,axis=1)
            else:
                x_points = np.argmin(sobel_x,axis=1)
            y_points = np.arange(0,len(x_points),1)

            # 3)
            if self._poly_or_ran:
                cofs, res, _, _, _ = np.polyfit(x_points, y_points, 1, full=True)

                h,w = sobel_x.shape

                x = 0.5*len(y_points)
                y = np.polyval(cofs,x)
                l = len(y_points) * np.sqrt(1+cofs[0]**2)
                rz = np.degrees(np.arctan(cofs[0]))
            else:
                self._ransac.fit(np.array([x_points]).T, y_points)
                slope = self._ransac.estimator_.coef_[0]
                h,w = sobel_x.shape

                x = 0.5*len(y_points)
                y = self._ransac.predict(np.array([[x]]))[0]
                l = len(y_points) * np.sqrt(1+slope**2)
                rz = np.degrees(np.arctan(slope))

            result = Line(x=x,
                            y=y,
                            rz=rz,
                            l=l)
            return result
        else:
            # 1)
            sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=self.ksize)

            # 2)
            if self._dark_to_bright:
                y_points = np.argmax(sobel_y,axis=0)
            else:
                y_points = np.argmin(sobel_y,axis=0)
            x_points = np.arange(0,len(y_points),1)

            # 3)
            if self._poly_or_ran:
                cofs, res, _, _, _ = np.polyfit(x_points, y_points, 1, full=True)

                h,w = sobel_y.shape

                x = 0.5*len(y_points)
                y = np.polyval(cofs,x)
                l = len(y_points) * np.sqrt(1+cofs[0]**2)
                rz = np.degrees(np.arctan(cofs[0]))
            else:
                self._ransac.fit(np.array([x_points]).T, y_points)
                slope = self._ransac.estimator_.coef_[0]
                h,w = sobel_y.shape

                x = 0.5*len(y_points)
                y = self._ransac.predict(np.array([[x]]))[0]
                l = len(y_points) * np.sqrt(1+slope**2)
                rz = np.degrees(np.arctan(slope))

            result = Line(x=x,
                            y=y,
                            rz=rz,
                            l=l)
            return result