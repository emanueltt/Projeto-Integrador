import cv2
import numpy as np
from ROI.libs.line_detector_all import LineDetectorAll
from ROI.libs import Rectangle, Scene
# from libs import draw_rectangle_1, draw_line_1
# from IPython.display import display, clear_output, Image
# import time
# import matplotlib.pyplot as plt

# Balao
def dist_interna(img):
    imagem_rotacionada = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    img_gray = imagem_rotacionada[100:imagem_rotacionada.shape[0], 120:350].copy()
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 5, 20, 20)

    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=9)

    opening = np.sqrt(sobel_y**2)
    opening = (np.mean(opening, axis = 1)) - np.min(np.mean(opening, axis = 1))

    rois = []
    n_cont = 0
    save_it = 0
    pause_cont = 0

    for i in opening:
        if i > np.mean(opening)*7 and n_cont > 50:
            if pause_cont <= 0:
                save_it = 1

        if save_it:
            rois.append(n_cont)
            pause_cont = 100
            save_it = 0

        n_cont += 1
        pause_cont -= 1 

    rect_1 = Rectangle(x = 0, y = rois[0]-20, rz = 0, w = 200, h = 120)
    rect_2 = Rectangle(x = 0, y = rois[1]-20, rz = 0, w = 200, h = 120)

    roi_1 = rect_1.crop_from_img(img_gray)
    roi_2 = rect_2.crop_from_img(img_gray)

    l_Detector_1  = LineDetectorAll(9, True, False, False)
    l_Detector_2  = LineDetectorAll(9, False, False, False)

    line_1 = l_Detector_1.detect(roi_1)
    # line_1[2] = -7
    line_2 = l_Detector_2.detect(roi_2)
    # line_2[2] = -6

    # Scenes
    scene_1 = Scene()
    scene_1.add(rect_1, "rect_1", None)
    scene_1.add(rect_2, "rect_2", None)
    scene_1.add(line_1, "line_1", "rect_1")
    scene_1.add(line_2, "line_2", "rect_2")

    # Global lines
    line_1_global = scene_1.get_global("line_1")
    line_2_global = scene_1.get_global("line_2")

    # img_lines = imagem_rotacionada[100:imagem_rotacionada.shape[0], 120:350].copy()
    # draw_line_1(roi_1, line_1, color=(255, 255, 255), linewidth=4, transparency=0.0)
    # draw_line_1(roi_2, line_2, color=(255, 255, 255), linewidth=4, transparency=0.0)
    # draw_line_1(img_lines, line_1_global, color=(255, 255, 255), linewidth=4, transparency=0.0)
    # draw_line_1(img_lines, line_2_global, color=(255, 255, 255), linewidth=4, transparency=0.0)

    # Vertical line - visualization 
    # cv2.line(img_lines, (int(line_1_global[0]), int(line_1_global[1])), (int(line_2_global[0]), int(line_2_global[1])), (255, 255, 255), 4) 
    
    # Distance plot
    # distance_text = f" {line_2_global[1] - line_1_global[1]:.2f} pixels"
    # cv2.putText(img_lines, distance_text, (int(line_2_global[0]), int((int(line_1_global[1])+int(line_2_global[1]))/2)),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1)


    # print("Line 1-2 distance:\t", line_2_global[1] - line_1_global[1])
    # print("Line 2-3 distance:\t", line_3_global[0] - line_2_global[0], "\n")


    return float(line_2_global[1] - line_1_global[1]), sobel_y
    # img_path = 'result_image.png'
    # cv2.imwrite(img_path, img_lines) 
    # clear_output(wait=True)
    # display(Image(filename=img_path))
    # display(plt.gcf())