# Distacia linhas
import cv2
import numpy as np
from .libs.line_detector_all import LineDetectorAll
from .libs import Rectangle, Scene
from .libs import draw_line_1

# %matplotlib inline


def process_image(img):
    img_gray = img[400:800, 350:850]
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 5, 20, 20)

    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=9)

    opening = np.sqrt(sobel_y**2)
    opening = (np.mean(opening, axis=0)) - np.min(np.mean(opening, axis=0))

    rois = []
    n_cont = 0
    save_it = 0
    pause_cont = 0

    for i in opening:
        if i > np.mean(opening):
            if pause_cont <= 0:
                save_it = 1

        if save_it:
            rois.append(n_cont)
            pause_cont = 100
            save_it = 0

        n_cont += 1
        pause_cont -= 1

    try:
        rect_1 = Rectangle(
            x=rois[0] - 20, y=int(img_gray.shape[0] / 4), rz=0, w=100, h=100
        )

        rect_2 = Rectangle(
            x=rois[1] - 20, y=int(img_gray.shape[0] / 3), rz=0, w=100, h=100
        )
        # rect_3 = Rectangle(x=rois[2] - 20, y=int(img_gray.shape[0] / 3), rz=0, w=100, h=100)
    except IndexError:
        return img_gray

    roi_1 = rect_1.crop_from_img(img_gray)
    roi_2 = rect_2.crop_from_img(img_gray)
    # roi_3 = rect_3.crop_from_img(img_gray)

    l_Detector_1 = LineDetectorAll(9, True, False, True)
    l_Detector_2 = LineDetectorAll(9, True, False, True)
    # l_Detector_3 = LineDetectorAll(9, True, False, True)

    line_1 = l_Detector_1.detect(roi_1)
    line_2 = l_Detector_2.detect(roi_2)
    # line_3 = l_Detector_3.detect(roi_3)

    # Scenes
    scene_1 = Scene()
    scene_1.add(rect_1, "rect_1", None)
    scene_1.add(rect_2, "rect_2", None)
    # scene_1.add(rect_3, "rect_3", None)
    scene_1.add(line_1, "line_1", "rect_1")
    scene_1.add(line_2, "line_2", "rect_2")
    # scene_1.add(line_3, "line_3", "rect_3")

    # Global lines
    line_1_global = scene_1.get_global("line_1")
    line_2_global = scene_1.get_global("line_2")
    # line_3_global = scene_1.get_global("line_3")

    img_lines = img_gray
    draw_line_1(img_lines, line_1_global, color=255, linewidth=4, transparency=0.0)
    draw_line_1(img_lines, line_2_global, color=255, linewidth=4, transparency=0.0)

    text_distance = f"{line_2_global[0] - line_1_global[0]} px"
    img_lines = cv2.putText(
        img_lines,
        text=text_distance,
        org=(10, 30),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=2,
        color=(255, 255, 255),
        thickness=2
    )
    # draw_line_1(img_lines, line_3_global, color=255, linewidth=4, transparency=0.0)

    return img_lines
