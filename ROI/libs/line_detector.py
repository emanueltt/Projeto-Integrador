
import cv2
import numpy as np

class detector_Linha_Gradiente():
    """
    Detecta uma linha horizontal através do gradiente da imagem.
    1. Calcula o gradiente vertical com um filtro de sobel.
    2. Extrai os indices máximo e mínimo para cada coluna
    3. Aplica regressão linear sobre os indices
    """

    def __init__(self, ksize: int = 3, dark_to_bright: bool = True):
        self._ksize = ksize
        self._dark_to_bright = dark_to_bright

    @property
    def ksize(self):
        return self._ksize

    @property
    def dark_to_bright(self):
        return self._dark_to_bright

    def detect(self, img):

        # 1)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=self.ksize)
        # 2)
        if self._dark_to_bright:
            y_points = np.argmax(sobel_y,axis=0)
        else:
            y_points = np.argmin(sobel_y,axis=0)
        x_points = np.arange(0,len(y_points),1)
        # 3)
        cofs, res, _, _, _ = np.polyfit(x_points, y_points, 1, full=True)

        h,w = sobel_y.shape

        x = 0.5*len(y_points)
        y = np.polyval(cofs,x)
        l = len(y_points) * np.sqrt(1+cofs[0]**2)
        rz = np.degrees(np.arctan(cofs[0]))

        result = Line(x=x,
                           y=y,
                           rz=rz,
                           l=l)
        return result